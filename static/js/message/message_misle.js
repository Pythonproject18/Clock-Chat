// Scroll to bottom of messages container
function scrollToBottom() {
    const messagesContainer = document.getElementById('messagesContainer');
    if (messagesContainer) {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
}


function open_action_popup(messageId){
    // First, close all currently open action menus
    const openMenus = document.querySelectorAll(".message-actions-menu");
    openMenus.forEach(menu => {
        menu.style.display = "none";
    });

    // Then open the one for the clicked message
    let modal = document.getElementById(`actions_menu_${messageId}`);
    if (modal) {
        modal.style.display = "block";
    } else {
        console.error("Modal not found for message ID:", messageId);
    }
}




document.addEventListener("click", function(event) {
    // Check if the click is NOT on a message-actions or actions menu
    if (!event.target.closest(".message-actions") && !event.target.closest(".message-actions-menu")) {
        const openMenus = document.querySelectorAll(".message-actions-menu");
        openMenus.forEach(menu => {
            menu.style.display = "none";
        });
    }
});


function createEmojiPopup(messageId, triggerElement) {
    const existingPopup = document.getElementById('emojiPopup');
    if (existingPopup) existingPopup.remove();

    const popup = document.createElement('div');
    popup.id = 'emojiPopup';
    popup.className = 'emoji-popup';

    allEmojis.forEach(emoji => {
        const emojiButton = document.createElement('button');
        emojiButton.innerHTML = emoji.value;
        emojiButton.title = emoji.name;
        emojiButton.addEventListener('click', () => {
            reactToMessage(messageId, emoji.id);
            popup.remove();
        });
        popup.appendChild(emojiButton);
    });

    document.body.appendChild(popup);

    const rect = triggerElement.getBoundingClientRect();
    popup.style.left = `${rect.left + window.scrollX}px`;
    popup.style.top = `${rect.top + window.scrollY - popup.offsetHeight - 10}px`;    

    // Click outside to close
    setTimeout(() => {
        document.addEventListener('click', function closePopup(e) {
            if (!popup.contains(e.target) && e.target !== triggerElement) {
                popup.remove();
                document.removeEventListener('click', closePopup);
            }
        });
    }, 0);
}



function toggleReplyMenu(messageId) {
    // Close all others first
    document.querySelectorAll(".reply-modal").forEach(modal => modal.style.display = "none");
    
    const modal = document.getElementById(`reply-modal-${messageId}`);
    if (modal) {
        modal.style.display = "block";
    }

    // Optional: Close on outside click
    setTimeout(() => {
        document.addEventListener('click', function closeReplyPopup(e) {
            if (!e.target.closest('.reply-modal') && !e.target.closest('.message-arrow-down')) {
                modal.style.display = "none";
                document.removeEventListener('click', closeReplyPopup);
            }
        });
    }, 0);
}


function showReplyPreview(msgId, text, senderName) {
    removeReplyPreview();
    replyToMessageId = msgId;

    const chatInput = document.querySelector('.chat-input');
    const previewHtml = `
        <div class="edit-preview" id="replyPreview">
            <div class="edit-preview-text">
                <i class="fas fa-reply" style="margin-right: 8px; color: var(--secondary-color);"></i>
                <strong>${senderName}</strong> : ${text}
            </div>
            <div class="edit-preview-close" onclick="cancelReply()">
                <i class="fas fa-times"></i>
            </div>
        </div>
    `;
    chatInput.insertAdjacentHTML('beforebegin', previewHtml);
}


function removeReplyPreview() {
    document.getElementById('replyPreview')?.remove();
    replyToMessageId = null;
}
function cancelReply() {
    removeReplyPreview();
}


function replyToMessage(msgId, text, senderName) {
    showReplyPreview(msgId, text, senderName);
    document.getElementById('messageInput').focus();
}





//msg seen create
function markMessagesAsSeen(messageIds) {
    fetch('/message/seen/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ message_ids: messageIds })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'success') {
            console.log('Messages marked as seen.');
        } else {
            console.error('Failed to mark messages as seen');
        }
    })
    .catch(err => console.error(err));
}