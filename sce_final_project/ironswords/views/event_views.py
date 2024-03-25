from django.shortcuts import render
from rest_framework import status
from ironswords.models.user_model import *
from django.shortcuts import get_object_or_404
from ironswords.serializers.event_serializer import *
from rest_framework import viewsets,mixins
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.parsers import JSONParser
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from ironswords.models.event_model import Event,Application
from rest_framework.decorators import action
from django.db.models import Q
class EventViewset(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin):
    queryset = Event.objects.all()
    def get_serializer_class(self):
        if self.action in ('apply','cancel') :
            return ApplicationSerializer
        return EventSerializer
    @action(detail=True, methods=['post'])
    def apply(self, request, pk=None):
        event = self.get_object()
        serializer = ApplicationSerializer(data = request.data)
        if serializer.is_valid():#need to make sure there is only one instance for each user and each event
            application = Application(user = serializer.validated_data['user'],event = event,status = "Pending")
            application.save()
            return HttpResponse("Succesfully applied to event")
        else:
            return HttpResponse("failed to apply to event")
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