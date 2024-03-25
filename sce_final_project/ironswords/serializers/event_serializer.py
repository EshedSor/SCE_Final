from rest_framework import serializers
from ironswords.models.user_model import User
from ironswords.models.event_model import Event,Application


class EventSerializer(serializers.ModelSerializer):
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