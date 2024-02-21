$(document).ready(function () {
  const inputFile = document.getElementById('input_profile_img');
  const fileNameDisplay = $('#file-name-display');

  if (inputFile) {
    inputFile.addEventListener('change', function () {
      if (inputFile.files.length > 0) {
        fileNameDisplay.text(inputFile.files[0].name);
        fileNameDisplay.addClass('file-selected');
      } else {
        fileNameDisplay.text('No file selected');
        fileNameDisplay.removeClass('file-selected');
      }
    });
  }
});
