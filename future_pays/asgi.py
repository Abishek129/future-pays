"""
ASGI config for future_pays project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""
import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import your_app.routing  # Replace with your actual app name

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'future_pays.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Handles normal Django views
    "websocket": AuthMiddlewareStack(
        URLRouter(
            your_app.routing.websocket_urlpatterns
        )
    ),
})

