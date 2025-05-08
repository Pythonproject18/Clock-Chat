// Load chat messages for a specific chat
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
            allEmojis = data.emojies || [];  // Store emojis for popup
        } else {
            console.error('Failed to load messages:', data.message);
        }
    })
    .catch(err => console.error(err));
}

// Render messages in the chat section
function renderMessages(chatId, chatTitle, messages) {
    const chatSection = document.getElementById('chatSection');
    const userId = document.body.dataset.userId;

    chatSection.classList.remove('hidden');

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

    const messagesContainer = document.getElementById('messagesContainer');
    messagesContainer.innerHTML = '';

    messages.forEach(msg => {
        const isSender = String(msg.sender_id) === String(userId);
        const messageClass = isSender ? 'sent' : 'received';
        const avatar = isSender ? '' : `<div class="message-avatar">${msg.sender_name[0]}</div>`;
    
    // In the renderMessages function, update the bubbleContent section to include media handling
    let bubbleContent = "";
    if (msg.text) {
        let editedLabel = msg.is_edited ? 
        (isSender 
            ? '<span style="font-size: 11px; color: var(--text-light); margin-left: 6px;">edited</span>' 
            : '<span style="font-size: 11px; color: var(--text-light); margin-right: 6px;">edited</span>'
        ) 
        : '';
        
        let replyHtml = '';
        if (msg.reply_to && msg.reply_to.text) {
            replyHtml = `
                <div class="reply-snippet">
                ${msg.reply_to.text.length > 50 
                    ? msg.reply_to.text.slice(0, 50) + '…' 
                    : msg.reply_to.text}
                </div>
            `;
        }

        bubbleContent = `
            <div class="message-bubble">
            ${replyHtml}
            ${msg.text}${editedLabel}
            </div>
        `;
    // Update the media handling section in renderMessages
} else if (msg.media_url) {
    const mediaCount = msg.media_url.length;
    bubbleContent = `<div class="media-grid media-count-${Math.min(mediaCount, 4)}">`; // Supports up to 4 items per row
    
    bubbleContent += msg.media_url.map((media, index) => {
        const isLastInRow = (index + 1) % 2 === 0 || index === mediaCount - 1;
        const marginClass = isLastInRow ? 'no-margin' : '';
        
        if (media.match(/\.(jpg|jpeg|png|gif|webp)$/i)) {
            return `<div class="media-grid-item ${marginClass}" onclick="openMediaViewer('${media}', 'image')">
                <img src="${media}" class="media-message">
                ${mediaCount > 1 ? '<div class="media-overlay"></div>' : ''}
            </div>`;
        } else if (media.match(/\.(mp4|webm|ogg|mov)$/i)) {
            return `<div class="media-grid-item ${marginClass}" onclick="openMediaViewer('${media}', 'video')">
                <video class="media-message">
                    <source src="${media}">
                </video>
                <div class="video-play-icon"><i class="fas fa-play"></i></div>
                ${mediaCount > 1 ? '<div class="media-overlay"></div>' : ''}
            </div>`;
        } else {
            return `<div class="media-grid-item ${marginClass}" onclick="openMediaViewer('${media}', 'file')">
                <div class="file-message">
                    <i class="fas fa-file-alt"></i>
                    <span>${media.split('/').pop()}</span>
                </div>
            </div>`;
        }
    }).join('');
    
    bubbleContent += '</div>';
}
        
        const messageHtml = `
        <div class="message ${messageClass}" data-message-id="${msg.id}">
            ${avatar}
            <div class="message-content">
                ${bubbleContent}
                <div class="message-time">
                ${msg.created_at}
                ${
                    isSender 
                    ? `
                    <span class="message-ticks">
                        ${
                        (msg.member_count > 2)
                        ? (msg.seen_by.length === 0)
                            ? `<i class="fas fa-check tick tick-gray single-tick"></i>`
                            : (msg.seen_by.length === msg.member_count - 1)
                            ? `<i class="fas fa-check tick tick-blue"></i>
                                <i class="fas fa-check tick tick-blue" style="left: 6px"></i>`
                            : `<i class="fas fa-check tick tick-gray"></i>
                                <i class="fas fa-check tick tick-gray" style="left: 6px"></i>`
                            : (msg.seen_by.length > 0)
                            ? `<i class="fas fa-check tick tick-blue"></i>
                                <i class="fas fa-check tick tick-blue" style="left: 6px"></i>`
                            : `<i class="fas fa-check tick tick-gray single-tick"></i>`
                        }
                    </span>`
                    : ''
                }
                </div>
                ${msg.reactions && msg.reactions.length > 0 ? `
                    <div class="emoji-reactions">
                        ${msg.reactions.map(reaction => 
                            `<span class="message-reaction ${reaction.is_current_user ? 'user-reaction' : ''}">${reaction.value}</span>`
                        ).join('')}
                    </div>` 
                : ''}
            </div>
            ${isSender ? `
                <div class="message-actions" id="actions" onclick="open_action_popup('${msg.id}')" style="left: 0px !important;right: auto;">
                    <div class="message-actions-dots">
                        <div class="message-actions-dot"></div>
                        <div class="message-actions-dot"></div>
                        <div class="message-actions-dot"></div>
                    </div>
                </div>
                <div class="message-actions-menu action-popup" id="actions_menu_${msg.id}" style="display:none;">
                    ${msg.text ? `<div class="message-action-edit">Edit</div>` : ''}
                    <div class="message-action-delete" onclick="open_deletemodal('${msg.id}')">Delete</div>
                    <div class="reply-modal-option" onclick="replyToMessage('${msg.id}', \`${msg.text}\`, '${msg.sender_name}')">Reply</div>
                </div>
                
                <div class="message-emoji-container">
                    <i class="far fa-smile message-emoji" onclick="createEmojiPopup('${msg.id}', this)"></i>
                </div>`

            : `<div class="message-actions" id="actions" onclick="open_action_popup('${msg.id}')">
                    <div class="message-actions-dots">
                        <div class="message-actions-dot"></div>
                        <div class="message-actions-dot"></div>
                        <div class="message-actions-dot"></div>
                    </div>
                </div>
                <div class="message-actions-menu action-popup" id="actions_menu_${msg.id}" style="display:none;">
                    <div class="message-action-delete" onclick="open_deletemodal('${msg.id}')">Delete</div>
                    <div class="reply-modal-option" onclick="replyToMessage('${msg.id}', \`${msg.text}\`, '${msg.sender_name}')">Reply</div>
                </div>
                
                <div class="message-emoji-container">
                    <i class="far fa-smile message-emoji" onclick="createEmojiPopup('${msg.id}', this)"></i>
                </div>
            `}

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
        
    
        document.getElementById("messagesContainer").insertAdjacentHTML("beforeend", messageHtml);
    });
    
    document.getElementById('chatInput').innerHTML = `
        <span class="icon" id="deleteBtn" style="display:none;font-size:16px;color: red;position: absolute;left: 30px;" onclick="deleteRecording()">
            <i class="fas fa-trash"></i>
        </span>

        <input type="text" id="messageInput" placeholder="Type a message..." />
        <input type="hidden" id="chatId" value="${chatId}" />
        <input type="hidden" id="csrfToken" value="{{ csrf_token }}">

       <span class="icon mic-icon" id="micIcon" onclick="startRecording()">
            <i class="fas fa-microphone"></i>
        </span>

        <span id="recordingTimer" style="display:none;font-size: 16px;right: 12%;position: absolute;">00:00</span>

        <span class="icon" id="micStop" style="display:none;font-size: 16px;right: 8%;position: absolute;" onclick="stopRecording()">
            <i class="fas fa-pause"></i>
        </span>

        <span class="icon" id="resumeBtn" style="display:none;font-size: 16px;right: 8%;position: absolute;" onclick="resumeRecording()">
            <i class="fas fa-play"></i>
        </span>

        <span class="icon" id="sendBtn" style="display:none;font-size:16px;" onclick="sendRecording()">
            <i class="fas fa-paper-plane"></i>
        </span>

        <!-- Media Upload (Plus Icon) -->
        <span class="icon plus-icon" id="plusIcon" onclick="triggerMediaInput()" style="display:block;">
            <i class="fas fa-plus"></i>
        </span>

        <!-- Send Media Button -->
        <span id="send_media" style="display:none;">
            <i class="fas fa-paper-plane send-media" id="sendMedia" onclick="sendSelectedMedia('${chatId}')"></i>
        </span>

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

// Cookie helper function
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



function openMediaViewer(mediaUrl, mediaType) {
    const mediaViewer = document.createElement('div');
    mediaViewer.className = 'media-viewer-overlay';
    
    // Create the close button first
    const closeBtn = document.createElement('div');
    closeBtn.className = 'media-viewer-close';
    closeBtn.innerHTML = '<i class="fas fa-times"></i>';
    closeBtn.onclick = () => {
        document.body.removeChild(mediaViewer);
    };

    let mediaContent = '';
    if (mediaType === 'image') {
        mediaContent = `<img src="${mediaUrl}" class="media-viewer-content">`;
    } else if (mediaType === 'video') {
        mediaContent = `
            <video controls autoplay class="media-viewer-content">
                <source src="${mediaUrl}">
                Your browser does not support the video tag.
            </video>
        `;
    } else if (mediaType === 'audio') {
        mediaContent = `
            <audio controls autoplay class="media-viewer-content">
                <source src="${mediaUrl}">
                Your browser does not support the audio element.
            </audio>
        `;
    } else {
        mediaContent = `
            <div class="file-viewer-content">
                <i class="fas fa-file-alt"></i>
                <span>${mediaUrl.split('/').pop()}</span>
            </div>
        `;
    }

    // Create container and append elements
    const container = document.createElement('div');
    container.className = 'media-viewer-container';
    container.appendChild(closeBtn);
    container.insertAdjacentHTML('beforeend', mediaContent);
    
    mediaViewer.appendChild(container);
    
    // Close when clicking outside content
    mediaViewer.onclick = (e) => {
        if (e.target === mediaViewer) {
            document.body.removeChild(mediaViewer);
        }
    };

    // Prevent clicks on the content from closing the viewer
    container.onclick = (e) => {
        e.stopPropagation();
    };

    document.body.appendChild(mediaViewer);
}