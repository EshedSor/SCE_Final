from rest_framework import viewsets
from ironswords.models import Organization
from ironswords.serializers.organization_serializers import *
class OrganizationViewset(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer