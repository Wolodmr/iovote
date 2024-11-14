document.addEventListener("DOMContentLoaded", () => {
    const chatLog = document.getElementById("chat-log");
    const chatForm = document.getElementById("message-form");
    const messageInput = document.getElementById("message-input");

    // Check if elements exist before setting onsubmit
    if (!chatForm || !messageInput) {
        console.error("Form or input element not found");
        return;
    }

    // Create WebSocket connection
    const socket = new WebSocket("ws://" + window.location.host + "/ws/chat/main_room/");

    socket.onopen = function () {
        console.log("WebSocket connection established");
    };

    socket.onmessage = function (event) {
        const data = JSON.parse(event.data);
        const messageElement = document.createElement("p");
        if (data.message_type === "notification") {
            messageElement.style.fontStyle = "italic";
            messageElement.style.color = "gray";
        }
        messageElement.textContent = data.message;
        chatLog.appendChild(messageElement);
    };

    socket.onerror = function (error) {
        console.error("WebSocket error: ", error);
        const errorMessage = document.createElement("p");
        errorMessage.textContent = "An error occurred with the WebSocket connection.";
        errorMessage.style.color = "red";
        chatLog.appendChild(errorMessage);
    };

    socket.onclose = function () {
        console.log("WebSocket connection closed");
        const closeMessage = document.createElement("p");
        closeMessage.textContent = "WebSocket connection closed.";
        closeMessage.style.color = "red";
        chatLog.appendChild(closeMessage);
    };

    // Send message on form submit
    chatForm.onsubmit = function (event) {
        event.preventDefault();
        const message = messageInput.value;

        if (message.trim() !== "") {
            socket.send(JSON.stringify({ message: message }));
            messageInput.value = "";  // Clear input field after sending
        }
    };
});
