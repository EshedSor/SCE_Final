# tests/test_consumers.py
import pytest
from channels.testing import WebsocketCommunicator
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from chat.consumers import ChatConsumer
from chat.models import Chat, Message
from asgiref.sync import async_to_sync

User = get_user_model()

@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_websocket_connect_and_message_flow():
    user_1 = await database_sync_to_async(User.objects.create_user)(phone="1234567890", password="password123")
    user_2 = await database_sync_to_async(User.objects.create_user)(phone="0987654321", password="password123")
    chat = await database_sync_to_async(Chat.objects.create)(member_1=user_1, member_2=user_2)

    communicator = WebsocketCommunicator(application=ChatConsumer.as_asgi(), path=f"/ws/chat/chat_{chat.id}/?token=valid_token")
    communicator.scope['user'] = user_1

    connected, subprotocol = await communicator.connect()
    assert connected

    # Test sending a message
    message_data = {
        'message': {
            'sender': user_1.id,
            'content': "Hello World!"
        }
    }

    await communicator.send_json_to(message_data)

    response = await communicator.receive_json_from()
    assert response['message']['content'] == "Hello World!"

    await communicator.disconnect()

@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_websocket_unauthenticated():
    communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), path=f"/ws/chat/chat_1/")
    connected, subprotocol = await communicator.connect()
    assert not connected  # Connection should fail for unauthenticated users
