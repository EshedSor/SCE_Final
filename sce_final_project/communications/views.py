# views.py
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import *
from .serializers import *
from django.db.models import Q,Max, OuterRef, Subquery,F
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageSerializer
    def perform_create(self, serializer):
        message = serializer.save()
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'chat_{message.related_chat.id}',
            {
                'type': 'chat_message',
                'message': MessageSerializer(message).data
            }
        )

    def get_queryset(self):
        user = self.request.user
        queryset = Message.objects.filter(Q(related_chat__member_1=user) | Q(related_chat__member_2=user)).select_related('related_chat','related_chat__member_1', 'related_chat__member_2')
        return queryset
    @action(detail=False, methods=['get'])
    def inbox(self, request):
        user = request.user
        latest_message_subquery = Message.objects.filter(
            Q(related_chat__member_1=OuterRef('related_chat__member_1'), related_chat__member_2=OuterRef('related_chat__member_2')) |
            Q(related_chat__member_1=OuterRef('related_chat__member_2'), related_chat__member_2=OuterRef('related_chat__member_1'))
        ).order_by('-timestamp').values('id')[:1]

        conversations = self.get_queryset().annotate(
            latest_message_id=Subquery(latest_message_subquery)
        ).filter(
            id=F('latest_message_id')
        ).order_by('-timestamp')
        serializer = self.get_serializer(conversations, many=True)
        return Response(serializer.data)
    
    @action(detail=True,methods=['get'])
    def conversation(self,request,pk):
        user = request.user
        chat = Chat.objects.get(id=pk)
        if user not in [chat.member_1, chat.member_2]:
            return Response({'status': 'Unauthorized'}, status=403)

        messages = Message.objects.filter(related_chat=chat).order_by('timestamp')
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)
    @action(detail=False, methods=['get'])
    def sent(self, request):
        messages = self.get_queryset().filter(related_chat__member_1=request.user)
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        message = self.get_object()
        if request.user not in [message.related_chat.member_1, message.related_chat.member_2]:
            return Response({'status': 'Unauthorized'}, status=403)
        message.read = True
        message.save()
        return Response({'status': 'Message marked as read'})

class ChatViewSet(viewsets.ModelViewSet):
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        group = self.get_object()
        user = request.data.get('user_id')
        group.members.add(user)
        group.save()
        return Response({'status': 'User added to group'})

class GroupMessageViewSet(viewsets.ModelViewSet):
    queryset = GroupMessage.objects.all()
    serializer_class = GroupMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        message = self.get_object()
        message.read_by.add(request.user)
        message.save()
        return Response({'status': 'Message marked as read'})