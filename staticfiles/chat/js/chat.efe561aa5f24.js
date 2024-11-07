document.addEventListener("DOMContentLoaded", function() {
    const roomName = document.body.getAttribute('data-room-name');
    console.log("Room Name:", roomName);

    if (!roomName) {
        console.error("Room name is missing. Cannot establish WebSocket connection.");
    } else {
        const chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat/${roomName}/`);
        console.log("WebSocket created:", chatSocket);

        chatSocket.onmessage = function(event) {
            const data = JSON.parse(event.data);
            const chatLog = document.getElementById('chat-log');
            const messageElement = document.createElement('div');
            messageElement.textContent = `${data.username}: ${data.message}`;
            chatLog.appendChild(messageElement);
            chatLog.scrollTop = chatLog.scrollHeight;
        };

        chatSocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly.');
        };

        const chatForm = document.getElementById('chat-form');
        chatForm.onsubmit = function(event) {
            event.preventDefault();
            const messageInput = document.getElementById('chat-message-input');
            const message = messageInput.value;
            if (message.trim() !== '') {
                if (chatSocket.readyState === WebSocket.OPEN) {
                    chatSocket.send(JSON.stringify({ 'message': message }));
                    messageInput.value = '';  // Clear the input field
                } else {
                    console.error("WebSocket is not open. Message not sent.");
                }
            }
        };
    }
});
