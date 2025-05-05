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
        
        // Insert after the time element
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
        emojiSpan.innerHTML = reaction.value;
        emojiSpan.className = 'message-reaction';
        if (reaction.is_current_user) {
            emojiSpan.classList.add('user-reaction');
        }
        reactionsContainer.appendChild(emojiSpan);
    });
}
