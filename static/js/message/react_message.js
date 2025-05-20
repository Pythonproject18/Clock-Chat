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

// When rendering modal emojis, include data-reaction-id and data-message-id
function openModal(event, messageId) {
    event.stopPropagation();
    const reactionsContainer = event.currentTarget;
    const modal = document.getElementById("emojiModal");
    modal.style.display = "flex";
    const modalContent = modal.querySelector('.modal-reacted');
    modalContent.innerHTML = '';

    // Get all reactions from the message's emoji-reactions bar
    const messageElement = document.querySelector(`.message[data-message-id="${messageId}"]`);
    const emojiSpans = messageElement.querySelectorAll('.message-reaction');
    emojiSpans.forEach(emojiSpan => {
        const emojiContent = emojiSpan.querySelector('span:last-child');
        const usernameSpan = emojiSpan.querySelector('.username');
        const reactionId = emojiSpan.dataset.reactionId;
        const emojiHtml = emojiContent ? emojiContent.innerHTML : '';
        const username = usernameSpan ? usernameSpan.textContent : '';
        const modalEmoji = document.createElement('span');
        modalEmoji.className = 'modal-emoji';
        modalEmoji.innerHTML = username + emojiHtml;
        modalEmoji.dataset.reactionId = reactionId;
        modalEmoji.dataset.messageId = messageId;
        modalContent.appendChild(modalEmoji);
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

// When rendering message reactions, set data-reaction-id for each emoji
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

    reactions.forEach(reaction => {
        const emojiSpan = document.createElement('span');
        emojiSpan.className = 'message-reaction';
        if (reaction.is_current_user) {
            emojiSpan.classList.add('user-reaction');
        }
        emojiSpan.dataset.reactionId = reaction.id; // Set reaction id for modal use

        const usernameSpan = document.createElement('span');
        usernameSpan.className = 'username';
        usernameSpan.textContent = reaction.username + ': ';

        const emojiContent = document.createElement('span');
        emojiContent.innerHTML = reaction.value;

        emojiSpan.appendChild(usernameSpan);
        emojiSpan.appendChild(emojiContent);

        reactionsContainer.appendChild(emojiSpan);
    });

    // Add click event to open modal
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