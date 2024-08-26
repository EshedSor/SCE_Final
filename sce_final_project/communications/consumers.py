import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Message, Chat
from users.models import User
from notifications.views import send_message_notification
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name'].split('_')[1]
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope["user"]

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        if self.user.is_authenticated:
            print(self.user.id)
            # Send the chat history to the client
            messages = await self.get_chat_history(self.room_name)
            for message in messages:
                sender = await self.get_user_info(message)
                await self.send(text_data=json.dumps({
                    'message': {
                        'sender': sender,
                        'content': message.content,
                        'timestamp': message.timestamp.isoformat(),
                    }
                }))
        else:
            await self.send(text_data=json.dumps({
                'error': 'Authentication failed.'
            }))
            await self.close()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_data = text_data_json['message']
        content = message_data['content']
        chat = await self.get_chat(self.room_name)

        await self.save_message(chat, content)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_data
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)

    @sync_to_async
    def get_chat(self, chat_id):
        return Chat.objects.get(id=chat_id)

    @sync_to_async
    def save_message(self, chat, content):
        receiver = chat.member_2 if chat.member_1 == self.user else chat.member_1
        send_message_notification(sender =self.user,receiver = receiver)
        Message.objects.create(related_chat=chat, content=content, sender=self.user)

    @sync_to_async
    def get_chat_history(self, chat_id):
        chat = Chat.objects.get(id=chat_id)
        history = list(Message.objects.filter(related_chat=chat).order_by('timestamp'))
        for i in history:
            print(i.sender_id)
        return history

    @sync_to_async
    def get_user_info(self, message):
        # Helper method to retrieve sender information asynchronously
        sender = message.sender
        return {
            'id': sender.id,
            'name': sender.name(),
        }