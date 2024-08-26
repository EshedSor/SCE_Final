from django.shortcuts import render
from rest_framework import status,permissions
from users.models import *
from django.shortcuts import get_object_or_404
from events.serializers import *
from rest_framework import viewsets,mixins
from django.http import HttpResponse 
from events.models import Event,Application
from rest_framework.decorators import action
from django.db.models import Q
from django_filters.rest_framework import FilterSet, DateFromToRangeFilter,CharFilter,BaseInFilter,NumberFilter
from rest_framework.filters import OrderingFilter
from django_filters import rest_framework as filters

from rest_framework.filters import SearchFilter


class NumberInFilter(BaseInFilter, NumberFilter):
    pass
class EventFilter(FilterSet):
    start_date = DateFromToRangeFilter()
    volunteers = CharFilter(method='filter_by_volunteers_or_friends')

    class Meta:
        model = Event
        fields = ['recurring', 'organization', 'start_date','volunteers']

    def filter_by_volunteers_or_friends(self, queryset, name, value):
        if value == "friends":
            # Assuming you have a way to get the current user and their friends
            user = self.request.user
            friends_ids = user.friends.values_list('id', flat=True)
            
            # Filter events by friends
            return queryset.filter(volunteers__in=friends_ids)
        if value == "self":
            # Assuming you have a way to get the current user and their friends
            user = self.request.user            
            # Filter events by self
            qs = queryset.filter(volunteers__in=[self.request.user.id])
            print(self.request.user.id)
            return qs
        else:
            # Default behavior for filtering by volunteers
            volunteers_ids = value.split(',')
            return queryset.filter(volunteers__in=volunteers_ids)
    #def filter_volunteers(self, queryset, name, value):
    #    volunteers = value.split(',')
    #    return queryset.filter(volunteers__user_id=volunteers)
class EventViewset(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin):
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = EventFilter
    filter_backends = [filters.DjangoFilterBackend,OrderingFilter,SearchFilter]
    search_fields = ['name', 'description','organization__name']
    queryset = Event.objects.filter(start_date__gt=timezone.now())
    def get_serializer_class(self):
        if self.action in ('apply','cancel') :
            return ApplicationSerializer
        return EventSerializer
    @action(detail=True, methods=['post'])
    def apply(self, request, pk=None):
        event = self.get_object()
        print(request.data)
        try:
            applications = Application.objects.get(user = self.request.user,event = event)
            return HttpResponse({"message":"failed to apply application Already applied"},status = status.HTTP_400_BAD_REQUEST)
        except Application.DoesNotExist:
            application = Application.objects.create(user = self.request.user,event = event,status = "pending")
            return HttpResponse({"message":"Succesfully applied Application"},status = status.HTTP_200_OK)
        except Application.MultipleObjectsReturned:
                return HttpResponse({"message":"failed to apply application MultipleObjectsReturned"},status = status.HTTP_400_BAD_REQUEST)
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        event = self.get_object()
        #serializer = ApplicationSerializer(data = request.data)
        #if serializer.is_valid():
        try:
                application = Application.objects.get(
        (Q(status='Pending') | Q(status='Approved')),
        user= self.request.user,
        event=event
    )
                application.status = "Canceled"
                application.save()
                event.volunteers.remove(self.request.user)
                event.save() 
                return HttpResponse("Succesfully Canceled Application",status = status.HTTP_200_OK)
        except Application.DoesNotExist:
                print(1)
                return HttpResponse("failed to Cancel application DoesNotExist",status = status.HTTP_400_BAD_REQUEST)
        except Application.MultipleObjectsReturned:
                print(2)
                return HttpResponse("failed to Cancel application MultipleObjectsReturned",status = status.HTTP_400_BAD_REQUEST)
        #else:
        #    print(3)
        #    return HttpResponse("failed to Cancel application 3",status = status.HTTP_400_BAD_REQUEST)
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        event = self.get_object()
        #serializer = ApplicationSerializer(data = request.data)
        #if serializer.is_valid():
        try:
                application = Application.objects.get(
        (Q(status='Approved')),
        user= self.request.user,
        event=event
    )
                application.status = "Confirmed"
                application.save()
                return HttpResponse("Succesfully approved Application",status = status.HTTP_200_OK)
        except Application.DoesNotExist:
                print(1)
                return HttpResponse("failed to approve application DoesNotExist",status = status.HTTP_400_BAD_REQUEST)
        except Application.MultipleObjectsReturned:
                print(2)
                return HttpResponse("failed to approve application MultipleObjectsReturned",status = status.HTTP_400_BAD_REQUEST)
        #else:
        #    print(3)
        #    return HttpResponse("failed to Cancel application 3",status = status.HTTP_400_BAD_REQUEST)    
class ShiftViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Event.objects.all()
    serializer_class = ShiftEventSerializer
    filterset_fields = ['recurring', 'organization']
    search_fields = ['name', 'description']
    filterset_class = EventFilter


class OrgApplicationFilter(FilterSet):
    status = CharFilter(field_name='status', lookup_expr='iexact')  # Case-insensitive filter
    class Meta:
        model = Application
        fields = ['id', 'user', 'event',"status"]
class OrganizationApplicationViewSet(mixins.RetrieveModelMixin,mixins.ListModelMixin,mixins.UpdateModelMixin,viewsets.GenericViewSet):
    serializer_class = OrganizationApplicationSerializer
    filterset_class = OrgApplicationFilter
    filter_backends = [filters.DjangoFilterBackend,OrderingFilter]
    def get_queryset(self):
        if(not self.request.user.is_anonymous):
            organization_id = self.request.user.org
            print(self.request.user.org)
            return Application.objects.filter(event__organization_id = organization_id)
        return Application.objects.filter(id = -1)
    @action(detail=True, methods=['post'])
    def decline(self, request, pk=None):
        app = self.get_object()
        print(app)
        if app.status == "Pending":
             app.status = "Declined"
             app.save()
             return HttpResponse({"message":"declined application succefully"},status = status.HTTP_200_OK)
        return HttpResponse({"message":"application status isnt pending"},status=status.HTTP_400_BAD_REQUEST)
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        app = self.get_object()
        if app.status.lower() == "pending":
            if app.event.max_volunteers > (app.event.volunteers.count()):
                app.status = "Approved"
                app.event.volunteers.add(app.user)
                app.save()
                print(mixins.ListModelMixin)
                return HttpResponse({"message":mixins.ListModelMixin},status = status.HTTP_200_OK)
            print("already reached max capacity")
            return HttpResponse({"message":"already reached max capacity"},status = status.HTTP_400_BAD_REQUEST)
        print("application status isnt pending")
        return HttpResponse({"message":"application status isnt pending"},status=status.HTTP_400_BAD_REQUEST)