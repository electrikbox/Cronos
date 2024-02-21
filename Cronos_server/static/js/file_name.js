$(document).ready(function () {
  const inputFile = document.getElementById('input_profile_img');
  const fileNameDisplay = document.getElementById('file-name-display');

  inputFile.addEventListener('change', function () {
    if (inputFile.files.length > 0) {
      fileNameDisplay.textContent = inputFile.files[0].name;
      fileNameDisplay.classList.add('file-selected');
    } else {
      fileNameDisplay.textContent = 'No file selected';
      fileNameDisplay.classList.remove('file-selected');
    }
  });
});
