# tests/test_models.py
from django.test import TestCase
from communications.models import Chat, Message, Group, GroupMessage
from users.models import User

class ChatModelTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(phone="1234567890", password="password123")
        self.user2 = User.objects.create_user(phone="0987654321", password="password123")
        self.chat = Chat.objects.create(member_1=self.user1, member_2=self.user2)

    def test_create_chat(self):
        self.assertEqual(self.chat.member_1, self.user1)
        self.assertEqual(self.chat.member_2, self.user2)

    def test_create_message(self):
        message = Message.objects.create(content="Hello", sender=self.user1, related_chat=self.chat)
        self.assertEqual(message.related_chat, self.chat)
        self.assertEqual(message.sender, self.user1)

class GroupModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(phone="1234567890", password="password123")
        self.group = Group.objects.create(name="Test Group")

    def test_create_group(self):
        self.assertEqual(self.group.name, "Test Group")

    def test_add_member(self):
        self.group.members.add(self.user)
        self.assertIn(self.user, self.group.members.all())

    def test_create_group_message(self):
        group_message = GroupMessage.objects.create(group=self.group, sender=self.user, content="Group message")
        self.assertEqual(group_message.group, self.group)
        self.assertEqual(group_message.sender, self.user)
        self.assertEqual(group_message.content, "Group message")
