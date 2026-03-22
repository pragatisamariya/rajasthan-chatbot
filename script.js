async function sendMessage() {
    const inputField = document.getElementById("userInput");
    const message = inputField.value.trim();

    if (message === "") return;

    addMessage(message, "user");
    inputField.value = "";

    try {
        const response = await fetch("https://lubricational-cagily-khalil.ngrok-free.dev/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();
        addMessage(data.response, "bot");

    } catch (error) {
        addMessage("Server error. Please try again later.", "bot");
        console.error(error);
    }
}

function addMessage(text, sender) {
    const chatbox = document.getElementById("chatbox");
    const messageDiv = document.createElement("div");

    messageDiv.classList.add("message", sender);
    messageDiv.innerText = text;

    chatbox.appendChild(messageDiv);
    chatbox.scrollTop = chatbox.scrollHeight;
}

document.getElementById("userInput").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});