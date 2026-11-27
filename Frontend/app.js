const API_URL = "http://127.0.0.1:8000";


// ==============================
// Upload PDF
// ==============================

document
    .getElementById("pdfFile")
    .addEventListener("change", uploadPDF);


async function uploadPDF(event) {

    const file = event.target.files[0];

    if (!file) {
        return;
    }

    const status = document.getElementById("uploadStatus");

    status.textContent = "Uploading and indexing...";

    const formData = new FormData();

    formData.append("file", file);


    try {

        const response = await fetch(
            `${API_URL}/upload-pdf`,
            {
                method: "POST",
                body: formData
            }
        );


        if (!response.ok) {
            throw new Error("Upload failed");
        }


        const data = await response.json();


        status.textContent =
            `${data.filename} indexed successfully (${data.documents} chunks)`;


    } catch (error) {

        console.error(error);

        status.textContent =
            "Upload failed. Is the FastAPI server running?";

    }

}


// ==============================
// Ask Question
// ==============================

async function askQuestion() {

    const input = document.getElementById("question");

    const question = input.value.trim();


    if (!question) {
        return;
    }


    addMessage(
        question,
        "user-message"
    );


    input.value = "";


    const loading = addMessage(
        "ForensiQ is searching the documents...",
        "ai-message"
    );


    try {

        const response = await fetch(
            `${API_URL}/ask`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    question: question
                })
            }
        );


        if (!response.ok) {
            throw new Error("Request failed");
        }


        const data = await response.json();


        loading.remove();


        addAIResponse(data);


    } catch (error) {

        console.error(error);

        loading.textContent =
            "Something went wrong while contacting ForensiQ.";

    }

}


// ==============================
// Add user message
// ==============================

function addMessage(text, className) {

    const chat = document.getElementById("chat");


    const message = document.createElement("div");

    message.className =
        `message ${className}`;


    message.textContent = text;


    chat.appendChild(message);


    chat.scrollTop = chat.scrollHeight;


    return message;

}


// ==============================
// Add AI response
// ==============================

function addAIResponse(data) {

    const chat = document.getElementById("chat");


    const message = document.createElement("div");

    message.className =
        "message ai-message";


    const answer = document.createElement("div");

    answer.textContent =
        data.answer;


    message.appendChild(answer);


    if (
        data.sources &&
        data.sources.length > 0
    ) {

        const sources =
            document.createElement("div");

        sources.className =
            "sources";


        const title =
            document.createElement("strong");

        title.textContent =
            "Sources";


        sources.appendChild(title);


        data.sources.forEach(source => {

            const item =
                document.createElement("div");

            item.className =
                "source-item";


            item.textContent =
                `Page ${source.page} — similarity ${source.similarity}`;


            sources.appendChild(item);

        });


        message.appendChild(sources);

    }


    chat.appendChild(message);


    chat.scrollTop =
        chat.scrollHeight;

}


// ==============================
// Example questions
// ==============================

function useExample(question) {

    document.getElementById("question").value =
        question;

}


// ==============================
// Enter key
// ==============================

function handleEnter(event) {

    if (event.key === "Enter") {

        askQuestion();

    }

}