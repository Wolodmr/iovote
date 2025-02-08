from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def broadcast_message_to_chat(message):
    """
    Broadcast a message to all connected WebSocket clients in the chat.
    
    Args:
        message (str): The message to be sent.
    """
    # Get the default channel layer
    channel_layer = get_channel_layer()
    
    # Specify the group name (this should match the group name used in your chat consumer)
    group_name = "chat_lobby"  # Replace with your actual group name if different

    # Send the message to the group
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "chat_message",  # The method in your consumer to handle this event
            "message": message,
        }
    )

