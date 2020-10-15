# chat/consumers.py
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import GameResult
from channels.auth import login

class GameResultConsumer(WebsocketConsumer):

    def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['room_name']

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name,
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name,
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'receive_result',
                'message': message
            }
        )
     
    def receive_result(self, event):
        message = event['message']
        self.send(text_data=message)