// Display a alert when click on a download link
$(document).ready(function () {

  $('.dl-link, .WiP').click(function (event) {
    event.preventDefault();
    alert('Download section under construction. Thank you for your patience');
  });
});
