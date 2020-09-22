from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        print('aqui', text_data)
        text_data_json = json.loads(text_data)
        print(text_data_json)
        message = text_data_json['message']
        print(message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

class WebhookConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """While the connection is open, it is associated with a callback id"""
        self.callback = self.scope["url_route"]["kwargs"]["uuid"]
        await self.channel_layer.group_add(self.callback, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.callback, self.channel_name)

    async def receive(self, text_data):
        # Discard all received data
        pass

    async def new_request(self, event):
        """Sends all the newly received data on the callback"""
        await self.send(text_data=json.dumps(event["data"]))
