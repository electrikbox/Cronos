document.addEventListener('DOMContentLoaded', function () {
  const inputFile = document.getElementById('input_profile_img');

  inputFile.addEventListener('change', function () {
    const fileNameDisplay = document.getElementById('file-name-display');

    if (inputFile.files.length > 0) {
      fileNameDisplay.textContent = inputFile.files[0].name;
    } else {
      fileNameDisplay.textContent = 'No file selected';
    }
  });
});
