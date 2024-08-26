from django.test import TestCase
from .models import Organization
from .serializers import OrganizationSerializer
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class OrganizationModelTests(TestCase):

    def setUp(self):
        self.organization = Organization.objects.create(
            name="Test Organization",
            description="Test description",
            contact_name="John Doe",
            contact_phone="1234567890"
        )

    def test_organization_creation(self):
        """Test that an organization can be created successfully."""
        self.assertEqual(self.organization.name, "Test Organization")
        self.assertEqual(self.organization.description, "Test description")
        self.assertEqual(self.organization.contact_name, "John Doe")
        self.assertEqual(self.organization.contact_phone, "1234567890")

    def test_organization_blank_fields(self):
        """Test that blank fields are handled correctly."""
        organization = Organization.objects.create(
            name="Another Organization",
            description="",
            contact_name="",
            contact_phone=""
        )
        self.assertEqual(organization.description, "")
        self.assertEqual(organization.contact_name, "")
        self.assertEqual(organization.contact_phone, "")
class OrganizationSerializerTests(TestCase):

    def setUp(self):
        self.organization_data = {
            'name': "Test Organization",
            'description': "Test description",
            'contact_name': "John Doe",
            'contact_phone': "1234567890"
        }
        self.organization = Organization.objects.create(**self.organization_data)

    def test_serializer_valid(self):
        """Test that the serializer is valid when provided with correct data."""
        serializer = OrganizationSerializer(data=self.organization_data)
        self.assertTrue(serializer.is_valid())
    
    def test_serializer_invalid(self):
        """Test that the serializer is invalid when required fields are missing."""
        invalid_data = {
            'description': "Test description",
            'contact_name': "John Doe",
            'contact_phone': "1234567890"
        }
        serializer = OrganizationSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    def test_serializer_save(self):
        """Test that the serializer correctly saves the organization."""
        serializer = OrganizationSerializer(data=self.organization_data)
        self.assertTrue(serializer.is_valid())
        organization = serializer.save()
        self.assertEqual(organization.name, "Test Organization")
        self.assertEqual(organization.description, "Test description")

class OrganizationViewsetTests(APITestCase):
    def setUp(self):
        # Ensure the test starts with a clean slate by clearing any existing organizations
        Organization.objects.all().delete()

        # Create a single organization for this test
        self.organization = Organization.objects.create(
            name="Test Organization",
            description="Test description",
            contact_name="John Doe",
            contact_phone="1234567890"
        )
    
    def test_list_organizations(self):
        """Test listing all organizations."""
        url = reverse('organization-list')  # Ensure you are using the correct URL name
        response = self.client.get(url)
        
        # Validate that the request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that only 1 organization is returned
        self.assertEqual(len(response.data['results']), 1)  # Pagination may return 'results'
        self.assertEqual(response.data['results'][0]['name'], self.organization.name)

    def test_create_organization(self):
        """Test creating an organization via POST."""
        url = reverse('organization-list')
        
        # Convert the organization data to a dictionary for the POST request
        organization_data = {
            'name': "New Organization",
            'description': "New description",
            'contact_name': "Jane Doe",
            'contact_phone': "0987654321"
        }
        
        response = self.client.post(url, organization_data, format='json')
        
        # Check that the response is successful and a new organization is created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Organization.objects.count(), 2)  # Ensure the organization was created


    def test_retrieve_organization(self):
        """Test retrieving a single organization."""
        url = reverse('organization-detail', args=[self.organization.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Test Organization")

    def test_update_organization(self):
        """Test updating an organization via PUT."""
        url = reverse('organization-detail', args=[self.organization.id])
        update_data = {
            'name': "Updated Organization",
            'description': "Updated description",
            'contact_name': "John Updated",
            'contact_phone': "1234567899"
        }
        response = self.client.put(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.organization.refresh_from_db()
        self.assertEqual(self.organization.name, "Updated Organization")
        self.assertEqual(self.organization.contact_phone, "1234567899")

    def test_delete_organization(self):
        """Test deleting an organization via DELETE."""
        url = reverse('organization-detail', args=[self.organization.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Organization.objects.count(), 0)  # Ensure the organization was deleted