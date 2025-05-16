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
// In the renderMessages function, update the media handling section:
} else if (msg.media_url) {
    // Filter out non-image/video files
    const mediaItems = msg.media_url.filter(media => 
        media.match(/\.(jpg|jpeg|png|gif|webp|mp4|webm|ogg|mov)$/i)
    );
    
    if (mediaItems.length > 0) {
        const mediaCount = mediaItems.length;
        const showCount = Math.min(mediaCount, 4); // Show max 4 items
        const hasMore = mediaCount > 4;
        
        bubbleContent = `<div class="media-grid media-count-${showCount}">`;
        
        mediaItems.slice(0, showCount).forEach((media, index) => {
            const isLastInRow = (index + 1) % 2 === 0 || index === showCount - 1;
            const marginClass = isLastInRow ? 'no-margin' : '';
            
            if (media.match(/\.(jpg|jpeg|png|gif|webp)$/i)) {
                bubbleContent += `<div class="media-grid-item ${marginClass}" onclick="event.stopPropagation(); openMediaViewer('${media}', 'image')">
                    <img src="${media}" class="media-message">
                    ${showCount > 1 ? '<div class="media-overlay"></div>' : ''}
                    ${hasMore && index === showCount - 1 ? 
                      `<div class="more-items-count">+${mediaCount - showCount}</div>` : ''}
                </div>`;
            } else if (media.match(/\.(mp4|webm|ogg|mov)$/i)) {
                bubbleContent += `<div class="media-grid-item ${marginClass}" onclick="openMediaViewer('${media}', 'video')">
                    <video class="media-message">
                        <source src="${media}">
                    </video>
                    <div class="video-play-icon"><i class="fas fa-play"></i></div>
                    ${showCount > 1 ? '<div class="media-overlay"></div>' : ''}
                    ${hasMore && index === showCount - 1 ? 
                      `<div class="more-items-count">+${mediaCount - showCount}</div>` : ''}
                </div>`;
            }
        });
        
        bubbleContent += '</div>';
    }
    
    // Handle any document files separately (not in grid)
    const docItems = msg.media_url.filter(media => 
        !media.match(/\.(jpg|jpeg|png|gif|webp|mp4|webm|ogg|mov)$/i)
    );

    if (docItems.length > 0) {
        docItems.forEach(media => {
            const fileName = media.split('/').pop();
            const fileExtension = fileName.split('.').pop().toUpperCase();
            bubbleContent += `
            <div class="document-message ${isSender ? 'sent' : 'received'}" ondblclick="window.open('${media}', '_blank')">
                    <i class="fa-solid fa-file" id="doc-icon">
                    <span class="file-extension">${fileExtension}</span>
                    </i>
                <div class="document-info">
                    <div class="document-name">${fileName}</div>
                    <div class="document-actions">
                        <a href="${media}" download="${fileName}" class="document-action" title="Download">
                            <i class="fas fa-download"></i>
                        </a>
                    </div>
                </div>
            </div>`;
        });
    }
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
                    <div class="emoji-reactions" onclick="openModal(event, '${msg.id}')">
                        ${msg.reactions.map(reaction => 
                            `<span class="message-reaction ${reaction.is_current_user ? 'user-reaction' : ''}">${reaction.username}: ${reaction.value}</span>`
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



function openMediaViewer(clickedUrl, clickedType) {
    const allMediaElements = document.querySelectorAll('.media-grid-item');
    const mediaList = [];

    allMediaElements.forEach(el => {
        const img = el.querySelector('img');
        const video = el.querySelector('video');
        const source = el.querySelector('source');

        if (img) {
            mediaList.push({ url: img.src, type: 'image' });
        } else if (video) {
            mediaList.push({ url: source?.src || video.src, type: 'video' });
        }
    });

    // Normalize blob URLs (createObjectURL) for match
    const matchIndex = mediaList.findIndex(media =>
        media.url === clickedUrl || clickedUrl.includes(media.url) || media.url.includes(clickedUrl)
    );

    let currentIndex = matchIndex !== -1 ? matchIndex : 0;

    const overlay = document.createElement('div');
    overlay.className = 'media-viewer-overlay';

    const container = document.createElement('div');
    container.className = 'media-viewer-container';

    const closeBtn = document.createElement('div');
    closeBtn.className = 'media-viewer-close';
    closeBtn.innerHTML = '<i class="fas fa-times"></i>';
    closeBtn.onclick = () => document.body.removeChild(overlay);

    const leftArrow = document.createElement('div');
    leftArrow.innerHTML = '<i class="fas fa-chevron-left"></i>';
    leftArrow.className = 'carousel-nav left';

    const rightArrow = document.createElement('div');
    rightArrow.innerHTML = '<i class="fas fa-chevron-right"></i>';
    rightArrow.className = 'carousel-nav right';

    function renderMedia(index) {
        const media = mediaList[index];
        const old = container.querySelector('.media-viewer-content');
        if (old) container.removeChild(old);

        let content;
        if (media.type === 'image') {
            content = document.createElement('img');
            content.src = media.url;
            content.className = 'media-viewer-content';
        } else if (media.type === 'video') {
            content = document.createElement('video');
            content.className = 'media-viewer-content';
            content.controls = true;
            content.autoplay = true;
            content.innerHTML = `<source src="${media.url}">Your browser does not support the video tag.`;
        }

        container.appendChild(content);

        // 🔁 Show/hide arrows based on position
        leftArrow.style.display = index === 0 ? 'none' : 'block';
        rightArrow.style.display = index === mediaList.length - 1 ? 'none' : 'block';
    }


    leftArrow.onclick = () => {
        currentIndex = (currentIndex - 1 + mediaList.length) % mediaList.length;
        renderMedia(currentIndex);
    };

    rightArrow.onclick = () => {
        currentIndex = (currentIndex + 1) % mediaList.length;
        renderMedia(currentIndex);
    };

    container.appendChild(closeBtn);
    overlay.appendChild(container);
    overlay.appendChild(leftArrow);
    overlay.appendChild(rightArrow);
    document.body.appendChild(overlay);

    renderMedia(currentIndex);
}