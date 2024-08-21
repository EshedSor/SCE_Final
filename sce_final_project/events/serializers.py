from rest_framework import serializers
from users.models import User
from .models import Event,Application
from organizations.serializers import OrganizationSerializer
class EventSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()  # Include organization details in the event serializer
    class Meta:
        model = Event
        fields = "__all__"
class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"
        extra_kwargs = {
            'status': {'required': False},
        }
class ShiftEventSerializer(serializers.ModelSerializer):
    organization_id = serializers.IntegerField()  # Include organization details in the event serializer
    class Meta:
        model = Event
        fields = "__all__"
class OrganizationApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = ['id','user','event']
