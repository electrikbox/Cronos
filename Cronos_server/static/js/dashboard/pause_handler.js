$(document).ready(function () {

  const csrfTokenInput = $('input[name=csrfmiddlewaretoken]');

  // Function to update cron status in database to pause
  // ==========================================================================
  function updateCronStatus(button, cronId, isPaused) {
    $.ajax({
      url: `/api/crons/${cronId}/update/`,
      type: 'POST',
      data: { csrfmiddlewaretoken: csrfTokenInput.val(), is_paused: isPaused },
      success: function (response) {
        console.log('Cron status updated successfully, is_paused:', isPaused);
      },
      error: function (xhr) {
        console.error('Failed to update cron status:', xhr.status, xhr.responseText);
        alert('Failed to update cron status');
      }
    });
  }

  // Handling clicks on pause-cron buttons
  // ==========================================================================
  $('.pause-cron').click(function () {
    const button = $(this);
    const cronId = button.data('cron-id');

    $.ajax({
      url: `/api/crons/${cronId}/`,
      type: 'GET',
      success: function (response) {
        const newIsPaused = !response.is_paused;
        updateCronStatus(button, cronId, newIsPaused);
        updateButtonIcon(button, newIsPaused);
        window.location.reload();
      },
      error: function (xhr) {
        console.error('AJAX request failed:', xhr.status, xhr.responseText);
        alert('Failed to perform the operation. Please try again.');
      }
    });
  });

  // Function to update the icon of the pause-cron button
  // ==========================================================================
  function updateButtonIcon(button, isPaused) {
    const icon = button.find('ion-icon');
    icon.attr('name', isPaused ? 'play-circle-outline' : 'pause-circle-outline');
    const cronTestDiv = button.closest('.cron-test');
    if (isPaused) {
      cronTestDiv.addClass('paused');
    } else {
      cronTestDiv.removeClass('paused');
    }
  }
});
