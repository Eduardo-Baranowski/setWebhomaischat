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
        print('aqui1', text_data)
        pass

    async def new_request(self, event):
        """Sends all the newly received data on the callback"""
        text_data = json.dumps(event["data"])
        datastore = json.loads(text_data)
        texto = datastore["body"]
        msg = json.loads(texto)
        #print('msg', msg)
        msg1 = msg["messages"]
        # formated = 'contato: '+contato+'----'+ 'menssagem: '+msg
        #print(msg1[0]['body'])
        #print(msg1[0]['chatName'])
        #jason = "'chatName'"+':'+ "'"+str(msg1[0]['chatName'])+"'"+','+"'body'"+':'+ "'"+str(msg1[0]['body'])+"'"
        jason = {'chatName': str(msg1[0]['chatName']), 'body': str(msg1[0]['body'])}
        #jason = json.dumps(jason)
        #jason = 'jason',jason.replace('"','')
        msg["messages"] = jason
        #print('msg formatada', msg)

        text_data = json.loads(text_data)
        #datastore = json.loads(text_data)
        text_data["body"] = msg
        await self.send(text_data=json.dumps(text_data))
        #print('text_data', text_data)
