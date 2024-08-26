import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.group_name = f"user_{self.user.id}"

        # Join the user's notification group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the user's notification group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive a message from the group and send it to WebSocket
    async def send_notification(self, event):
        notification = event['notification']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'notification': notification
        }))