import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from .custom_middleware.jwt_middleware import JWTAuthMiddleware

from channels.routing import ProtocolTypeRouter, URLRouter
import customers.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "future_pays.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTAuthMiddleware(
        URLRouter(
            customers.routing.websocket_urlpatterns
        )
    ),
})
