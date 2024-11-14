import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "main_room"
        self.room_group_name = f"chat_{self.room_name}"

        # Join the room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Notify on user join
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": "A new user has joined the chat!",
                "message_type": "notification",
            },
        )

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        # Notify on user leave
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": "A user has left the chat.",
                "message_type": "notification",
            },
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]

        # Send message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "message_type": "chat",
            },
        )

    async def chat_message(self, event):
        message = event["message"]
        message_type = event["message_type"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "message_type": message_type}))
