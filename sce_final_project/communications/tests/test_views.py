# tests/test_views.py
from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import User
from chat.models import Chat, Message, Group, GroupMessage
from rest_framework import status

class ChatViewSetTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(phone="1234567890", password="password123")
        self.user2 = User.objects.create_user(phone="0987654321", password="password123")
        self.client.force_authenticate(user=self.user1)

    def test_create_chat(self):
        url = reverse('chat-list')
        data = {
            "member_1": {"id": self.user1.id},
            "member_2": {"id": self.user2.id}
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_conversation(self):
        chat = Chat.objects.create(member_1=self.user1, member_2=self.user2)
        Message.objects.create(content="Hello", sender=self.user1, related_chat=chat)
        
        url = reverse('message-conversation', args=[chat.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_message(self):
        chat = Chat.objects.create(member_1=self.user1, member_2=self.user2)
        url = reverse('message-list')
        data = {
            "related_chat": chat.id,
            "content": "Hello",
            "sender": self.user1.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class GroupViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(phone="1234567890", password="password123")
        self.client.force_authenticate(user=self.user)
        self.group = Group.objects.create(name="Test Group")

    def test_create_group(self):
        url = reverse('group-list')
        data = {
            "name": "New Group",
            "members": [self.user.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_member(self):
        url = reverse('group-add-member', args=[self.group.id])
        data = {"user_id": self.user.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GroupMessageViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(phone="1234567890", password="password123")
        self.client.force_authenticate(user=self.user)
        self.group = Group.objects.create(name="Test Group")
        self.group.members.add(self.user)

    def test_create_group_message(self):
        url = reverse('groupmessage-list')
        data = {
            "group": self.group.id,
            "content": "Group message",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
