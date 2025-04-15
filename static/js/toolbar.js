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
      }
    
      function outsideClick(event) {
        const modal = document.getElementById('profileModal');
        const modalBox = document.querySelector('.profile-modal-box');
    
        // If clicked outside modal-box but inside modal
        if (!modalBox.contains(event.target) && modal.classList.contains('show')) {
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
                document.getElementById('profilePhoto').src = data.profile_photo;
                document.getElementById('about').src = data.bio;
                document.getElementById('fullName').innerText = data.full_name || "";
                document.getElementById('email').innerText = ` ${data.email || ""}`;
                document.getElementById('dob').innerText = ` ${data.dob || ""}`;
                document.getElementById('gender').innerText = `${data.gender || ""}`;
                document.getElementById('dateJoined').innerText = `Joined: ${data.date_joined || ""}`;
    
                // Show the modal
                document.getElementById('profileModal').style.display = 'flex';
            })
            .catch(error => {
                console.error('Error loading profile data:', error);
            });
    }
    
    