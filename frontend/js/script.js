// ========================================
// GET HTML ELEMENTS
// ========================================

const chatInput = document.getElementById("chat-input");
const sendButton = document.getElementById("send-button");
const chatMessages = document.getElementById("chat-messages");
const clearButton = document.getElementById("clear-button");


// ========================================
// ADD MESSAGE
// ========================================

function addMessage(message, sender) {

    const messageElement = document.createElement("div");

    messageElement.classList.add(
        "message",
        sender
    );


    const textElement = document.createElement("div");

    textElement.textContent = message;


    const timeElement = document.createElement("div");

    const now = new Date();

    timeElement.textContent =
        now.toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit"
        });

    timeElement.classList.add(
        "message-time"
    );


    messageElement.appendChild(textElement);

    messageElement.appendChild(timeElement);


    chatMessages.appendChild(
        messageElement
    );


    chatMessages.scrollTop =
        chatMessages.scrollHeight;
}


// ========================================
// SEND MESSAGE
// ========================================

async function sendMessage() {

    const question =
        chatInput.value.trim();


    // Don't send empty messages

    if (!question) {
        return;
    }


    // Show user question

    addMessage(
        question,
        "user"
    );


    // Clear input

    chatInput.value = "";


    // Disable send button

    sendButton.disabled = true;


    // Create thinking message

    const loadingMessage =
        document.createElement("div");

    loadingMessage.classList.add(
        "message",
        "bot"
    );


    loadingMessage.innerHTML = `
        <div class="typing">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;


    chatMessages.appendChild(
        loadingMessage
    );


    chatMessages.scrollTop =
        chatMessages.scrollHeight;


    try {

        // Send request to Flask

        const response = await fetch(
            "http://127.0.0.1:5000/chat",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    question: question
                })
            }
        );


        const data =
            await response.json();


        // Remove thinking message

        loadingMessage.remove();


        // Check response

        if (response.ok) {

            // Show answer

            addMessage(
                data.answer,
                "bot"
            );


            // Show source

           if (data.source) {

    const sourceElement =
        document.createElement("div");

    sourceElement.classList.add(
        "message",
        "source"
    );

    sourceElement.textContent =
        "📄 Source: " + data.source;

    chatMessages.appendChild(
        sourceElement
    );

}

        } else {

            addMessage(
                data.error ||
                "Something went wrong.",
                "bot"
            );

        }


    } catch (error) {

        console.error(
            "Chatbot error:",
            error
        );


        loadingMessage.remove();


        addMessage(
            "Unable to connect to the chatbot server. Make sure Flask is running.",
            "bot"
        );

    }


    // Enable send button again

    sendButton.disabled = false;
}


// ========================================
// SEND BUTTON
// ========================================

sendButton.addEventListener(
    "click",
    sendMessage
);


// ========================================
// ENTER KEY
// ========================================

chatInput.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {

            event.preventDefault();

            sendMessage();

        }

    }
);


// ========================================
// SUGGESTED QUESTIONS
// ========================================

function askQuestion(question) {

    // Put question inside textbox

    chatInput.value = question;


    // Send it

    sendMessage();

}


// ========================================
// CLEAR CHAT
// ========================================

if (clearButton) {

    clearButton.addEventListener(
        "click",
        function() {

            chatMessages.innerHTML = `
                <div class="message bot">
                    Hello! 👋
                    <br><br>
                    I'm your Student Support Assistant.
                    Ask me about attendance, exams,
                    scholarships, library services,
                    and other student-related information.
                </div>
            `;


            chatInput.value = "";

            chatInput.focus();

        }
    );

}