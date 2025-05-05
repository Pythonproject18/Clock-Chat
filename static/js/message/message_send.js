//message send
window.sendMessage = function () {
    const messageInput = document.getElementById("messageInput");
    const chatId = document.getElementById("chatId")?.value;
    const messagesContainer = document.getElementById("messagesContainer");
    
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
                    let editedLabel = '';
                    if (data.data.is_edited) {
                        editedLabel = '<span style="font-size:11px; color:var(--text-light); display:inline-block; margin-left:6px;">edited</span>';
                    }
                    messageElement.querySelector(".message-bubble").innerHTML = `${data.data.text}${editedLabel}`;                    
                }                
                resetInput();
                removeEditPreview();
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
                reply_to: replyToMessageId || ''
            }),
        })
        .then((response) => {
            if (!response.ok) throw new Error("Failed to send message");
            return response.json();
        })
        .then((data) => {
            if (data.status === "success") {
                const isSender = true;
                const messageClass = isSender ? 'sent' : 'received';
                const replyText = document.querySelector('#replyPreview .edit-preview-text')?.textContent?.split(':')?.slice(1)?.join(':')?.trim() || '';
                const replyHtml = replyToMessageId && replyText ? `
                    <div class="reply-snippet">
                        ${replyText.length > 50 ? replyText.slice(0, 50) + '…' : replyText}
                    </div>
                ` : '';

                const messageDiv = document.createElement("div");
                messageDiv.className = `message ${messageClass}`;
                messageDiv.dataset.messageId = data.data.id;

                messageDiv.innerHTML = `
                    <div class="message-content">
                        <div class="message-bubble">
                            ${replyHtml}
                            ${data.data.text}
                        </div>
                        <div class="message-time">
                            ${new Date().toLocaleTimeString("en-IN", { hour: '2-digit', minute: '2-digit' })}
                            <i class="fas fa-check" style="margin-left: 6px; font-size: 10px; color: var(--text-light);"></i>
                        </div>
                    </div>
                    <div class="message-actions" onclick="open_action_popup('${data.data.id}')" style="left: 0px !important;right: auto;">
                        <div class="message-actions-dots">
                            <div class="message-actions-dot"></div>
                            <div class="message-actions-dot"></div>
                            <div class="message-actions-dot"></div>
                        </div>
                    </div>
                    <div class="message-actions-menu action-popup" id="actions_menu_${data.data.id}" style="display:none;">
                        <div class="message-action-edit">Edit</div>
                        <div class="message-action-delete" onclick="open_deletemodal('${data.data.id}')">Delete</div>
                        <div class="reply-modal-option" onclick="replyToMessage('${data.data.id}', \`${data.data.Text}\`, '${data.data.sender_name}')">Reply</div>
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
                removeEditPreview();
                scrollToBottom();
                removeReplyPreview();
            }
        })
        .catch((error) => console.error("Error:", error));
    }
};


// Reset input field
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