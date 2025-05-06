import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Notification
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model

class OrderStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.group_name = f"user_{self.user_id}"

        # Join Redis group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # Optional: send unseen notifications
        unseen_notifications = await self.get_unseen_notifications()
        for note in unseen_notifications:
            await self.send(text_data=json.dumps({
                "message": note.message,
                "timestamp": str(note.timestamp),
            }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_notification(self, event):
        await self.send(text_data=json.dumps(event["data"]))

    @sync_to_async
    def get_unseen_notifications(self):
        return Notification.objects.filter(user_id=self.user_id, seen=False)
