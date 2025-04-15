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
        console.log(fieldId);
      const input = document.getElementById(fieldId);
    
      // Store original value
      originalValues[fieldId] = input.value;
      console.log("hellooo");
    
      // Make editable and focus
      input.removeAttribute("readonly");
      input.focus();
    
      // Listen for Enter key
      const onEnter = (e) => {
        if (e.key === "Enter") {
        console.log("pressed");
            
          e.preventDefault();
    
          const newValue = input.value;
    
          fetch("/profile/update/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": getCSRFToken(),
            },
            body: JSON.stringify({
              field: fieldId,
              value: newValue,
            }),
          })
            .then((res) => res.json())
            .then((data) => {
              if (!data.success) {
                alert("Update failed: " + data.message);
                input.value = originalValues[fieldId];
              }
              input.setAttribute("readonly", true);
            })
            .catch((error) => {
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
        .find((row) => row.startsWith("csrftoken="))
        ?.split("=")[1];
    }
    
    