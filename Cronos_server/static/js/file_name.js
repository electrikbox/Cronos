$(document).ready(function() {
  $('#input_profile_img').change(function() {
      const fileNameDisplay = $('#file-name-display');

      if (this.files.length > 0) {
          fileNameDisplay.text(this.files[0].name);
      } else {
          fileNameDisplay.text('No file selected');
      }
  });
});
