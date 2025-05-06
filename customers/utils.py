from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification

def send_order_notification(user, message):
    # Save the notification
    Notification.objects.create(user=user, message=message)

    # Send it to WebSocket group
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user.id}",
        {
            "type": "send_notification",  # this must match consumer method
            "data": {
                "message": message,
            },
        },
    )
