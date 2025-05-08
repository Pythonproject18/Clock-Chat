  const statusDiv = document.querySelector('.status_text');

  const togglePlaceholder = () => {
    console.log("sajjbdjbshahdbmnsandsd");
    if (statusDiv.textContent.trim() === '') {
      statusDiv.classList.add('empty');
    } else {
      statusDiv.classList.remove('empty');
    }
  };

  statusDiv.addEventListener('input', togglePlaceholder);
  statusDiv.addEventListener('blur', togglePlaceholder);
  statusDiv.addEventListener('focus', togglePlaceholder);

  // Initialize on page load
  togglePlaceholder();
