import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "chat_lobby"
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def chat_message(self, event):
        # Retrieve the message from the event
        message = event["message"]

        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            "message": message
        }))
