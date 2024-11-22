// static/chat/js/room.js
document.addEventListener('DOMContentLoaded', function() {
    const chatLog = document.querySelector('#chat-log');
    const messageForm = document.querySelector('#message-form');
    const messageInput = document.querySelector('#message-input');

    if (!chatLog || !messageForm || !messageInput) {
        console.error("Required chat elements are missing.");
        return;
    }

    const socket = new WebSocket('ws://' + window.location.host + '/ws/chat/main_room/');

    socket.onopen = function() {
        console.log("WebSocket connection established");
    };

    socket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        if (data.message && data.username && data.timestamp) {
            const messageElement = document.createElement('div');
            messageElement.classList.add('message');

            // Display the message with the username and timestamp
            messageElement.innerHTML = `<strong>${data.username}</strong> [${data.timestamp}]: ${data.message}`;
            chatLog.appendChild(messageElement);
            chatLog.scrollTop = chatLog.scrollHeight;
        }
    };

    socket.onerror = function(e) {
        console.error("WebSocket error:", e);
    };

    messageForm.onsubmit = function(e) {
        e.preventDefault();

        const message = messageInput.value.trim();
        if (message) {
            socket.send(JSON.stringify({'message': message}));
            messageInput.value = '';
        }
    };
});
