$(document).ready(function () {
  // Change day field to * when the other is selected
  $('#id_day_of_week, #id_day_of_month').change(function () {
    const selectedValue = $(this).val();
    const dayOfWeek = $('#id_day_of_week');
    const dayOfMonth = $('#id_day_of_month');
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
          csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
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

  // Update pause cron button
  function updateButtonIcon(button, isPaused) {
    const icon = button.find('ion-icon');
    if (!isPaused) {
      icon.attr('name', 'pause-circle-outline');
    } else {
      icon.attr('name', 'play-circle-outline');
    }
  }

  // Update cron status in database
  function updateCronStatus(button, cronId, isPaused) {
    $.ajax({
      url: `/api/crons/${cronId}/update/`,
      type: 'POST',
      data: {
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        is_paused: isPaused
      },
      success: function (response) {
        console.log('Cron status updated successfully, is_paused:', isPaused);
      },
      error: function (xhr) {
        console.error('Failed to update cron status:', xhr.status, xhr.responseText);
        alert('Failed to update cron status');
      }
    });
  }

  // Update buttons on page load
  function updateButtonsOnLoad() {
    $('.pause-cron').each(function () {
      const button = $(this);
      const cronId = button.data('cron-id');

      $.ajax({
        url: `/api/crons/${cronId}/`,
        type: 'GET',
        data: {
          csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (response) {
          console.log('Cron status retrieved successfully');
          updateButtonIcon(button, response.is_paused);
        },
        error: function (xhr) {
          console.error('Failed to retrieve cron status:', xhr.status, xhr.responseText);
          alert('Failed to retrieve cron status');
        }
      });
    });
  }

  updateButtonsOnLoad();

  // Pause cron
  $('.pause-cron').click(function () {
    const button = $(this);
    const cronId = button.data('cron-id');

    $.ajax({
      url: `/api/crons/${cronId}/`,
      type: 'GET',
      data: {
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
      },
      success: function (response) {
        console.log('Cron status retrieved successfully');
        const newIsPaused = !response.is_paused;
        updateCronStatus(button, cronId, newIsPaused);
        updateButtonIcon(button, newIsPaused);
      },
      error: function (xhr) {
        console.error('Failed to retrieve cron status:', xhr.status, xhr.responseText);
        alert('Failed to retrieve cron status');
      }
    });
  });

});
