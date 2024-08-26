from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from events.models import Event, Application
from organizations.models import Organization
from users.models import User
from events.serializers import EventSerializer, ApplicationSerializer
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
class EventModelTests(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(name="Test Organization")
        self.user = User.objects.create_user(phone="1234567890", password="password123")
        self.event = Event.objects.create(
            name="Test Event",
            description="Test Description",
            recurring=False,
            max_volunteers=5,
            start_date=timezone.now() + timedelta(days=1),
            duration=timedelta(hours=2),
            organization=self.organization,
        )

    def test_event_creation(self):
        """Test that an event is created successfully."""
        self.assertEqual(self.event.name, "Test Event")
        self.assertEqual(self.event.description, "Test Description")
        self.assertEqual(self.event.organization, self.organization)

    def test_event_volunteers(self):
        """Test adding and removing volunteers from an event."""
        self.event.volunteers.add(self.user)
        self.assertEqual(self.event.volunteers.count(), 1)
        self.event.volunteers.remove(self.user)
        self.assertEqual(self.event.volunteers.count(), 0)


class ApplicationModelTests(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(name="Test Organization")
        self.user = User.objects.create_user(phone="1234567890", password="password123")
        self.event = Event.objects.create(
            name="Test Event",
            description="Test Description",
            recurring=False,
            max_volunteers=5,
            start_date=timezone.now() + timedelta(days=1),
            duration=timedelta(hours=2),
            organization=self.organization,
        )
        self.application = Application.objects.create(user=self.user, event=self.event, status="Pending")

    def test_application_creation(self):
        """Test that an application is created successfully."""
        self.assertEqual(self.application.user, self.user)
        self.assertEqual(self.application.event, self.event)
        self.assertEqual(self.application.status, "Pending")

    def test_application_unique_together(self):
        """Test that a user can only have one application per event."""
        with self.assertRaises(Exception):
            Application.objects.create(user=self.user, event=self.event)
class EventSerializerTests(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(name="Test Organization")
        self.user = User.objects.create_user(phone="1234567890", password="password123")
        self.event_data = {
            "name": "Test Event",
            "description": "Test Description",
            "recurring": False,
            "max_volunteers": 5,
            "start_date": timezone.now() + timedelta(days=1),
            "duration": timedelta(hours=2),
            "organization": self.organization  # Correct this line
        }
        self.event = Event.objects.create(**self.event_data)

    def test_event_serializer_valid(self):
        """Test that the event serializer is valid with correct data."""
        serializer = EventSerializer(instance=self.event)
        serialized_data = serializer.data
        self.assertEqual(serialized_data['name'], self.event.name)
        self.assertEqual(serialized_data['description'], self.event.description)

    def test_event_serializer_invalid(self):
        """Test that the event serializer is invalid with missing data."""
        invalid_data = self.event_data.copy()
        invalid_data.pop("name")
        serializer = EventSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)



class ApplicationSerializerTests(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(name="Test Organization")
        self.user = User.objects.create_user(phone="1234567890", password="password123")
        self.event = Event.objects.create(
            name="Test Event",
            description="Test Description",
            recurring=False,
            max_volunteers=5,
            start_date=timezone.now() + timedelta(days=1),
            duration=timedelta(hours=2),
            organization=self.organization,
        )
        self.application_data = {
            "user": self.user.id,
            "event": self.event.id,
            "status": "Pending"
        }

    def test_application_serializer_valid(self):
        """Test that the application serializer is valid with correct data."""
        serializer = ApplicationSerializer(data=self.application_data)
        self.assertTrue(serializer.is_valid())

    def test_application_serializer_invalid(self):
        """Test that the application serializer is invalid with missing data."""
        invalid_data = self.application_data.copy()
        invalid_data.pop("user")
        serializer = ApplicationSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('user', serializer.errors)

class EventViewsetTests(APITestCase):
    def setUp(self):
        self.organization = Organization.objects.create(name="Test Organization")
        self.user = User.objects.create_user(phone="1234567890", password="password123")
        self.client.force_authenticate(user=self.user)
        self.event = Event.objects.create(
            name="Test Event",
            description="Test Description",
            recurring=False,
            max_volunteers=5,
            start_date=timezone.now() + timedelta(days=1),
            duration=timedelta(hours=2),
            organization=self.organization,
        )
    
    def test_list_events(self):
        """Test listing all events."""
        url = reverse('event-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_apply_for_event(self):
        """Test applying for an event."""
        url = reverse('event-apply', args=[self.event.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Application.objects.count(), 1)

    def test_cancel_application(self):
        """Test canceling an application."""
        Application.objects.create(user=self.user, event=self.event, status="Pending")
        url = reverse('event-cancel', args=[self.event.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Application.objects.filter(status="Canceled").count(), 1)

    def test_confirm_application(self):
        """Test confirming an approved application."""
        Application.objects.create(user=self.user, event=self.event, status="Approved")
        url = reverse('event-confirm', args=[self.event.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Application.objects.filter(status="Confirmed").count(), 1)


class ShiftViewSetTests(APITestCase):
    def setUp(self):
        self.organization = Organization.objects.create(name="Test Organization")
        self.user = User.objects.create_user(phone="1234567890", password="password123")
        self.client.force_authenticate(user=self.user)
        self.event = Event.objects.create(
            name="Test Event Shift",
            description="Test Shift Description",
            recurring=False,
            max_volunteers=5,
            start_date=timezone.now() + timedelta(days=1),
            duration=timedelta(hours=2),
            organization=self.organization,
        )

    def test_list_shifts(self):
        """Test listing all shifts."""
        url = reverse('shift-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_shift(self):
        """Test creating a shift."""
        url = reverse('event-list')
        shift_data = {
            "name": "New Shift",
            "description": "New Shift Description",
            "recurring": False,
            "max_volunteers": 10,
            "start_date": timezone.now() + timedelta(days=1),
            "duration": timedelta(hours=2),
            "organization": self.organization.id
        }
        response = self.client.post(url, shift_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Event.objects.count(), 1)
