// Event listener for edit message

document.addEventListener("click", function (e) {
    if (e.target.classList.contains("message-action-edit")) {
        const messageElement = e.target.closest(".message");
        const messageBubble = messageElement.querySelector(".message-bubble");
        const messageId = messageElement.dataset.messageId;

        editingMessageId = messageId;

        const rawText = messageBubble.childNodes[0].nodeValue.trim();
        messageInput.value = rawText;
        messageInput.focus();
        
        // Show edit preview
        showEditPreview(rawText);
        

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



let editingMessageId = null;

let allEmojis = [];

let replyToMessageId = null;

// Edit Preview Functions
function showEditPreview(text) {
    removeEditPreview();
    const chatInput = document.querySelector('.chat-input');
    const previewHtml = `
        <div class="edit-preview" id="editPreview">
            <div class="edit-preview-text">
                <i class="fas fa-edit" style="margin-right: 8px; color: var(--secondary-color);"></i>
                Editing: ${text}
            </div>
            <div class="edit-preview-close" onclick="cancelEdit()">
                <i class="fas fa-times"></i>
            </div>
        </div>
    `;
    chatInput.insertAdjacentHTML('beforebegin', previewHtml);
    document.getElementById('chatInput').classList.add('editing-mode');
}

function removeEditPreview() {
    const existingPreview = document.getElementById('editPreview');
    if (existingPreview) {
        existingPreview.remove();
    }
    document.getElementById('chatInput').classList.remove('editing-mode');
}

function cancelEdit() {
    removeEditPreview();
    resetInput();
}