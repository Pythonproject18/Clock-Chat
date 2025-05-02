
let selectedMediaFiles = [];

function triggerMediaInput() {
    document.getElementById("sendIcon").style.display="none";
    document.getElementById("send_media").style.display="block";
    document.getElementById("mediaInput").click();
}

document.addEventListener("DOMContentLoaded", function () {
    const mediaInput = document.getElementById("mediaInput");

    if (!mediaInput) {
        console.error("mediaInput element not found.");
        return;
    }

    mediaInput.addEventListener("change", function (event) {
        selectedMediaFiles = Array.from(event.target.files);
        showMediaPreview(selectedMediaFiles);
    });
});

function showMediaPreview(files) {
    const previewContainer = document.getElementById("mediaPreview");
    console.log("dshbhdsfsfsf");
    previewContainer.innerHTML = "";

    files.forEach(file => {
        const preview = document.createElement("div");
        preview.classList.add("media-preview");  // Common class for all previews
    
        if (file.type.startsWith("image/")) {
            const img = document.createElement("img");
            img.src = URL.createObjectURL(file);
            img.classList.add("media-image");
            preview.appendChild(img);
        } else if (file.type.startsWith("video/")) {
            const video = document.createElement("video");
            video.src = URL.createObjectURL(file);
            video.controls = true;
            video.classList.add("media-video");
            preview.appendChild(video);
        } else if (file.type.startsWith("audio/")) {
            const audio = document.createElement("audio");
            audio.src = URL.createObjectURL(file);
            audio.controls = true;
            audio.classList.add("media-audio");
            preview.appendChild(audio);
        } else {
            const span = document.createElement("span");
            span.textContent = file.name;
            span.classList.add("media-file");
            preview.appendChild(span);
        }
    
        previewContainer.appendChild(preview);
    });
}

function sendSelectedMedia(chatId) {
    if (selectedMediaFiles.length === 0) {
        console.log("No media selected.");
        return;
    }

    const formData = new FormData();
    formData.append("chat_id", chatId);  // Use passed chatId

    selectedMediaFiles.forEach((file, index) => {
        formData.append(`media_${index}`, file);
    });

    fetch("/message/upload_media/", {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": getCSRFToken()
        }
    })
    .then(response => {
        if (!response.ok) throw new Error("Upload failed");
        return response.json();
    })
    .then(data => {
        console.log("Media uploaded successfully.");
        selectedMediaFiles = [];
        document.getElementById("mediaPreview").innerHTML = "";
        document.getElementById("send_media").style.display = "none";
    })
    .catch(error => {
        console.error("Media upload failed.", error);
        document.getElementById("send_media").style.display = "none";
    });
}


function getCSRFToken() {
    return document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken'))
        ?.split('=')[1];
}
