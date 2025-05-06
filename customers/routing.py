from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/order_status/<str:user_id>/", consumers.OrderStatusConsumer.as_asgi()),
]
