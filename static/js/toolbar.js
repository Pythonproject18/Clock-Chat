window.addEventListener("pageshow", function (event) {
    if (event.persisted || (window.performance && performance.getEntriesByType("navigation")[0].type === "back_forward")) {
        // If the page was loaded from bfcache (back-forward cache), reload it
        location.reload();
    }
});


function profile_modal() {
    const modal = document.getElementById('profileModal');
    modal.classList.add('show');
    loadProfileData();
    // Add click listener to close modal when clicking outside
    setTimeout(() => {
        document.addEventListener('click', outsideClick);
    }, 0);
    }

    function close_profile_modal() {
    const modal = document.getElementById('profileModal');
    modal.classList.remove('show');
    document.removeEventListener('click', outsideClick);
        // Revert any unsaved changes
    for (let fieldId in originalValues) {
        const input = document.getElementById(fieldId);
        if (input) {
        input.value = originalValues[fieldId];
        input.setAttribute("readonly", true);
        }
    }

    // Clear saved originals
    Object.keys(originalValues).forEach(key => delete originalValues[key]);
    }
    function outsideClick(event) {
        const modal = document.getElementById('profileModal');
        const modalBox = document.querySelector('.profile-modal-box');
      
        const clickedElem = event.target;
      
        // Skip closing if clicked on the gender input or select (both use id="gender")
        if ((clickedElem.id === 'gender') || modalBox.contains(clickedElem)) {
          return;
        }
      
        if (modal.classList.contains('show')) {
          close_profile_modal();
        }
      }
      
      


    function loadProfileData() {
    fetch(`/userprofile/`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log(data);

            const setVal = (id, value) => {
                const el = document.getElementById(id);
                if (el) el.value = value || "";
            }

            const setText = (id, value) => {
                const el = document.getElementById(id);
                if (el) el.innerText = value || "";
            }

            const setSrc = (id, value, fallback) => {
                const el = document.getElementById(id);
                if (el) el.src = value || fallback;
            }

            setSrc("profilePhoto", data.profile_photo, "/static/images/default_avatar.png");
            setText("fullName", data.full_name);
            setVal("about", data.bio);
            setVal("email", data.email);
            setVal("dob", data.dob);
            setVal("gender", data.gender);
            setVal("dateJoined", data.date_joined);

            document.getElementById('profileModal').style.display = 'flex';
        })
        .catch(error => {
            console.error('Error loading profile data:', error);
        });
}

    
const originalValues = {};

function editField(fieldId) {
    const input = document.getElementById(fieldId);
    originalValues[fieldId] = input.value;

    // Enable editing for normal text input fields
    input.removeAttribute("readonly");
    input.focus();

    const onEnter = (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            const newValue = input.value;

            fetch("/profile/update/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken(),
                },
                body: JSON.stringify({ field: fieldId, value: newValue }),
            })
            .then(res => res.json())
            .then(data => {
                if (!data.success) {
                    alert("Update failed: " + data.message);
                    input.value = originalValues[fieldId];
                }
                input.setAttribute("readonly", true);
            })
            .catch(error => {
                alert("Error: " + error.message);
                input.value = originalValues[fieldId];
                input.setAttribute("readonly", true);
            });

            input.removeEventListener("keypress", onEnter);
        }
    };

    input.addEventListener("keypress", onEnter);
}

function getCSRFToken() {
    return document.cookie
        .split("; ")
        .find(row => row.startsWith("csrftoken="))
        ?.split("=")[1];
}



function updateGender(select) {
  const selectedValue = select.value;

  fetch("/profile/update/", {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(),
      },
      body: JSON.stringify({
          field: "gender",
          value: selectedValue,
      }),
  })
  .then(res => res.json())
  .then(data => {
      if (!data.success) {
          alert("Update failed: " + data.message);
      }
  })
  .catch(error => {
      alert("Error: " + error.message);
  });
}




function triggerPhotoUpload() {
    document.getElementById("photoInput").click();
}

function uploadProfilePhoto(input) {
    const file = input.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("photo", file);

    fetch("/profile/upload_photo/", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken(),
        },
        body: formData,
    })
    .then(res => res.json())
    .then(data => {
        if (data.success && data.photo_url) {
            document.getElementById("profilePhoto").src = data.photo_url;
        } else {
            alert("Failed to upload photo.");
        }
    })
    .catch(err => {
        console.error(err);
        alert("Error uploading photo.");
    });
}




function highlightActiveIcon() {
    const icons = document.querySelectorAll('.toolbar-icon');
    const currentPath = window.location.pathname;

    icons.forEach(icon => {
        icon.classList.remove('active');
    });

    // Match paths to icons
    if (currentPath.startsWith('/chat/')) {
        document.querySelector('.toolbar-icon[data-tooltip="Chats"]').classList.add('active');
    } else if (currentPath.startsWith('/status/')) {
        document.querySelector('.toolbar-icon[data-tooltip="Status"]').classList.add('active');
    } else if (currentPath.includes('/settings')) {
        document.querySelector('.toolbar-icon[data-tooltip="Settings"]').classList.add('active');
    }
}

document.addEventListener('DOMContentLoaded', highlightActiveIcon);