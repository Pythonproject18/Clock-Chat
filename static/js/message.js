function loadChatMessages(chatId, chatTitle) {
    fetch(`/message/${chatId}`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'success') {
            renderMessages(chatId, chatTitle, data.messages);
        } else {
            console.error('Failed to load messages:', data.message);
        }
    })
    .catch(err => console.error(err));
}

function renderMessages(chatId, chatTitle, messages) {
    const chatSection = document.getElementById('chatSection');
    const userId = document.body.dataset.userId;

    // Show chat section
    chatSection.classList.remove('hidden');

    // Set header content
    document.getElementById('chatHeader').innerHTML = `
        <div class="chat-header-avatar">${chatTitle[0]}</div>
        <div class="chat-header-info">
            <h2>${chatTitle}</h2>
            <p>Last seen today at ${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</p>
        </div>
        <div class="chat-header-actions">
            <span class="icon"><i class="fas fa-phone-alt"></i></span>
            <span class="icon"><i class="fas fa-video"></i></span>
            <span class="icon"><i class="fas fa-ellipsis-v"></i></span>
        </div>
    `;

    // Set messages
    const messagesContainer = document.getElementById('messagesContainer');
    messagesContainer.innerHTML = ''; // Clear old messages

    messages.forEach(msg => {
        const isSender = String(msg.sender_id) === String(userId);
        const messageClass = isSender ? 'sent' : 'received';
        const avatar = isSender ? '' : `<div class="message-avatar">${msg.sender_name[0]}</div>`;

        const messageHtml = `
            <div class="message ${messageClass}">
                ${avatar}
                <div class="message-content">
                    <div class="message-bubble">${msg.text}</div>
                    <div class="message-time">${msg.created_at}</div>
                </div>
            </div>
        `;

        messagesContainer.insertAdjacentHTML('beforeend', messageHtml);
    });

    // Set input box
    document.getElementById('chatInput').innerHTML = `
        <input type="text" id="messageInput" placeholder="Type a message..." />
        <input type="hidden" id="chatId" value="${chatId}" />
        <input type="hidden" id="csrfToken" value="{{ csrf_token }}">

        <span class="icon mic-icon" id="micIcon"><i class="fas fa-microphone"></i></span>
        <span class="icon plus-icon" id="plusIcon"><i class="fas fa-plus"></i></span>
        <span class="icon send-icon" onclick="sendMessage()" id="sendIcon">
            <i class="fas fa-paper-plane"></i>
        </span>
    `;
}


// Utility to get CSRF token from cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

window.sendMessage = function () {
    const messageInput = document.getElementById("messageInput");
    const chatId = document.getElementById("chatId")?.value;
    const messagesContainer = document.getElementById("messagesContainer");

    const messageText = messageInput.value.trim();
    if (!messageText) return;

    const csrfToken = getCookie("csrftoken");

    fetch(`/message/create/${chatId}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": csrfToken,
        },
        body: new URLSearchParams({
            chat_id: chatId,
            message_text: messageText,
        }),
    })
    .then((response) => {
        if (!response.ok) throw new Error("Failed to send message");
        return response.json();
    })
    .then((data) => {
        if (data.status === "success") {
            const messageDiv = document.createElement("div");
            messageDiv.className = "message sent";
            messageDiv.innerHTML = `
                <div class="message-content">
                    <div class="message-bubble">${data.data.text}</div>
                    <div class="message-time">${new Date().toLocaleTimeString("en-IN", { hour: '2-digit', minute: '2-digit' })}</div>
                </div>
            `;
            messagesContainer.appendChild(messageDiv);
            messageInput.value = "";
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
    })
    .catch((error) => console.error("Error:", error));
};
