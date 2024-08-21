from django.shortcuts import render
from rest_framework import status
from users.models import *
from django.shortcuts import get_object_or_404
from .serializers import *
from rest_framework import viewsets,mixins
from django.http import HttpResponse 
from .models import Event,Application
from rest_framework.decorators import action
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, DateFromToRangeFilter,OrderingFilter

from rest_framework.filters import SearchFilter



class EventFilter(FilterSet):
    start_date = DateFromToRangeFilter()

    class Meta:
        model = Event
        fields = ['recurring', 'organization', 'start_date']
class EventViewset(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin):
    queryset = Event.objects.all()
    
    def get_serializer_class(self):
        if self.action in ('apply','cancel') :
            return ApplicationSerializer
        return EventSerializer
    @action(detail=True, methods=['post'])
    def apply(self, request, pk=None):
        event = self.get_object()
        print(request.data)
        serializer = ApplicationSerializer(data = request.data)
        if serializer.is_valid():#need to make sure there is only one instance for each user and each event
            applications = Application.objects.filter(user = serializer.validated_data['user'],event = event)
            print(applications)
            if len(applications) == 0:
                application = Application(user = serializer.validated_data['user'],event = event,status = "Pending")
                application.save()
                return HttpResponse("Succesfully applied to event",status = status.HTTP_200_OK)
            else:
                print("here")
                return HttpResponse("Already applied to this event",status = status.HTTP_400_BAD_REQUEST)
        else:
            print("here 36")
            return HttpResponse("failed to apply to event",status = status.HTTP_400_BAD_REQUEST)
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        event = self.get_object()
        serializer = ApplicationSerializer(data = request.data)
        if serializer.is_valid():
            try:
                application = Application.objects.get(
        (Q(status='Pending') | Q(status='Approved')),
        user= serializer.validated_data['user'],
        event=event
    )
                application.status = "Canceled"
                application.save()
            except Application.DoesNotExist:
                return HttpResponse("failed to Cancel application 1")
            except Application.MultipleObjectsReturned:
                return HttpResponse("failed to Cancel application 2")
            return HttpResponse("Succesfully Canceled Application")
        else:
            return HttpResponse("failed to Cancel application 3")
        
class ShiftViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = ShiftEventSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['recurring', 'organization']
    search_fields = ['name', 'description']
    filterset_class = EventFilter

class OrgApplicationFilter(FilterSet):
    class Meta:
        model = Application
        fields = ['id', 'user', 'event']
class OrganizationApplicationViewSet(mixins.ListModelMixin,mixins.UpdateModelMixin,viewsets.GenericViewSet):
    serializer_class = OrganizationApplicationSerializer
    queryset = Application.objects.all()
    filterset_class = OrgApplicationFilter
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    def get_queryset(self):
        organization_id = self.request.user.organization
        return Application.objects.filter(event__organization_id = organization_id)