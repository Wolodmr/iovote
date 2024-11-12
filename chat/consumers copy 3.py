import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get room_name from URL kwargs (already set in the communicator)
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        print(f"Connecting to room: {self.room_group_name}")

        # Accept WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Handle disconnection (clean up resources, close connections, etc.)
        pass

    async def receive(self, text_data):
        try:
            # Ensure text_data is valid JSON
            data = json.loads(text_data)
            message = data.get("message", "")
            
            if message:
                # Broadcast message to room group
                await self.send(text_data=json.dumps({
                    'message': message
                }))
        except json.JSONDecodeError:
            # Handle invalid JSON (e.g., empty or malformed message)
            print("Invalid JSON received:", text_data)
            pass
