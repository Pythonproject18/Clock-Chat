function openmodal() {
  let modal = document.getElementById("openmodal");
  modal.style.display = "block";
}

function close_modal() {
  let modal = document.getElementById("openmodal");
  modal.style.display = "none";
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