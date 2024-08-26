# tests/test_permissions.py
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from chat.permissions import IsGroupMember
from chat.models import Group, GroupMessage
from users.models import User

class GroupPermissionsTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(phone="1234567890", password="password123")
        self.user2 = User.objects.create_user(phone="0987654321", password="password123")
        self.group = Group.objects.create(name="Test Group")
        self.group.members.add(self.user1)

    def test_group_member_permission(self):
        permission = IsGroupMember()
        factory = APIRequestFactory()
        request = factory.get('/')
        request.user = self.user1

        # Test if user1 has access to the group
        self.assertTrue(permission.has_object_permission(request, None, self.group))

        # Test if user2 is denied access
        request.user = self.user2
        self.assertFalse(permission.has_object_permission(request, None, self.group))
