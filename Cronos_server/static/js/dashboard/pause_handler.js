// Pauses and resumes crons on the dashboard

$(document).ready(function () {

  const access_token = localStorage.getItem('access_token');
  const csrfTokenInput = $('input[name=csrfmiddlewaretoken]');

  /**
   * Updates the pause buttons on page load
   */
  function updatePauseButtonsOnLoad() {
    $('.pause-cron').each(function () {
      const button = $(this);
      const cronId = button.data('cron-id');

      $.ajax({
        url: `/api/crons/${cronId}/`,
        type: 'GET',
        headers: {
          'Authorization': `Bearer ${access_token}`
        },
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
    $('.cron-full input[type="checkbox"]').prop('checked', false);
    updateSelectedButtonState();
  }

  /**
   * Toggles the pause button for selected crons
   *
   * @param {boolean} is_paused - Indicates whether the crons should be paused or resumed
   * @returns {void}
   */
  function togglePauseButton(is_paused) {
    const selectedCronIds = getSelectedPauseCronIds();
    const numSelectedCrons = Object.keys(selectedCronIds).length;

    if (numSelectedCrons <= 0) {
      alert('Please select at least 1 cron');
      return;
    }
    pauseMultipleCrons(selectedCronIds, is_paused);
    // Deselect all checkboxes after operation
    $('.cron-full input[type="checkbox"]').prop('checked', false);
    updateSelectedButtonState();
  }

  /**
   * Toggles the pause state of a cron job
   *
   * @param {string} cronId - The ID of the cron job
   * @param {jQuery} button - The button element that triggered the pause toggle
   */
  function pauseToggle(cronId, button) {
    const currentIcon = button.find('ion-icon').attr('name');
    const isCurrentlyPaused = currentIcon === 'play-circle-outline';
    console.log('currentIcon:', currentIcon);
    console.log('isCurrentlyPaused:', isCurrentlyPaused);

    const newIsPaused = !isCurrentlyPaused;

    $.ajax({
      url: `/api/crons/${cronId}/update/`,
      type: 'PUT',
      headers: {
        'Authorization': `Bearer ${access_token}`
      },
      data: { csrfmiddlewaretoken: csrfTokenInput.val(), is_paused: newIsPaused },
      success: function (response) {
        $('.loader').hide();
        updateButtonIcon(button, newIsPaused);
        setTimeout(reloadCronFormLogs, 500);
      },
      error: function (xhr) {
        alert('Please login again');
        window.location.href = "/accounts/logout/?next=/dashboard/"; // <------- redirect to login page
      }
    });
  }

  /**
   * Updates the button icon and styling based on the pause state
   * @param {jQuery} button - The button element to update
   * @param {boolean} isPaused - The pause state
   */
  function updateButtonIcon(button, isPaused) {
    const icon = button.find('ion-icon');
    icon.attr('name', isPaused ? 'play-circle-outline' : 'pause-circle-outline');
    const cronFullDiv = button.closest('.cron-full');
    if (isPaused) {
      cronFullDiv.addClass('paused');
    } else {
      cronFullDiv.removeClass('paused');
    }
  }

  /**
   * Retrieves the selected pause cron IDs along with their corresponding rows
   * @returns {Object} An object containing the selected cron IDs as keys and their corresponding rows as values
   */
  function getSelectedPauseCronIds() {
    const selectedCronIds = {};
    $('.cron-full input[type="checkbox"]:checked').each(function () {
      const cronId = $(this).closest('.cron-full').find('.pause-cron').data('cron-id');
      const row = $(this).closest('.cron-full');
      selectedCronIds[cronId] = row;
    });
    return selectedCronIds;
  }

  /**
   * Updates the state of the selected buttons based on the number of checked cron checkboxes
   */
  function updateSelectedButtonState() {
    const checkedCrons = $('.cron-full input[type="checkbox"]:checked');
    const isEnabled = checkedCrons.length > 0;
    $('.delete-selected').prop('disabled', !isEnabled);
    $('.pause-selected').prop('disabled', !isEnabled);
    $('.play-selected').prop('disabled', !isEnabled);
  }

  /**
   * Pauses multiple crons
   *
   * @param {Object} cronIds - The cron IDs to pause
   * @param {boolean} is_paused - Indicates whether the crons should be paused or not
   */
  function pauseMultipleCrons(cronIds, is_paused) {
    $.ajax({
      url: '/api/pause-multiple/',
      type: 'PUT',
      headers: {
        'Authorization': `Bearer ${access_token}`,
        'X-CSRFToken': csrfTokenInput.val()
      },
      data: JSON.stringify({ ids: Object.keys(cronIds), is_paused: is_paused }),
      contentType: 'application/json',
      success: function (response) {
        console.log('Crons have been paused successfully');
        Object.values(cronIds).forEach(function (row) {
          $('.select-all').prop('checked', false);
          updateSelectedButtonState();
        });
        window.location.href = "/dashboard?pause=true"; // <------- reload page
      },
      error: function (xhr, status, error) {
        alert('Please login again');
        window.location.href = "/accounts/logout/?next=/dashboard/"; // <------- redirect to login page
      }
    });
  }

  /**
   * Reloads the cron form logs by fetching the current URL and updating the logs section
   */
  function reloadCronFormLogs() {
    var currentUrl = window.location.href;
    $('.logs-div').load(currentUrl + ' .logs');
  }

  // =======================  Event Listeners  =======================

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

  $('.pause-cron').click(function () {
    const button = $(this);
    const cronId = button.data('cron-id');
    console.log('cronId:', cronId);

    pauseToggle(cronId, button);
    $('.loader').show();
  });

  updatePauseButtonsOnLoad();
});
