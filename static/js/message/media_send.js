
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


function triggerMediaInput() {
    document.getElementById("sendIcon").style.display="none";
    document.getElementById("send_media").style.display="block";
    document.getElementById("mediaInput").click();
    // Hide mic icon when adding media
    const micIcon = document.getElementById("micIcon");
    if (micIcon) micIcon.style.display = "none";
}


function showMediaPreview(files) {
    const previewContainer = document.getElementById("mediaPreview");
    previewContainer.innerHTML = "";
        const micIcon = document.getElementById("micIcon");
    if (micIcon) micIcon.style.display = "none";

        document.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && files.length > 0) {
            const chatId = document.getElementById('chatId').value;
            sendSelectedMedia(chatId);
        }
    });


    // Create a grid container
    const gridContainer = document.createElement("div");
    gridContainer.className = "media-preview-grid";
    previewContainer.appendChild(gridContainer);

    files.forEach(file => {
        const preview = document.createElement("div");
        preview.className = "media-preview-item";

        if (file.type.startsWith("image/")) {
            const imgWrapper = document.createElement("div");
            imgWrapper.className = "media-preview-image-wrapper";
            
            const img = document.createElement("img");
            img.src = URL.createObjectURL(file);
            img.className = "media-preview-image";
            img.onload = () => URL.revokeObjectURL(img.src);
            
            imgWrapper.appendChild(img);
            preview.appendChild(imgWrapper);
        } 
        else if (file.type.startsWith("video/")) {
            const videoWrapper = document.createElement("div");
            videoWrapper.className = "media-preview-video-wrapper";
            
            const video = document.createElement("video");
            video.src = URL.createObjectURL(file);
            video.className = "media-preview-video";
            video.controls = false;
            video.muted = true;
            video.playsInline = true;
            
            // Add play button overlay
            const playButton = document.createElement("div");
            playButton.className = "media-preview-play-button";
            playButton.innerHTML = '<i class="fas fa-play"></i>';
            
            // Click to play/pause
            playButton.addEventListener('click', (e) => {
                e.stopPropagation();
                if (video.paused) {
                    video.play();
                    playButton.style.display = 'none';
                } else {
                    video.pause();
                    playButton.style.display = 'flex';
                }
            });
            
            videoWrapper.appendChild(video);
            videoWrapper.appendChild(playButton);
            preview.appendChild(videoWrapper);
            
            // Revoke URL when video is loaded
            video.onloadeddata = () => URL.revokeObjectURL(video.src);
        } 
        else if (file.type.startsWith("audio/")) {
            const audioWrapper = document.createElement("div");
            audioWrapper.className = "media-preview-audio-wrapper";
            
            const audio = document.createElement("audio");
            audio.src = URL.createObjectURL(file);
            audio.controls = true;
            audio.className = "media-preview-audio";
            
            audioWrapper.appendChild(audio);
            preview.appendChild(audioWrapper);
            
            audio.onloadeddata = () => URL.revokeObjectURL(audio.src);
        } 
        else {
            const fileWrapper = document.createElement("div");
            fileWrapper.className = "media-preview-file-wrapper";
            
            const icon = document.createElement("i");
            icon.className = "fas fa-file-alt";
            
            const name = document.createElement("span");
            name.className = "media-preview-file-name";
            name.textContent = file.name.length > 20 
                ? file.name.substring(0, 17) + '...' 
                : file.name;
            
            fileWrapper.appendChild(icon);
            fileWrapper.appendChild(name);
            preview.appendChild(fileWrapper);
        }

        gridContainer.appendChild(preview);
    });
}

function sendSelectedMedia(chatId) {
    if (selectedMediaFiles.length === 0) {
        console.log("No media selected.");
        return;
    }

    const formData = new FormData();
    formData.append("chat_id", chatId);

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
        
        // Reload messages after successful upload
        const chatTitle = document.querySelector('.chat-header-info h2').textContent;
        loadChatMessages(chatId, chatTitle);
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
