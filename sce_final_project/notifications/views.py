from django.shortcuts import render

# Create your views here.

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def send_friend_request_notification(sender, receiver,frequest):
    notification_data = {
        'type': 'friend_request',
        'message': f"{sender.name()} sent you a friend request!",
        'request_id': frequest.id,
    }

    # Send notification to the receiver's WebSocket group via Redis
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{receiver.id}",
        {
            'type': 'send_notification',
            'notification': notification_data
        }
    )
def send_message_notification(sender, receiver):
    notification_data = {
        'type': 'new_message',
        'message': f"{sender.name()} sent you a new message",
    }
    print(notification_data)
    # Send notification to the receiver's WebSocket group via Redis
    channel_layer = get_channel_layer()
    print(channel_layer)
    async_to_sync(channel_layer.group_send)(
        f"user_{receiver.id}",
        {
            'type': 'send_notification',
            'notification': notification_data
        }
    )