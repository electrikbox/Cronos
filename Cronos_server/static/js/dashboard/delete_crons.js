// Used to delete crons from the dashboard

$(document).ready(function () {

  const access_token = localStorage.getItem('access_token');
  const csrfTokenInput = $('input[name=csrfmiddlewaretoken]');

  /**
   * Updates the state of the delete selected button based on the number of checked crons
   */
  function updateDeleteSelectedButtonState() {
    const checkedCrons = $('.cron-full input[type="checkbox"]:checked');
    const isEnabled = checkedCrons.length > 0;
    $('.delete-selected').prop('disabled', !isEnabled);
    $('.pause-selected').prop('disabled', !isEnabled);
    $('.play-selected').prop('disabled', !isEnabled);
  }

  /**
   * Deletes a cron
   */
  function deleteCron() {
    const cronId = $(this).data('cron-id');
    const confirmation = confirm('Are you sure you want to delete this cron ?');
    const row = $(this).closest('.cron-full');
    $('.loader').show();

    if (confirmation) {
      $.ajax({
        url: `/api/crons/${cronId}/delete/`,
        type: 'POST',
        headers: {
          'Authorization': `Bearer ${access_token}`
        },
        data: {
          csrfmiddlewaretoken: csrfTokenInput.val()
        },
        success: function (response) {
          row.remove();
          window.location.href = "/dashboard?delete=true";
        },
        error: function (xhr) {
          alert('Please login again');
          window.location.href = "/accounts/logout/?next=/dashboard/"; // <------- redirect to login page
        }
      });
    }
  }

  /**
   * Deletes multiple crons
   * @param {Object} cronIds - The cron IDs to be deleted
   */
  function deleteMultipleCrons(cronIds) {

    $.ajax({
      url: '/api/delete-multiple/',
      type: 'POST',
      headers: {
        'Authorization': `Bearer ${access_token}`,
        'X-CSRFToken': csrfTokenInput.val()
      },
      data: JSON.stringify({ ids: Object.keys(cronIds) }),
      contentType: 'application/json',
      success: function (response) {
        console.log('Crons deleted successfully');
        Object.values(cronIds).forEach(function (row) {
          row.remove();
          $('.select-all').prop('checked', false);
          updateDeleteSelectedButtonState();
          window.location.href = "/dashboard?deletes=true";
        });
      },
      error: function (xhr, status, error) {
        alert('Please login again');
        window.location.href = "/accounts/logout/?next=/dashboard/"; // <------- redirect to login page
      }
    });
  }

  /**
   * Retrieves the selected cron IDs and their corresponding rows
   * @returns {Object} An object containing the selected cron IDs as keys and their corresponding rows as values
   */
  function getSelectedCronIds() {
    const selectedCronIds = {};
    $('.cron-full input[type="checkbox"]:checked').each(function () {
      const cronId = $(this).closest('.cron-full').find('.delete-cron').data('cron-id');
      const row = $(this).closest('.cron-full');
      selectedCronIds[cronId] = row;
    });
    return selectedCronIds;
  }

  /**
   * Deletes the selected cron jobs
   */
  function deleteSelected() {
    const selectedCronIds = getSelectedCronIds();
    const numSelectedCrons = Object.keys(selectedCronIds).length;
    if (numSelectedCrons > 0) {
      const confirmation = confirm('Are you sure you want to delete this cron ?');
      if (confirmation) {
        $('.loader').show();
        deleteMultipleCrons(selectedCronIds);
      }
    } else {
      alert('Please select at least 1 cron');
    }
  }

  // =======================  Event Listeners  =======================

  updateDeleteSelectedButtonState();

  // delete selected crons
  $('.delete-selected').click(deleteSelected);

  // change state of buttons
  $('.cron-full input[type="checkbox"]').change(updateDeleteSelectedButtonState);

  // delete 1 cron
  $('.delete-cron').click(deleteCron);

  // select all crons
  $('.select-all').click(function () {
    $('.cron_form_list-div .cron-full input[type="checkbox"]').click();
    getSelectedCronIds();
  });
});
