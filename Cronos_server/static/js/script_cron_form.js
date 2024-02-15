$(document).ready(function () {
  const csrfTokenInput = $('input[name=csrfmiddlewaretoken]');

  // Change day field to * when the other is selected
  $('#dow, #dom').change(function () {
    const selectedValue = $(this).val();
    const dayOfWeek = $('#dow');
    const dayOfMonth = $('#dom');

    const otherField = $(this).is(dayOfWeek) ? dayOfMonth : dayOfWeek;

    if (selectedValue !== '*') {
      otherField.val('*');
    }
  });

  // Delete cron
  $('.delete-cron').click(function () {
    const cronId = $(this).data('cron-id');
    const confirmation = confirm('Are you sure you want to delete this cron?');
    const row = $(this).closest('.cron');

    if (confirmation) {
      $.ajax({
        url: `/api/crons/${cronId}/delete/`,
        type: 'POST',
        data: {
          csrfmiddlewaretoken: csrfTokenInput.val()
        },
        success: function (response) {
          row.remove();
        },
        error: function (xhr) {
          console.log(`${xhr.status}: ${xhr.responseText}`);
          alert('Failed to delete cron');
        }
      });
    }
  });

  // Function to update button icon based on is_paused state
  function updateButtonIcon(button, isPaused) {
    const icon = button.find('ion-icon');
    icon.attr('name', isPaused ? 'play-circle-outline' : 'pause-circle-outline');
  }

  // Function to update cron status in database
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

  // Function to handle AJAX errors
  function handleAjaxError(xhr) {
    console.error('AJAX request failed:', xhr.status, xhr.responseText);
    alert('Failed to perform the operation. Please try again.');
  }

  // Function to update buttons on page load
  function updateButtonsOnLoad() {
    $('.pause-cron').each(function () {
      const button = $(this);
      const cronId = button.data('cron-id');

      $.ajax({
        url: `/api/crons/${cronId}/`,
        type: 'GET',
        // data: { csrfmiddlewaretoken: csrfTokenInput.val() },
        success: function (response) {
          // console.log('Cron status retrieved successfully');
          updateButtonIcon(button, response.is_paused);
        },
        error: handleAjaxError
      });
    });
  }

  // Call the function to update buttons on page load
  updateButtonsOnLoad();

  // Event handling for clicks on pause-cron buttons
  $('.pause-cron').click(function () {
    const button = $(this);
    const cronId = button.data('cron-id');

    $.ajax({
      url: `/api/crons/${cronId}/`,
      type: 'GET',
      // data: { csrfmiddlewaretoken: csrfTokenInput.val() },
      success: function (response) {
        console.log('Cron status retrieved successfully');
        const newIsPaused = !response.is_paused;
        updateCronStatus(button, cronId, newIsPaused);
        updateButtonIcon(button, newIsPaused);
      },
      error: handleAjaxError
    });
  });
});
