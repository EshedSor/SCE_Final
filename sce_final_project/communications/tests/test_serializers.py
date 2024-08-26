# tests/test_serializers.py
from django.test import TestCase
from communications.serializers import ChatSerializer, MessageSerializer, GroupSerializer, GroupMessageSerializer
from communications.models import Chat, Message, Group, GroupMessage
from users.models import User
from rest_framework.exceptions import ValidationError

class ChatSerializerTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(phone="1234567890", password="password123")
        self.user2 = User.objects.create_user(phone="0987654321", password="password123")
        self.chat = Chat.objects.create(member_1=self.user1, member_2=self.user2)

    def test_chat_serializer_valid(self):
        """Test that the chat serializer handles valid data"""
        serializer = ChatSerializer(instance=self.chat)
        data = serializer.data
        self.assertEqual(data['member_1']['id'], self.user1.id)
        self.assertEqual(data['member_2']['id'], self.user2.id)
        self.assertEqual(data['id'], self.chat.id)

    def test_chat_serializer_invalid(self):
        """Test that the chat serializer raises validation errors with missing data"""
        invalid_data = {
            "member_1": {"id": self.user1.id}
        }
        serializer = ChatSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('member_2', serializer.errors)

class MessageSerializerTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(phone="1234567890", password="password123")
        self.user2 = User.objects.create_user(phone="0987654321", password="password123")
        self.chat = Chat.objects.create(member_1=self.user1, member_2=self.user2)
        self.message = Message.objects.create(content="Hello", sender=self.user1, related_chat=self.chat)

    def test_message_serializer_valid(self):
        """Test that the message serializer handles valid data"""
        serializer = MessageSerializer(instance=self.message)
        data = serializer.data
        self.assertEqual(data['content'], self.message.content)
        self.assertEqual(data['sender']['id'], self.user1.id)
        self.assertEqual(data['related_chat']['id'], self.chat.id)

    def test_message_serializer_invalid(self):
        """Test that the message serializer raises validation errors with missing data"""
        invalid_data = {
            "content": "",
            "related_chat": self.chat.id,
        }
        serializer = MessageSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('content', serializer.errors)

class GroupSerializerTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(phone="1234567890", password="password123")
        self.group = Group.objects.create(name="Test Group")
        self.group.members.add(self.user1)

    def test_group_serializer_valid(self):
        """Test that the group serializer handles valid data"""
        serializer = GroupSerializer(instance=self.group)
        data = serializer.data
        self.assertEqual(data['name'], self.group.name)
        self.assertIn(self.user1.id, data['members'])

    def test_group_serializer_invalid(self):
        """Test that the group serializer raises validation errors with missing data"""
        invalid_data = {
            "name": "",
            "members": [self.user1.id]
        }
        serializer = GroupSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

class GroupMessageSerializerTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(phone="1234567890", password="password123")
        self.group = Group.objects.create(name="Test Group")
        self.group_message = GroupMessage.objects.create(group=self.group, sender=self.user1, content="Group Message Content")

    def test_group_message_serializer_valid(self):
        """Test that the group message serializer handles valid data"""
        serializer = GroupMessageSerializer(instance=self.group_message)
        data = serializer.data
        self.assertEqual(data['content'], self.group_message.content)
        self.assertEqual(data['sender'], self.user1.id)
        self.assertEqual(data['group'], self.group.id)

    def test_group_message_serializer_invalid(self):
        """Test that the group message serializer raises validation errors with missing data"""
        invalid_data = {
            "content": "",
            "group": self.group.id
        }
        serializer = GroupMessageSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('content', serializer.errors)
