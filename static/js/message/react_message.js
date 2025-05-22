// Function to send reaction to server
function reactToMessage(messageId, emojiId) {
    fetch('/message/react/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
            message_id: messageId,
            emoji_id: emojiId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            updateMessageReactionsUI(messageId, data.reactions);
        } else {
            console.error('Failed to react:', data.message);
        }
    })
    .catch(error => {
        console.error('Error reacting to message:', error);
    });
}

// ...existing code...

function openModal(event, messageId) {
    event.stopPropagation();
    const modal = document.getElementById("emojiModal");
    modal.style.display = "flex";
    const modalContent = modal.querySelector('.modal-reacted');
    modalContent.innerHTML = '';

    // Get all reactions from the message's emoji-reactions bar
    const messageElement = document.querySelector(`.message[data-message-id="${messageId}"]`);
    const emojiSpans = messageElement.querySelectorAll('.message-reaction');
    emojiSpans.forEach(emojiSpan => {
        // Get only the emoji (without count)
        const emojiContent = emojiSpan.querySelector('span:last-child');
        let emojiOnly = '';
        if (emojiContent) {
            // Remove <sup>...</sup> from innerHTML
            emojiOnly = emojiContent.innerHTML.replace(/<sup>.*?<\/sup>/, '').trim();
        }
        const usernames = (emojiSpan.dataset.username || '').split(',').map(u => u.trim()).filter(Boolean);
        const reactionId = emojiSpan.dataset.reactionId;
        const messageIdAttr = messageId;

        // Show each user as a separate entry for this emoji, without count
        usernames.forEach(username => {
            const modalEmoji = document.createElement('span');
            modalEmoji.className = 'modal-emoji';
            // Use flex to shift emoji to the right
            modalEmoji.style.display = "flex";
            modalEmoji.style.alignItems = "center";
            modalEmoji.style.justifyContent = "space-between";
            modalEmoji.innerHTML = `
                <span class="modal-username">${username}</span>
                <span class="modal-emoji-value">${emojiOnly}</span>
            `;
            modalEmoji.dataset.reactionId = reactionId;
            modalEmoji.dataset.messageId = messageIdAttr;
            modalEmoji.dataset.username = username;
            modalContent.appendChild(modalEmoji);
        });
    });

    modal.dataset.messageId = messageId;
}

// Add click handler for modal emojis (delete on click)
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById("emojiModal");
    const modalContent = modal.querySelector('.modal-reacted');
    modalContent.onclick = function(event) {
        const emojiSpan = event.target.closest('.modal-emoji');
        if (!emojiSpan) return;
        const reactionId = emojiSpan.dataset.reactionId;
        const messageId = emojiSpan.dataset.messageId;
        if (!reactionId || !messageId) return;

        // Send delete request
        fetch('/message/react/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                message_id: messageId,
                reaction_id: reactionId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                updateMessageReactionsUI(messageId, data.reactions);
                modal.style.display = "none";
            }
        });
    };
});

function updateMessageReactionsUI(messageId, reactions) {
    const messageElement = document.querySelector(`.message[data-message-id="${messageId}"]`);
    if (!messageElement) return;

    let reactionsContainer = messageElement.querySelector('.emoji-reactions');
    if (!reactionsContainer) {
        reactionsContainer = document.createElement('div');
        reactionsContainer.className = 'emoji-reactions';
        const timeElement = messageElement.querySelector('.message-time');
        if (timeElement) {
            timeElement.insertAdjacentElement('afterend', reactionsContainer);
        } else {
            messageElement.querySelector('.message-content').appendChild(reactionsContainer);
        }
    }

    reactionsContainer.innerHTML = '';

    let totalCount = 0;

    reactions.forEach(reaction => {
        const emojiSpan = document.createElement('span');
        emojiSpan.className = 'message-reaction';
        if (reaction.is_current_user) {
            emojiSpan.classList.add('user-reaction');
        }

        emojiSpan.dataset.reactionId = reaction.id;
        emojiSpan.dataset.username = reaction.usernames.join(', ');  // tooltip use

        const emojiContent = document.createElement('span');
        emojiContent.innerHTML = `${reaction.value}`; // No count per emoji

        emojiSpan.appendChild(emojiContent);
        reactionsContainer.appendChild(emojiSpan);

        totalCount += reaction.count;
    });

    // Show total count at the end only if more than one reaction
    if (totalCount > 1) {
        const totalCountSpan = document.createElement('span');
        totalCountSpan.className = 'reactions-total-count';
        totalCountSpan.textContent = `+${totalCount}`;
        reactionsContainer.appendChild(totalCountSpan);
    }

    reactionsContainer.onclick = function(event) {
        openModal(event, messageId);
    };
}


// Close the modal when clicking outside of modal content
document.addEventListener('click', function(event) {
    const modal = document.getElementById("emojiModal");
    
    // Only act if modal is visible
    if (modal.style.display === "flex") {
        const modalContent = modal.querySelector('.modal-reacted');
        
        // If the clicked element is not the modal content or its children
        if (!modalContent.contains(event.target)) {
            modal.style.display = "none";
        }
    }
});