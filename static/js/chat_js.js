  function openmodal() {
    const modal = document.getElementById("openmodal");
    modal.style.display = "block";

    // Add outside click listener
    setTimeout(() => {
      document.addEventListener("click", outsideClickHandler);
    }, 0);
  }

  function close_modal() {
    const modal = document.getElementById("openmodal");
    modal.style.display = "none";

    // Remove listener when closed
    document.removeEventListener("click", outsideClickHandler);
  }

  function outsideClickHandler(event) {
    const modal = document.getElementById("openmodal");
    const content = document.querySelector(".modal-content");
    const user_list = document.getElementById("userList");
    const user_search = document.getElementById("userSearch");

    if (modal.style.display === "block" && !content.contains(event.target) && !user_list.contains(event.target)&& !user_search.contains(event.target)) {
      close_modal();
    }
  }




document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("chatSearch").addEventListener("input", function () {
    const query = this.value.toLowerCase();
    const chatItems = document.querySelectorAll("#chatList .chat-item");

    chatItems.forEach(item => {
      const title = item.querySelector(".chat-title").textContent.toLowerCase();
      item.style.display = title.includes(query) ? "flex" : "none";
    });
  });

  document.getElementById("userSearch").addEventListener("input", function () {
    const query = this.value.toLowerCase();
    const users = document.querySelectorAll("#userList .modal-option");

    users.forEach(user => {
      const name = user.querySelector(".user-name").textContent.toLowerCase();
      user.style.display = name.includes(query) ? "flex" : "none";
    });
  });
});



document.addEventListener('DOMContentLoaded', () => {
  let selectedUserIds = []
  let longPressTimer = null
  let isLongPress = false

  // Get CSRF token from meta tag
  function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content')
  }

  function toggleUserSelection(userId, element) {
    console.log("toggle selection")
    const idx = selectedUserIds.indexOf(userId)
    if (idx > -1) {
      selectedUserIds.splice(idx, 1)
      element.classList.remove('selected')
    } else {
      selectedUserIds.push(userId)
      element.classList.add('selected')
    }

    const createBtn = document.getElementById('createGroupChatBtn')
    createBtn.style.display = selectedUserIds.length > 1 ? 'block' : 'none'
  }

  function createPersonalChat(userId) {
    console.log("Creating personal chat with", userId)
    fetch('/chat/create/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken(),
      },
      body: JSON.stringify({
        user_ids: [userId]
      })
    })
    .then(res => res.json())
    .then(data => {
      if (data.status === 'success') {
        location.reload()
      } else {
        alert(data.message)
      }
    })
    .catch(err => console.error('Error creating personal chat:', err))
  }

  function createGroupChat() {
    console.log("Creating group chat with", selectedUserIds)
    fetch('/chat/create/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken(),
      },
      body: JSON.stringify({
        user_ids: selectedUserIds,
      })
    })
    .then(res => res.json())
    .then(data => {
      if (data.status === 'success') {
        location.reload()
      } else {
        alert(data.message)
      }
    })
    .catch(err => console.error('Error creating group chat:', err))
  }

  document.querySelectorAll('.modal-option').forEach(option => {
    const userId = parseInt(option.getAttribute('data-user-id'))

    option.addEventListener('mousedown', (e) => {
      isLongPress = false
      longPressTimer = setTimeout(() => {
        isLongPress = true
        toggleUserSelection(userId, option)
      }, 500)
    })

    option.addEventListener('mouseup', () => {
      clearTimeout(longPressTimer)
    })

    option.addEventListener('mouseleave', () => {
      clearTimeout(longPressTimer)
    })

    option.addEventListener('click', () => {
      console.log("click on user", userId)
      if (!isLongPress && selectedUserIds.length === 0) {
        createPersonalChat(userId)
      }
    })
  })

  const createBtn = document.getElementById('createGroupChatBtn')
  if (createBtn) {
    createBtn.addEventListener('click', createGroupChat)
  }
})
