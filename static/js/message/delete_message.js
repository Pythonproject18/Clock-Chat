// Message deletion functions
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
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ purpose: purpose })
    })
    .then(response => {
        if (response.ok) {
            console.log(`Message ${msgId} deleted (${purpose})`);
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
