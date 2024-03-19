// Display a alert when click on windows download link

$(document).ready(function () {

  $('.wip_link').click(function (event) {
    event.preventDefault();
    alert(
      'Cronos-Connect Client is not yet available on Windows \n We apologize for the inconvenience'
    );
  });
});
