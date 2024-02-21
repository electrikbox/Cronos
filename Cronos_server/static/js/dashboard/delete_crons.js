$(document).ready(function () {

  const csrfTokenInput = $('input[name=csrfmiddlewaretoken]');

  function updateDeleteSelectedButtonState() {
    const checkedCrons = $('.cron-test input[type="checkbox"]:checked');
    const isEnabled = checkedCrons.length > 0;
    $('.delete-selected').prop('disabled', !isEnabled);
    $('.pause-selected').prop('disabled', !isEnabled);
    $('.play-selected').prop('disabled', !isEnabled);
  }

  $('.cron-test input[type="checkbox"]').change(updateDeleteSelectedButtonState);

  // Delete cron
  $('.delete-cron').click(function () {
    const cronId = $(this).data('cron-id');
    const confirmation = confirm('Are you sure you want to delete this cron?');
    const row = $(this).closest('.cron-test');
    $('.loader').show();

    if (confirmation) {
      $.ajax({
        url: `/api/crons/${cronId}/delete/`,
        type: 'POST',
        data: {
          csrfmiddlewaretoken: csrfTokenInput.val()
        },
        success: function (response) {
          row.remove();
          window.location.href = "/dashboard?delete=true";
        },
        error: function (xhr) {
          console.log(`${xhr.status}: ${xhr.responseText}`);
          alert('Failed to delete cron');
        }
      });
    }
  });

  $('.select-all').click(function () {
    $('.cron_form_list .cron-test input[type="checkbox"]').click();
    getSelectedCronIds();
  });

  function deleteMultipleCrons(cronIds) {
    $.ajax({
      url: '/api/delete-multiple/',
      type: 'POST',
      headers: {
        'X-CSRFToken': csrfTokenInput.val()
      },
      data: JSON.stringify({ ids: Object.keys(cronIds) }),
      contentType: 'application/json',
      success: function (response) {
        console.log('Crons deleted successfully.');
        Object.values(cronIds).forEach(function (row) {
          row.remove();
          $('.select-all').prop('checked', false);
          updateDeleteSelectedButtonState();
          window.location.href = "/dashboard?deletes=true";
        });
      },
      error: function (xhr, status, error) {
        console.error('Delete crons error:', error);
      }
    });
  }

  function getSelectedCronIds() {
    const selectedCronIds = {};
    $('.cron-test input[type="checkbox"]:checked').each(function () {
      const cronId = $(this).closest('.cron-test').find('.delete-cron').data('cron-id');
      const row = $(this).closest('.cron-test');
      selectedCronIds[cronId] = row;
    });
    return selectedCronIds;
  }

  $('.delete-selected').click(function () {
    const selectedCronIds = getSelectedCronIds();
    const numSelectedCrons = Object.keys(selectedCronIds).length;
    if (numSelectedCrons > 0) {
      const confirmation = confirm('Are you shure you want to delete cron ?');
      if (confirmation) {
        $('.loader').show();
        deleteMultipleCrons(selectedCronIds);
      }
    } else {
      alert('Please select at least 1 cron.');
    }
  });

  updateDeleteSelectedButtonState();
});
