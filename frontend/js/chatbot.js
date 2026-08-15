async function sendMessage() {

    const input = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");

    const question = input.value.trim();

    if (question === "") {
        return;
    }

    // Display user's message
    const userMessage = document.createElement("div");

    userMessage.classList.add("message", "user-message");

    userMessage.textContent = question;

    chatBox.appendChild(userMessage);

    // Clear input
    input.value = "";

    try {

        const response = await fetch("http://127.0.0.1:5000/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })

        });

        const data = await response.json();

        // Display bot response
        const botMessage = document.createElement("div");

        botMessage.classList.add("message", "bot-message");

        botMessage.textContent = data.answer;

        chatBox.appendChild(botMessage);

        // Scroll to latest message
        chatBox.scrollTop = chatBox.scrollHeight;

    } catch (error) {

        console.error(error);

        const errorMessage = document.createElement("div");

        errorMessage.classList.add("message", "bot-message");

        errorMessage.textContent =
            "Sorry, I couldn't connect to the server.";

        chatBox.appendChild(errorMessage);
    }
}