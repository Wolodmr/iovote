document.addEventListener("DOMContentLoaded", function () {
    function connectToRoom(roomName) {
        if (!roomName) {
            console.log("Room name is missing. Cannot establish WebSocket connection.");
            return;
        }

        console.log("Attempting to connect to WebSocket with room name:", roomName);
        
        const chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat/${roomName}/`);

        chatSocket.onopen = function () {
            console.log("WebSocket connection established.");
        };

        chatSocket.onmessage = function (event) {
            const data = JSON.parse(event.data);
            console.log("Received message:", data.message);

            const messageElement = document.createElement("p");
            messageElement.textContent = data.message;
            document.getElementById("messages").appendChild(messageElement);
        };

        chatSocket.onclose = function () {
            console.log("WebSocket connection closed.");
        };

        document.getElementById("message-form").onsubmit = function (event) {
            event.preventDefault();
            const messageInput = document.getElementById("message-input");
            const message = messageInput.value;

            if (message) {
                console.log("Sending message:", message);
                chatSocket.send(JSON.stringify({
                    'message': message
                }));
                messageInput.value = "";
            }
        };
    }

    const roomName = document.body.getAttribute('room-name-data');
    if (roomName) {
        connectToRoom(roomName);
    }
});
