from rest_framework import serializers
from ironswords.models import Organization

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['name', 'description', 'contact_name', 'contact_phone']
