import asyncio
from channels.testing import WebsocketCommunicator
from channels.layers import get_channel_layer
from chat.routing import application  # Ensure this is the correct import for your ASGI application

async def test_channel_layer():
    # Correct WebSocket path (must be a string)
    communicator = WebsocketCommunicator(application, "/ws/chat/")  # Ensure '/ws/chat/' matches your WebSocket URL
    connected, subprotocol = await communicator.connect()
    assert connected, "WebSocket connection failed"
    
    # Sending a test message
    await communicator.send_json_to({"message": "Hello, world!"})
    
    # Receiving the message
    response = await communicator.receive_json_from()
    
    # Verifying the response
    assert response["message"] == "Hello, world!", f"Expected message, got {response}"
    
    # Disconnecting
    await communicator.disconnect()

# To run this test, you can use `asyncio.run(test_channel_layer())` for standalone testing
