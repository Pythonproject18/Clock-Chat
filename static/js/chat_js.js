function openmodal() {
  let modal = document.getElementById("openmodal");
  modal.style.display = "block";
}

function close_modal() {
  let modal = document.getElementById("openmodal");
  modal.style.display = "none";
}

document.addEventListener('click', function(event) {
  let modal = document.getElementById('openmodal');
  let isPlusIcon = event.target.closest('#plus_icon, #plusIcon');
  let isModalContent = event.target.closest('.modal-content');
  
  if (modal.style.display === "block" && !isModalContent && !isPlusIcon) {
    close_modal();
  }
});