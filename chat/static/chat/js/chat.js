document.addEventListener("DOMContentLoaded", function() {
    const roomName = document.body.getAttribute('data-room-name');
    console.log("Room Name:", roomName);

    // Check if room name is available
    if (!roomName) {
        console.error("Room name is missing. Cannot establish WebSocket connection.");
    } else {
        // Create WebSocket connection
        const chatSocket = new WebSocket(
            'ws://' + window.location.host + '/ws/chat/' + roomName + '/'
        );
        
        console.log("WebSocket created:", chatSocket);

        // Handle incoming messages from WebSocket
        chatSocket.onmessage = function(event) {
            const data = JSON.parse(event.data);
            const chatLog = document.getElementById('chat-log');
            const messageElement = document.createElement('div');
            messageElement.textContent = `${data.username}: ${data.message}`;
            chatLog.appendChild(messageElement);
            chatLog.scrollTop = chatLog.scrollHeight;
        };

        // Handle WebSocket closure
        chatSocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly.');
        };

        // Handle WebSocket errors
        chatSocket.onerror = function(e) {
            console.error('Error with WebSocket:', e);
        };

        // Chat form submission
        const chatForm = document.getElementById('chat-form');
        chatForm.onsubmit = function(event) {
            event.preventDefault();
            const messageInput = document.getElementById('chat-message-input');
            const message = messageInput.value;
            
            // Check if the message is not empty
            if (message.trim() !== '') {
                // Check WebSocket state before sending message
                if (chatSocket.readyState === WebSocket.OPEN) {
                    chatSocket.send(JSON.stringify({ 'message': message }));
                    messageInput.value = '';  // Clear the input field
                } else {
                    console.error("WebSocket is not open. Message not sent.");
                }
            } else {
                console.warn("Message is empty. Not sending.");
            }
        };
    }
});
