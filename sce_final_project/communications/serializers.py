from rest_framework import serializers
from .models import *

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'content', 'timestamp', 'read']
        read_only_fields = ['id', 'sender', 'timestamp', 'read']
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'members']
        read_only_fields = ['id']

class GroupMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMessage
        fields = ['id', 'group', 'sender', 'content', 'timestamp', 'read_by']
        read_only_fields = ['id', 'sender', 'timestamp', 'read_by']