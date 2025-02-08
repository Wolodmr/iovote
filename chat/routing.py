# chat/routing.py
from django.urls import re_path
from .consumers import ChatConsumer
from channels.routing import ProtocolTypeRouter

application = ProtocolTypeRouter({})
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
]

