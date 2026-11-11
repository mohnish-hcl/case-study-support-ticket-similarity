let datasetLoaded = false;

// =====================================
// HELPERS
// =====================================

function scrollToBottom() {
    const chat = document.getElementById("chat-window");
    chat.scrollTop = chat.scrollHeight;
}

function getMessageBox() {
    return document.getElementById("message");
}

// =====================================
// INIT
// =====================================

window.onload = () => {
    const fileInput = document.getElementById("ticket-file");

    fileInput.addEventListener("change", () => {
        if (fileInput.files.length > 0) {
            document.getElementById("file-name").innerHTML = fileInput.files[0].name;
        }
    });

    const textarea = getMessageBox();

    textarea.addEventListener("keydown", function(event) {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
        }
    });
};

// =====================================
// DATASET UPLOAD
// =====================================

async function uploadFile() {
    const fileInput = document.getElementById("ticket-file");

    if (fileInput.files.length === 0) {
        alert("Please select tickets.json");
        return;
    }

    const uploadStatus = document.getElementById("upload-status");
    const appStatus = document.getElementById("app-status");

    uploadStatus.innerHTML = "⏳ Building vector index...";

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {
        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        const result = await response.json();
        datasetLoaded = true;

        document.getElementById("chat-btn").disabled = false;

        const messageBox = getMessageBox();
        messageBox.disabled = false;
        messageBox.value = "";
        messageBox.placeholder = "Provide the Ticket details and get related tickets";

        appStatus.innerHTML = "✅ Search Ready";

        uploadStatus.innerHTML = `
        <div class="dataset-ready">
            <strong>✅ Dataset Ready</strong><br><br>
            <strong>File</strong><br>
            ${fileInput.files[0].name}<br><br>
            <strong>Tickets Indexed</strong><br>
            ${result.count}
        </div>
        `;

        document.getElementById("stats-card").classList.remove("hidden");

        document.getElementById("ticket-count").innerHTML = `
            <div class="model-info">
                <strong>Status</strong><br>
                ✅ Ready<br><br>
                <strong>File</strong><br>
                ${fileInput.files[0].name}<br><br>
                <strong>Tickets Indexed</strong><br>
                ${result.count}<br><br>
                <strong>Embedding Model</strong><br>
                nomic-embed-text<br><br>
                <strong>LLM</strong><br>
                phi4-mini<br><br>
                <strong>Confidence Threshold</strong><br>
                70%
            </div>
        `;
    } catch(error) {
        console.error(error);
        document.getElementById("app-status").innerHTML = "❌ Upload Failed";
        uploadStatus.innerHTML = "❌ Upload Failed";
    }
}

// =====================================
// CHAT
// =====================================

async function sendMessage() {
    if (!datasetLoaded) {
        alert("Please upload a dataset first.");
        return;
    }

    const textarea = getMessageBox();
    const query = textarea.value.trim();

    if (!query) {
        return;
    }

    const chat = document.getElementById("chat-window");

    // USER MESSAGE
    chat.innerHTML += `
    <div class="user-row">
        <div class="user-bubble">${query}</div>
        <div class="avatar">👤</div>
    </div>
    `;

    textarea.value = "";
    const placeholderId = `msg-${Date.now()}`;

    // ASSISTANT LOADER
    chat.innerHTML += `
    <div class="assistant-row" id="${placeholderId}">
        <div class="avatar">🤖</div>
        <div class="assistant-bubble">
            <div class="typing-loader">
                <span></span>
                <span></span>
                <span></span>
            </div>
            Searching historical tickets...
        </div>
    </div>
    `;

    scrollToBottom();

    try {
        const response = await fetch("/search", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: query })
        });

        const data = await response.json();
        const placeholder = document.getElementById(placeholderId);

        // CHAT MODE
        if (data.status === "CHAT") {
            placeholder.innerHTML = `
            <div class="avatar">🤖</div>
            <div class="assistant-bubble">${data.response}</div>
            `;
            scrollToBottom();
            return;
        }

        // NO MATCH
        if (data.status === "NO_MATCH") {
            placeholder.innerHTML = `
            <div class="avatar">🤖</div>
            <div class="assistant-bubble">${data.message}</div>
            `;
            scrollToBottom();
            return;
        }

        // MATCHES
        let ticketCards = "";

        data.matches.forEach(ticket => {
            ticketCards += `
            <div class="match-card">
                <div class="ticket-top">
                    <strong>${ticket.ticket_id}</strong>
                    <span class="confidence-pill">${ticket.confidence}%</span>
                </div>
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width:${ticket.confidence}%"></div>
                </div>
                <div class="ticket-section">
                    <div class="ticket-label">Subject</div>
                    <div class="ticket-value">${ticket.subject}</div>
                </div>
                <div class="ticket-section">
                    <div class="ticket-label">Description</div>
                    <div class="ticket-value">${ticket.description}</div>
                </div>
                <div class="ticket-section">
                    <div class="ticket-label">Category</div>
                    <div class="ticket-value">${ticket.category}</div>
                </div>
                <div class="ticket-section">
                    <div class="ticket-label">Tags</div>
                    <div class="ticket-value">${ticket.tags}</div>
                </div>
                <div class="ticket-section">
                    <div class="ticket-label">Resolution</div>
                    <div class="ticket-value">${ticket.resolution}</div>
                </div>
            </div>
            `;
        });

        placeholder.innerHTML = `
        <div class="avatar">🤖</div>
        <div class="assistant-bubble">
            <div class="recommendation">${data.llm_response}</div>
            <div class="ticket-list-header">Similar Historical Tickets</div>
            ${ticketCards}
        </div>
        `;

        scrollToBottom();
    } catch(error) {
        console.error(error);
        const placeholder = document.getElementById(placeholderId);
        if (placeholder) {
            placeholder.innerHTML = `
            <div class="avatar">🤖</div>
            <div class="assistant-bubble">Something went wrong while searching.</div>
            `;
        }
    }
}