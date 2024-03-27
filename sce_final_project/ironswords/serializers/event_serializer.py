from rest_framework import serializers
from ironswords.models.user_model import User
from ironswords.models.event_model import Event,Application
from ironswords.models.organization_model import Organization

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['name', 'description', 'contact_name', 'contact_phone']

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