$(document).ready(function () {

  function updatePauseButtonsOnLoad() {
    $('.pause-cron').each(function () {
      const button = $(this);
      const cronId = button.data('cron-id');

      $.ajax({
        url: `/api/crons/${cronId}/`,
        type: 'GET',
        success: function (response) {
          updateButtonIcon(button, response.is_paused);
        },
        error: function (xhr) {
          console.log(`${xhr.status}: ${xhr.responseText}`);
          alert('Failed to get crons');
        }
      });
    });
    // Deselect all checkboxes after loading buttons
    $('.cron-test input[type="checkbox"]').prop('checked', false);
    updateSelectedButtonState();
  }

  function togglePauseButton(is_paused) {
    const selectedCronIds = getSelectedPauseCronIds();
    const numSelectedCrons = Object.keys(selectedCronIds).length;

    if (numSelectedCrons <= 0) {
      alert('Please select at least 1 cron.');
      return;
    }
    pauseMultipleCrons(selectedCronIds, is_paused);
    // Deselect all checkboxes after operation
    $('.cron-test input[type="checkbox"]').prop('checked', false);
    updateSelectedButtonState();
  }

  const csrfTokenInput = $('input[name=csrfmiddlewaretoken]');

  // Function to update cron status in database to pause
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
      },
      error: function (xhr) {
        console.error('AJAX request failed:', xhr.status, xhr.responseText);
        alert('Failed to perform the operation. Please try again.');
      }
    });
  });

  // Function to update the icon of the pause-cron button
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

  // Multi pause
  function getSelectedPauseCronIds() {
    const selectedCronIds = {};
    $('.cron-test input[type="checkbox"]:checked').each(function () {
      const cronId = $(this).closest('.cron-test').find('.pause-cron').data('cron-id');
      const row = $(this).closest('.cron-test');
      selectedCronIds[cronId] = row;
    });
    return selectedCronIds;
  }

  function updateSelectedButtonState() {
    const checkedCrons = $('.cron-test input[type="checkbox"]:checked');
    const isEnabled = checkedCrons.length > 0;
    $('.delete-selected').prop('disabled', !isEnabled);
    $('.pause-selected').prop('disabled', !isEnabled);
    $('.play-selected').prop('disabled', !isEnabled);
  }

  function pauseMultipleCrons(cronIds, is_paused) {
    $.ajax({
      url: '/api/pause-multiple/',
      type: 'POST',
      headers: {
        'X-CSRFToken': csrfTokenInput.val()
      },
      data: JSON.stringify({ ids: Object.keys(cronIds), is_paused: is_paused }),
      contentType: 'application/json',
      success: function (response) {
        console.log('Crons have been paused successfully.');
        Object.values(cronIds).forEach(function (row) {
          $('.select-all').prop('checked', false);
          // updateSelectedButtonState();
          // updatePauseButtonsOnLoad(); // <------- à remplacer pour eviter les multiples requetes
        });
        window.location.href = "/dashboard?pause=true"; // <------- reload page
      },
      error: function (xhr, status, error) {
        console.error('Error pausing crons:', error);
      }
    });
  }

  // Handling pause-selected button click
  $('.pause-selected').click(function () {
    togglePauseButton(true);
    $('.loader').show();
  });

  // Handling play-selected button click
  $('.play-selected').click(function () {
    togglePauseButton(false);
    $('.loader').show();
  });

  // Initial update of pause buttons
  updatePauseButtonsOnLoad();

});
