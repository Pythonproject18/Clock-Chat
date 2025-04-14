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
