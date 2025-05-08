// Audio recording functionality
let mediaRecorder;
let audioChunks = [];
let audioBlob;
let stream;
let timerInterval;
let recordingSeconds = 0;


function startRecording() {
    document.getElementById('plusIcon').style.display = "none";
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(s => {
            stream = s;
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];

            mediaRecorder.ondataavailable = (event) => {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = () => {
                audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            };

            mediaRecorder.start();
            startTimer(); // <-- Start the timer here

            // UI changes
            document.getElementById("micIcon").style.display = "none";
            document.getElementById("micStop").style.display = "inline-block";
            document.getElementById("sendBtn").style.display = "inline-block";
            document.getElementById("deleteBtn").style.display = "inline";
        })
        .catch(error => {
            alert("Microphone access denied: " + error);
            console.error(error);
        });
}

function stopRecording() {
    document.getElementById('plusIcon').style.display = "none";
    if (mediaRecorder && mediaRecorder.state === "recording") {
        mediaRecorder.pause();
        pauseTimer(); // <-- Pause timer when recording is paused

        // UI changes
        document.getElementById("micStop").style.display = "none";
        document.getElementById("resumeBtn").style.display = "inline-block";
        document.getElementById("sendBtn").style.display = "inline-block";

    }
}

function resumeRecording() {
    document.getElementById('plusIcon').style.display = "none";
    if (mediaRecorder && mediaRecorder.state === "paused") {
        mediaRecorder.resume();
        startTimer(); // <-- Resume timer

        // UI changes
        document.getElementById("resumeBtn").style.display = "none";
        document.getElementById("micStop").style.display = "inline-block";
        document.getElementById("sendBtn").style.display = "inline-block";

    }
}

function sendRecording() {
    if (!mediaRecorder) return;

    mediaRecorder.onstop = () => {
        audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
        resetTimer();

        const formData = new FormData();
        formData.append("audio", audioBlob, "recording.webm");
        formData.append("chat_id", document.getElementById("chatId").value);

        fetch("/send-audio-message/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const messagesContainer = document.getElementById("messagesContainer");

                const messageDiv = document.createElement("div");
                messageDiv.className = "message sent";
                messageDiv.innerHTML = `
                    <div class="message-content">
                        <audio controls controlsList="nodownload noplaybackrate nofullscreen" src="${data.audio_url}" style="max-height: 40px;"></audio>
                        <div class="message-time">${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</div>
                    </div>
                `;
                messagesContainer.appendChild(messageDiv);
                scrollToBottom();
            } else {
                alert("Failed to send audio: " + data.error);
            }
        })
        .catch(error => {
            console.error("Error sending audio:", error);
        });
        stopMicStream();

        // UI reset
        document.getElementById('plusIcon').style.display = "block";
        document.getElementById("micIcon").style.display = "inline-block";
        document.getElementById("micStop").style.display = "none";
        document.getElementById("resumeBtn").style.display = "none";
        document.getElementById("sendBtn").style.display = "none";
        document.getElementById("deleteBtn").style.display = "none";
        document.getElementById("recordingTimer").style.display = "none";
    };

    if (mediaRecorder.state !== "inactive") {
        mediaRecorder.stop();
    }
}

function deleteRecording() {
    if (mediaRecorder && mediaRecorder.state !== "inactive") {
        mediaRecorder.stop();
    }
    
    // Clear chunks
    audioChunks = [];
    stopMicStream();
    resetTimer(); // <-- Stop and reset the timer

    // UI reset
    document.getElementById('plusIcon').style.display = "block";
    document.getElementById("micIcon").style.display = "inline-block";
    document.getElementById("micStop").style.display = "none";
    document.getElementById("resumeBtn").style.display = "none";
    document.getElementById("sendBtn").style.display = "none";
    document.getElementById("deleteBtn").style.display = "none";
    document.getElementById("recordingTimer").style.display = "none";

}

function stopMicStream() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }
}


function startTimer() {
    document.getElementById("recordingTimer").style.display = "inline-block";
    timerInterval = setInterval(() => {
        recordingSeconds++;
        updateTimerDisplay();
    }, 1000);
}

function pauseTimer() {
    clearInterval(timerInterval);
}

function resetTimer() {
    clearInterval(timerInterval);
    recordingSeconds = 0;
    updateTimerDisplay();
    document.getElementById("recordingTimer").style.display = "none";
}

function updateTimerDisplay() {
    const minutes = String(Math.floor(recordingSeconds / 60)).padStart(2, '0');
    const seconds = String(recordingSeconds % 60).padStart(2, '0');
    document.getElementById("recordingTimer").textContent = `${minutes}:${seconds}`;
}
