
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

class OrderConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = "orders"
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data):
        # optional: handle messages from frontend
        pass

    def order_placed(self, event):
        self.send(text_data=json.dumps({
            'message': event['message']
        }))
