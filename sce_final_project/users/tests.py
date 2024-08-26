from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from .models import User, FriendRequest, generate_otp, verify_otp
from organizations.models import Organization
from .serializers import PhoneSerializer, OTPSerializer, PrefrencesSerializer
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status


class UserModelTests(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name="Test Org")
        self.user = User.objects.create_user(
            phone="1234567890",
            password="password123",
            first_name="John",
            last_name="Doe",
            org=self.org,
            email="john@example.com"
        )

    def test_user_creation(self):
        """Test that a user is created correctly with the required fields."""
        self.assertEqual(self.user.phone, "1234567890")
        self.assertEqual(self.user.email, "john@example.com")
        self.assertEqual(self.user.org, self.org)

    def test_generate_otp(self):
        """Test that an OTP is generated and hashed correctly."""
        otp = generate_otp(self.user)
        self.assertTrue(self.user.otp)
        self.assertTrue(self.user.otp_created_at)
        self.assertEqual(len(str(otp)), 6)

    def test_verify_otp(self):
        """Test that the OTP verification works correctly."""
        otp = generate_otp(self.user)
        self.assertTrue(verify_otp(self.user.phone, otp))  # Correct OTP

        # Test incorrect OTP
        self.assertFalse(verify_otp(self.user.phone, '000000'))

        # Test expired OTP
        self.user.otp_created_at = timezone.now() - timedelta(minutes=10)
        self.user.save()
        self.assertFalse(verify_otp(self.user.phone, otp))


class FriendRequestModelTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(phone="1234567890", password="password123")
        self.user2 = User.objects.create_user(phone="0987654321", password="password456")
        self.friend_request = FriendRequest.objects.create(sender=self.user1, receiver=self.user2)

    def test_friend_request_creation(self):
        """Test that a friend request is created correctly."""
        self.assertEqual(self.friend_request.sender, self.user1)
        self.assertEqual(self.friend_request.receiver, self.user2)
        self.assertEqual(self.friend_request.status, "pending")

    def test_friend_request_acceptance(self):
        """Test friend request acceptance."""
        self.friend_request.status = "accepted"
        self.friend_request.save()
        self.assertEqual(self.friend_request.status, "accepted")


class PhoneSerializerTests(APITestCase):
    def test_valid_phone(self):
        """Test that the phone serializer accepts valid data."""
        data = {'phone': '1234567890'}
        serializer = PhoneSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_phone_length(self):
        """Test that phone numbers with incorrect lengths are rejected."""
        data = {'phone': '12345'}
        serializer = PhoneSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['phone'][0], "Phone number must be 10 digits.")


class OTPSerializerTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(phone="1234567890", password="password123")

    def test_valid_otp(self):
        """Test that OTP validation succeeds with correct data."""
        otp = generate_otp(self.user)
        data = {'phone': self.user.phone, 'otp': str(otp)}
        serializer = OTPSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_otp(self):
        """Test that OTP validation fails with incorrect or expired data."""
        otp = generate_otp(self.user)
        data = {'phone': self.user.phone, 'otp': '000000'}
        serializer = OTPSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['non_field_errors'][0], "OTP incorrect or timed out.")


class PrefrencesSerializerTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone="1234567890", password="password123",
            first_name="John", last_name="Doe"
        )

    def test_valid_prefrences(self):
        """Test that the preferences serializer handles valid data."""
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'gender': 'M',
            'birth_day': '1990-01-01',
            'volunteer_frequency': 1,
            'volunteer_categories': ["Packaging", "Driving"],
            'most_important': 'Friends',
            'allow_notifications': True,
            'finished_onboarding': True,
            'phone': '1234567890'
        }
        serializer = PrefrencesSerializer(instance=self.user, data=data)

        # Print errors if validation fails
        if not serializer.is_valid():
            print(serializer.errors)

        self.assertTrue(serializer.is_valid())


class OTPViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(phone="1234567890", password="password123")

    def test_send_otp(self):
        """Test sending OTP to a valid user."""
        url = reverse('send_otp-list')  # Use 'send_otp-list' for the create action
        data = {'phone': self.user.phone}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_verify_otp(self):
        """Test verifying OTP."""
        otp = generate_otp(self.user)
        url = reverse('verify_otp-list')  # Use 'verify_otp-list' for the create action
        data = {'phone': self.user.phone, 'otp': otp}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_otp(self):
        """Test that OTP validation fails with incorrect or expired data."""
        otp = generate_otp(self.user)
        url = reverse('verify_otp-list')
        data = {'phone': self.user.phone, 'otp': '000000'}  # Incorrect OTP
        response = self.client.post(url, data, format='json')

        # Compare the string version of the error
        self.assertEqual(str(response.data['non_field_errors'][0]).strip(), "OTP incorrect or timed out.".strip())