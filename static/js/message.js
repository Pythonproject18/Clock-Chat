<<<<<<< HEAD
=======
function scrollToBottom() {
    const messagesContainer = document.getElementById('messagesContainer');
    if (messagesContainer) {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
}

let editingMessageId = null;

>>>>>>> 8620c48bb0c63c9b535cce97d2dde7d5ddfcb31b
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

<<<<<<< HEAD
    let html = `
        <div class="chat-header">
            <div class="chat-header-avatar">${chatTitle[0]}</div>
            <div class="chat-header-info">
                <h2>${chatTitle}</h2>
                <p>Last seen today at ${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</p>
            </div>
            <div class="chat-header-actions">
                <span class="icon"><i class="fas fa-phone-alt"></i></span>
                <span class="icon"><i class="fas fa-video"></i></span>
                <span class="icon"><i class="fas fa-ellipsis-v"></i></span>
            </div>
=======
    chatSection.classList.remove('hidden');

    document.getElementById('chatHeader').innerHTML = `
        <div class="chat-header-avatar">${chatTitle[0]}</div>
        <div class="chat-header-info">
            <h2>${chatTitle}</h2>
            <p>Last seen today at ${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</p>
>>>>>>> 8620c48bb0c63c9b535cce97d2dde7d5ddfcb31b
        </div>

<<<<<<< HEAD
        <div class="chat-messages" id="messagesContainer">`;
=======
    const messagesContainer = document.getElementById('messagesContainer');
    messagesContainer.innerHTML = '';
>>>>>>> 8620c48bb0c63c9b535cce97d2dde7d5ddfcb31b

    messages.forEach(msg => {
        const isSender = String(msg.sender_id) === String(userId);
        const messageClass = isSender ? 'sent' : 'received';
        const avatar = isSender ? '' : `<div class="message-avatar">${msg.sender_name[0]}</div>`;
<<<<<<< HEAD
        html += `
            <div class="message ${messageClass}">
                ${avatar}
                <div class="message-content">
                    <div class="message-bubble">${msg.text}</div>
                    <div class="message-time">${msg.created_at}</div>
                </div>
            </div>
        `;
    });

    html += `</div>
        <div class="chat-input">
            <input type="text" id="messageInput" placeholder="Type a message..." />
            <input type="hidden" id="chatId" value="${chatId}" />
            <input type="hidden" id="csrfToken" value="{{ csrf_token }}">

            <span class="icon mic-icon" id="micIcon"><i class="fas fa-microphone"></i></span>
            <span class="icon plus-icon" id="plusIcon"><i class="fas fa-plus"></i></span>
            <span class="icon send-icon" onclick="sendMessage()" id="sendIcon">
                <i class="fas fa-paper-plane"></i>
            </span>
        </div>
    `;

    chatSection.innerHTML = html;
}

// Utility to get CSRF token from cookie
=======

        const messageHtml = `
        <div class="message ${messageClass}" data-message-id="${msg.id}">
            ${avatar}
            <div class="message-content">
                <div class="message-bubble">${msg.text}</div>
                <div class="message-time">${msg.created_at}</div>
            </div>
            ${isSender ? `
            <div class="message-actions">
                <div class="message-actions-dots">
                    <div class="message-actions-dot"></div>
                    <div class="message-actions-dot"></div>
                    <div class="message-actions-dot"></div>
                </div>
                <div class="message-actions-menu">
                    <div class="message-action-edit">Edit</div>
                    <div class="message-action-delete" onclick="open_deletemodal('${msg.id}')">Delete</div>
                </div>
            </div>` : '<div class="message-emoji-container"><i class="far fa-smile message-emoji"></i></div>'}
        </div>
        



            <div class="message-action-delete" id="deletemodal-${msg.id}" style="display: none;">
                <div class="modal-dialog">
                    <div class="modal-content" id="modalcontent">
                        <div class="modal-header">
                            <h5 class="modal-title">Are you want to delete it?</h5>
                            <i class="fas fa-times" onclick="close_deletemodal('${msg.id}')" style="position: absolute; right: 4%; top: 4%; cursor: pointer;"></i> 
                        </div>
                        <div class="modal-body" style="gap: 10px; flex-direction: column; display: flex;">
                            <div class="button" style="background:rgba(0, 0, 0, 0.2);" onclick="delete_for_me('${msg.id}')">Delete for me</div>
                            <div class="button" style="background:rgba(0, 0, 0, 0.2);" onclick="delete_for_everyone('${msg.id}')">Delete for everyone</div>
                            <div class="button" style="background: #ff000000;" onclick="close_deletemodal('${msg.id}')">Cancel</div>
                        </div>
                    </div>
                </div>
            </div>

    `;
    
        messagesContainer.insertAdjacentHTML('beforeend', messageHtml);
    });

    document.getElementById('chatInput').innerHTML = `
        <input type="text" id="messageInput" placeholder="Type a message..." />
        <input type="hidden" id="chatId" value="${chatId}" />
        <input type="hidden" id="csrfToken" value="{{ csrf_token }}">

        <span class="icon mic-icon" id="micIcon"><i class="fas fa-microphone"></i></span>
        <span class="icon plus-icon" id="plusIcon"><i class="fas fa-plus"></i></span>
        <span class="icon send-icon" onclick="sendMessage()" id="sendIcon" style="display:none;">
            <i class="fas fa-paper-plane" id="sendPlaneIcon"></i>
            <i class="fas fa-check" id="sendCheckIcon" style="display:none;"></i>
        </span>
    `;

    setTimeout(scrollToBottom, 0);

    const messageInput = document.getElementById('messageInput');
    const micIcon = document.getElementById('micIcon');
    const plusIcon = document.getElementById('plusIcon');
    const sendIcon = document.getElementById('sendIcon');

    messageInput.addEventListener('input', function () {
        if (this.value.trim() !== '') {
            sendIcon.style.display = 'inline-block';
            micIcon.style.display = 'none';
            plusIcon.style.display = 'none';
        } else {
            sendIcon.style.display = 'none';
            micIcon.style.display = 'inline-block';
            plusIcon.style.display = 'inline-block';
        }
    });

    messageInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter' && this.value.trim() !== '') {
            sendMessage();
        }
    });
}

>>>>>>> 8620c48bb0c63c9b535cce97d2dde7d5ddfcb31b
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
<<<<<<< HEAD
=======
    const micIcon = document.getElementById("micIcon");
    const plusIcon = document.getElementById("plusIcon");
    const sendIcon = document.getElementById("sendIcon");
    const sendPlaneIcon = document.getElementById("sendPlaneIcon");
    const sendCheckIcon = document.getElementById("sendCheckIcon");
>>>>>>> 8620c48bb0c63c9b535cce97d2dde7d5ddfcb31b

    const messageText = messageInput.value.trim();
    if (!messageText) return;

    const csrfToken = getCookie("csrftoken");

    if (editingMessageId) {
        fetch(`/message/update/${editingMessageId}`, {
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
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                const messageElement = messagesContainer.querySelector(`.message[data-message-id='${editingMessageId}']`);
                if (messageElement) {
                    messageElement.querySelector(".message-bubble").innerText = data.data.text;
                }
                resetInput();
            } else {
                console.error(data.message);
            }
        })
        .catch(error => console.error("Edit error:", error));
    } else {
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
                messageDiv.dataset.messageId = data.data.id;
                messageDiv.innerHTML = `
                    <div class="message-content">
                        <div class="message-bubble">${data.data.text}</div>
                        <div class="message-time">${new Date().toLocaleTimeString("en-IN", { hour: '2-digit', minute: '2-digit' })}</div>
                    </div>
                    <div class="message-actions">
                        <div class="message-actions-dots">
                            <div class="message-actions-dot"></div>
                            <div class="message-actions-dot"></div>
                            <div class="message-actions-dot"></div>
                        </div>
                        <div class="message-actions-menu">
                            <div class="message-action-edit">Edit</div>
                            <div class="message-action-delete" onclick="open_deletemodal('${data.data.id}')">Delete</div>
                        </div>
                    </div>


                    <div class="message-action-delete" id="deletemodal-${data.data.id}" style="display: none;">
                        <div class="modal-dialog">
                            <div class="modal-content" id="modalcontent" style="position:fixed !important;left:70%!important;">
                                <div class="modal-header">
                                    <h5 class="modal-title">Are you want to delete it?</h5>
                                    <i class="fas fa-times" onclick="close_deletemodal('${data.data.id}')" style="position: absolute; right: 4%; top: 4%; cursor: pointer;"></i> 
                                </div>
                                <div class="modal-body" style="gap: 10px; flex-direction: column; display: flex;">
                                    <div class="button" style="background:rgba(0, 0, 0, 0.2);" onclick="delete_for_me('${data.data.id}')">Delete for me</div>
                                    <div class="button" style="background:rgba(0, 0, 0, 0.2);" onclick="delete_for_everyone('${data.data.id}')">Delete for everyone</div>
                                    <div class="button" style="background: #ff000000;" onclick="close_deletemodal('${data.data.id}')">Cancel</div>
                                </div>
                            </div>
                        </div>
                    </div>

                `;
                messagesContainer.appendChild(messageDiv);
                resetInput();
                scrollToBottom();
            }
        })
        .catch((error) => console.error("Error:", error));
    }
};

function resetInput() {
    const messageInput = document.getElementById("messageInput");
    const micIcon = document.getElementById("micIcon");
    const plusIcon = document.getElementById("plusIcon");
    const sendIcon = document.getElementById("sendIcon");
    const sendPlaneIcon = document.getElementById("sendPlaneIcon");
    const sendCheckIcon = document.getElementById("sendCheckIcon");

    messageInput.value = "";
    editingMessageId = null;

    sendIcon.style.display = "none";
    sendPlaneIcon.style.display = "inline";
    sendCheckIcon.style.display = "none";
    micIcon.style.display = "inline-block";
    plusIcon.style.display = "inline-block";
}

document.addEventListener("click", function (e) {
    if (e.target.classList.contains("message-action-edit")) {
        const messageElement = e.target.closest(".message");
        const messageBubble = messageElement.querySelector(".message-bubble");
        const messageId = messageElement.dataset.messageId;

        editingMessageId = messageId;

        const messageInput = document.getElementById("messageInput");
        messageInput.value = messageBubble.innerText;
        messageInput.focus();

        const sendIcon = document.getElementById("sendIcon");
        const micIcon = document.getElementById("micIcon");
        const plusIcon = document.getElementById("plusIcon");
        const sendPlaneIcon = document.getElementById("sendPlaneIcon");
        const sendCheckIcon = document.getElementById("sendCheckIcon");

        sendIcon.style.display = "inline-block";
        micIcon.style.display = "none";
        plusIcon.style.display = "none";
        sendPlaneIcon.style.display = "none";
        sendCheckIcon.style.display = "inline";
    }
});


  function open_deletemodal(msgId) {
    const modal = document.getElementById(`deletemodal-${msgId}`);
    if (modal) {
      modal.style.display = "block";
    }
  }

  function close_deletemodal(msgId) {
    const modal = document.getElementById(`deletemodal-${msgId}`);
    if (modal) {
      modal.style.display = "none";
    }
  }

  function delete_for_me(msgId) {
    console.log(`Deleting message ${msgId} for me...`);
    let purpose = "delete for me";
    delete_msg(msgId,purpose);
    close_deletemodal(msgId);
  }

  function delete_for_everyone(msgId) {
    let purpose = "delete for everyone";
    delete_msg(msgId,purpose);
    console.log(`Deleting message ${msgId} for everyone...`);
    close_deletemodal(msgId);
  }

  function delete_msg(msgId, purpose) {
    fetch(`/message/delete/${msgId}`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),  // Using getCookie here instead
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ purpose: purpose })
    })
<<<<<<< HEAD
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
=======
    .then(response => {
        if (response.ok) {
            console.log(`Message ${msgId} deleted (${purpose})`);
            // Select the element by data-message-id and remove it
            const msgElement = document.querySelector(`.message[data-message-id="${msgId}"]`);
            if (msgElement) {
                msgElement.remove();
            }
            close_deletemodal(msgId);
        } else {
            response.json().then(data => console.error(data));
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
>>>>>>> 8620c48bb0c63c9b535cce97d2dde7d5ddfcb31b
