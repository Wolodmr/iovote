# chat/routing.py

from django.urls import re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from . import consumers

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            re_path(r"^ws/chat/$", consumers.ChatConsumer.as_asgi()),
        ])
    ),
})
