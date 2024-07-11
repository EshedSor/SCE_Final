from rest_framework import serializers
from ironswords.models.user_model import User
from ironswords.models.event_model import Event,Application
from ironswords.serializers.organization_serializers import OrganizationSerializer
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