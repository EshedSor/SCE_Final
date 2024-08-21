from django.db import models
from users.models import User

class Chat(models.Model):
    member_1 = models.ForeignKey(User,related_name='chats_as_member_1',on_delete=models.CASCADE)
    member_2 = models.ForeignKey(User,related_name='chats_as_member_2',on_delete=models.CASCADE)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['member_1', 'member_2'], name='unique_chat_members')
        ]
class Message(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    related_chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User,on_delete=models.CASCADE)
class Group(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name='communication_groups')

    def __str__(self):
        return self.name

class GroupMessage(models.Model):
    group = models.ForeignKey(Group, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='group_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read_by = models.ManyToManyField(User, related_name='read_group_messages', blank=True)

    def __str__(self):
        return f'Message from {self.sender} in {self.group} at {self.timestamp}'

