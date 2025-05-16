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

    // Clear existing reactions
    reactionsContainer.innerHTML = '';

    // Add all reactions
    reactions.forEach(reaction => {
        const emojiSpan = document.createElement('span');
        emojiSpan.className = 'message-reaction';
        if (reaction.is_current_user) {
            emojiSpan.classList.add('user-reaction');
        }
        
        // Create username span
        const usernameSpan = document.createElement('span');
        usernameSpan.className = 'username';
        usernameSpan.textContent = reaction.username + ': ';
        
        // Create emoji span
        const emojiContent = document.createElement('span');
        emojiContent.innerHTML = reaction.value;
        
        // Append both
        emojiSpan.appendChild(usernameSpan);
        emojiSpan.appendChild(emojiContent);
        
        reactionsContainer.appendChild(emojiSpan);
    });
}

// Function to open the modal with existing reactions
function openModal(event, messageId) {
    // Stop this click from bubbling up to document
    event.stopPropagation();
    
    // Get the reactions container that was clicked
    const reactionsContainer = event.currentTarget;
    
    // Clone the reactions to show in modal
    const reactions = Array.from(reactionsContainer.querySelectorAll('.message-reaction')).map(el => ({
        value: el.innerHTML,
        isCurrentUser: el.classList.contains('user-reaction')
    }));
    
    const modal = document.getElementById("emojiModal");
    modal.style.display = "flex";
    
    // Update modal content with only the reacted emojis
    const modalContent = modal.querySelector('.modal-reacted');
    modalContent.innerHTML = '';
    
    reactions.forEach(reaction => {
        const emojiSpan = document.createElement('span');
        emojiSpan.innerHTML = reaction.value;
        emojiSpan.className = 'modal-emoji';
        if (reaction.isCurrentUser) {
            emojiSpan.classList.add('user-reaction');
        }
        modalContent.appendChild(emojiSpan);
    });
    
    // Store the message ID on the modal for later use if needed
    modal.dataset.messageId = messageId;
}

// Function to close the modal
function closeModal() {
    document.getElementById("emojiModal").style.display = "none";
}

// Close modal when clicking outside
document.addEventListener('click', function() {
    const modal = document.getElementById("emojiModal");
    if (modal.style.display === "flex") {
        closeModal();
    }
});

// Prevent clicks inside modal from closing it
document.getElementById("emojiModal").addEventListener('click', function(event) {
    event.stopPropagation();
});