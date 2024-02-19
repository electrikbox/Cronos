$(document).ready(function () {

  function switchPendingStatus() {
    $.ajax({
      url: `/api/crons/`,
      type: 'GET',
      success: function (response) {
        response.forEach((cron, index) => {
          const pendingDiv = $(`.pending:eq(${index})`);
          const paragraph = pendingDiv.find('p');
          if (cron.validated) {
            pendingDiv.addClass('active');
            paragraph.text('Active');
          } else {
            pendingDiv.removeClass('active');
            paragraph.text('Pending');
          }
        });
      },
      error: function (xhr) {
        console.error('Failed to get users status:', xhr.status, xhr.responseText);
      }
    });
  }

  switchPendingStatus();

  let intervalId;
  intervalId = setInterval(switchPendingStatus, 5000);

  const stopTime = 1 * 20 * 1000;
  setTimeout(() => {
    clearInterval(intervalId);
  }, stopTime);
});
