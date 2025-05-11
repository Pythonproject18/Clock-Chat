document.addEventListener("DOMContentLoaded", () => {
  const statusData = document.getElementById('status-data');

  if (statusData) {
    const data = JSON.parse(statusData.textContent);
    let statuses = data.statuses || [];
    let currentIndex = 0;
    let isPaused = false;
    let progressStartTime;
    let elapsed = 0;
    let progressTimeout;

    const STATUS_DURATION = 10000; // 10 seconds

    function renderStatus(index) {
      const container = document.getElementById('status-container');
      if (!statuses.length || index >= statuses.length || index < 0) return;

      const status = statuses[index];
      const isOwner = data.userId === data.viewerId;
      const isvideo = status.type == '2';

      container.innerHTML = `
        <div class="progress-bar"><div class="progress-fill" id="progress-fill"></div></div>

        <div class="status-header">
          <div class="profile-pic">
            <img src="${data.userProfile || '/static/images/default_avatar.png'}" style="border-radius: 50%; height: 100%; width: 100%;">
          </div>
          <div class="user-info">
            <div class="number">${data.userFullName}</div>
            <div class="time">${new Date(status.created_at).toLocaleString()}</div>
          </div>
          <div style="margin-top: 5%;position: absolute; right: 10%; top: 10px;">
            <button id="pause-play-btn" style="background: transparent;border:none;">
              <i class="fa-solid ${isPaused ? 'fa-play' : 'fa-pause'}" style="color: white;"></i>
            </button>
          </div>
        </div>

        <div id="viewerModal" class="viewer-modal">
          <div class="viewer-modal-box">
            <div id="header">
              <span class="close-btn" onclick="close_viewer_modal()">&times;</span>
              <h2 style="text-align: start;">Seen by</h2>
            </div>
            <div class="viewer-modal-content">
              <p style="text-align:center; color: black;">No viewers yet.</p>
            </div>
          </div>
        </div>

        <div class="status-body">
        ${isvideo ? `<video autoplay src="${status.media_url}" 
            style="width:100%;max-height:100%; object-fit:cover;">
          `:
          `<img src="${status.media_url}" style="width:100%;max-height:100%; object-fit:cover;">`
        }
        </div>

        ${status.caption ? `<div style="text-align: center; font-size: larger;">${status.caption}</div>` : ''}

        ${isOwner ? ` 
          <div class="view-count" onclick="open_viewer_modal(${status.id})">
            <i class="fa fa-eye"></i> <span>${status.viewers_count}</span>
          </div>
        ` : ''}
     `;

      document.getElementById("pause-play-btn").addEventListener("click", togglePausePlay);

      document.querySelector(".fa-less-than").addEventListener("click", (e) => {
        e.stopPropagation();
        showPrevious();
      });

      document.querySelector(".fa-greater-than").addEventListener("click", (e) => {
        e.stopPropagation();
        showNext();
      });

      startProgress();
    }

    function startProgress() {
      const bar = document.getElementById("progress-fill");
      bar.style.width = "0%";
      bar.style.transition = "none";

      elapsed = 0;
      progressStartTime = Date.now();

      const isVideo = statuses[currentIndex].type == '2';

      if (isVideo) {
        const video = document.querySelector("video");
        if (video) {
          const setupVideoProgress = () => {
            const duration = video.duration * 1000; // convert to milliseconds
            if (!isPaused) {
              bar.style.transition = `width ${duration}ms linear`;
              bar.style.width = "100%";
              scheduleNext(duration);
            }
          };

          if (video.readyState >= 1) {
            // metadata already loaded
            setupVideoProgress();
          } else {
            // wait for metadata to load
            video.addEventListener("loadedmetadata", setupVideoProgress, { once: true });
          }
        }
      } else {
        setTimeout(() => {
          if (!isPaused) {
            bar.style.transition = `width ${STATUS_DURATION}ms linear`;
            bar.style.width = "100%";
            scheduleNext(STATUS_DURATION);
          }
        }, 10);
      }
    }

    function scheduleNext(durationLeft) {
      progressTimeout = setTimeout(() => {
        showNext();
      }, durationLeft);
    }

    function pauseProgress() {
      isPaused = true;
      clearTimeout(progressTimeout);
      elapsed += Date.now() - progressStartTime;
      const bar = document.getElementById("progress-fill");
      const computedStyle = window.getComputedStyle(bar);
      const width = computedStyle.width;
      bar.style.transition = "none";
      bar.style.width = width;

      const video = document.querySelector("video");
      if (video && !video.paused) {
        video.pause();
      }

      updatePausePlayIcon();
    }

    function resumeProgress() {
      isPaused = false;
      progressStartTime = Date.now();
      const bar = document.getElementById("progress-fill");

      const isVideo = statuses[currentIndex].type == '2';
      const duration = isVideo ? (document.querySelector("video")?.duration || 10) * 1000 : STATUS_DURATION;
      const remaining = duration - elapsed;

      bar.style.transition = `width ${remaining}ms linear`;
      bar.style.width = "100%";
      scheduleNext(remaining);

      const video = document.querySelector("video");
      if (video && video.paused) {
        video.play();
      }

      updatePausePlayIcon();
    }

    function togglePausePlay() {
      if (isPaused) {
        resumeProgress();
      } else {
        pauseProgress();
      }
    }

    function updatePausePlayIcon() {
      const icon = document.querySelector("#pause-play-btn i");
      if (icon) {
        icon.classList.toggle("fa-play", isPaused);
        icon.classList.toggle("fa-pause", !isPaused);
      }
    }

    function showNext() {
      clearTimeout(progressTimeout);
      elapsed = 0;
      if (currentIndex < statuses.length - 1) {
        currentIndex++;
        renderStatus(currentIndex);
      } else {
        window.location.href = "/status/"; // Update path if needed
      }
    }

    function showPrevious() {
      clearTimeout(progressTimeout);
      elapsed = 0;
      if (currentIndex > 0) {
        currentIndex--;
        renderStatus(currentIndex);
      }
    }

    renderStatus(currentIndex);
  }
});




  
  
  
  function open_viewer_modal(statusId) {
    const modal = document.getElementById('viewerModal');
    modal.classList.add('show');
    statusViewerFatch(statusId);

    // Add click listener to close modal when clicking outside
    setTimeout(() => {
      document.addEventListener('click', outsideClick);
    }, 0);
  }

  function close_viewer_modal() {
    const modal = document.getElementById('viewerModal');
    modal.classList.remove('show');
    document.removeEventListener('click', outsideClick);
  }

  function outsideClick(event) {
    const modal = document.getElementById('viewerModal');
    const modalBox = document.querySelector('.viewer-modal-box');

    // If clicked outside modal-box but inside modal
    if (!modalBox.contains(event.target) && modal.classList.contains('show')) {
      close_viewer_modal();
    }
  }



  function statusViewerFatch(statusId) {
    fetch(`/status/viewers/${statusId}/`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        const viewerContainer = document.querySelector('.viewer-modal-content');
        viewerContainer.innerHTML = ''; // Clear existing content
  
        if (data.viewers && data.viewers.length > 0) {
          data.viewers.forEach(viewer => {
            const viewerElement = document.createElement('div');
            viewerElement.classList.add('viewer-item');
            viewerElement.innerHTML = `
              <div style="display:flex; align-items:center; gap:10px; margin:10px 0;color: black;">
                <img src="${viewer.profile_pic}" alt="Profile" style="height:20px; width:20px; border-radius:50%;">
                <span>${viewer.full_name}</span>
              </div>
            `;
            viewerContainer.appendChild(viewerElement);
          });
        } else {
          viewerContainer.innerHTML = `<p style="text-align:center;">No viewers yet.</p>`;
        }
      })
      .catch(error => {
        console.error('Error fetching viewer data:', error);
      });
  }
  

  function back() {
    window.history.back();
  }



