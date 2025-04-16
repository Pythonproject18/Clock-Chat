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
    const buttondropdown = document.getElementById('dropdownbtn');
    const input = document.getElementById(fieldId);
    originalValues[fieldId] = input.value;

    if (fieldId === "gender") {
        const genderOptions = [
            { label: "Male", value: 1 },
            { label: "Female", value: 2 },
            { label: "Other", value: 3 },
        ];

        const select = document.createElement("select");
        select.style.width = "100%";
        select.style.color = "#ffffff";
        select.style.border = "none";
        select.style.background = "#323232";
        select.style.padding = "5px";
        select.id = fieldId;

        genderOptions.forEach(option => {
            buttondropdown.style.display = "none";

            const opt = document.createElement("option");
            opt.value = option.value;
            opt.text = option.label;

            if (option.label.toLowerCase() === input.value.toLowerCase()) {
                opt.selected = true;
            }

            select.appendChild(opt);
        });

        input.replaceWith(select);
        select.focus();

        // On change, send the update immediately
        select.addEventListener("change", () => {
            const newValue = select.value;

            fetch("/profile/update/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken(),
                },
                body: JSON.stringify({
                    field: fieldId,
                    value: newValue, // Send number (1, 2, 3)
                }),
            })
                .then((res) => res.json())
                .then((data) => {
                    const selectedOption = genderOptions.find(opt => opt.value == newValue);
                    const newInput = document.createElement("input");
                    newInput.type = "text";
                    newInput.id = fieldId;
                    newInput.value = data.success ? selectedOption.label : originalValues[fieldId];
                    newInput.setAttribute("readonly", true);
                    newInput.setAttribute("onclick", `editField('${fieldId}')`);
                    select.replaceWith(newInput);
                })
                .catch((error) => {
                    alert("Error: " + error.message);
                    const revertInput = document.createElement("input");
                    revertInput.type = "text";
                    revertInput.id = fieldId;
                    revertInput.value = originalValues[fieldId];
                    revertInput.setAttribute("readonly", true);
                    revertInput.setAttribute("onclick", `editField('${fieldId}')`);
                    select.replaceWith(revertInput);
                });
        });
    } else {
        // Editable text input fields
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
}

function getCSRFToken() {
    return document.cookie
        .split("; ")
        .find((row) => row.startsWith("csrftoken="))
        ?.split("=")[1];
}
