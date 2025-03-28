function openmodal(){
  let modal=document.getElementById("openmodal");
  modal.style.display="block";
}

function close_modal(){
    let modal=document.getElementById("openmodal");
    modal.style.display="none";
}

window.onclick = function(event) {
    let modal = document.getElementById('openmodal');
    let plus = document.getElementById('plus_icon');
    if (event.target !== modal && event.target !== plus) {
      modal.style.display = "none";
    }

  }

