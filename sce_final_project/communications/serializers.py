from rest_framework import serializers
from .models import *
from users.models import User
class ChatParticipantSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id','name']
        read_only_fields = ['id']
    def get_name(self,obj):
        return obj.name()
class ChatSerializer(serializers.ModelSerializer):
    member_1 = ChatParticipantSerializer()
    member_2 = ChatParticipantSerializer()
    class Meta:
        model = Chat
        fields = ['member_1','member_2','id']

class MessageSerializer(serializers.ModelSerializer):
    sender = ChatParticipantSerializer()
    related_chat = ChatSerializer()
    class Meta:
        model = Message
        fields = ['id', 'content', 'timestamp', 'read','related_chat','sender']
        read_only_fields = ['id', 'timestamp', 'read']
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['sender'] = ChatParticipantSerializer(instance.sender).data
        response['related_chat'] = ChatSerializer(instance.related_chat).data
        print(response)
        return response
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