# chat/routing.py
from django.urls import re_path
from . import consumers

# Updated WebSocket URL pattern to match the URL used in chat.js
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),  # **<-- Updated to `ws/chat/` to match JavaScript**
]
