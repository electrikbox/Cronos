$(document).ready(function () {

  document.cookie.split(';').forEach(function (cookie) {
    const parts = cookie.split('=');
    console.log(parts);
  });

  const csrfTokenInput = $('input[name=csrfmiddlewaretoken]');
  const deleteSelectedButton = $('.delete-selected');
  const pauseSelectedButton = $('.pause-selected');

  function updateDeleteSelectedButtonState() {
    const checkedCrons = $('.cron-test input[type="checkbox"]:checked');
    const isEnabled = checkedCrons.length > 0;
    deleteSelectedButton.prop('disabled', !isEnabled);
    pauseSelectedButton.prop('disabled', !isEnabled);
  }

  $('.cron-test input[type="checkbox"]').change(updateDeleteSelectedButtonState);

  // Function to delete a single cron
  function deleteCron(cronId, row) {
    // const userToken = cookie.get('user_token');

    $.ajax({
      url: `/api/crons/${cronId}/delete/`,
      type: 'POST',
      headers: {
          // 'Authorization': `Token ${userToken}`,
          'X-CSRFToken': csrfTokenInput.val()
      },
      success: function (response) {
          row.remove();
      },
      error: function (xhr) {
          console.error(`${xhr.status}: ${xhr.responseText}`);
          alert('Failed to delete cron');
      }
  });
  }

  $('.select-all').click(function () {
    $('.cron_form_list .cron-test input[type="checkbox"]').click();
    getSelectedCronIds();
  });

  // Delete cron (individual)
  $('.delete-cron').click(function (event) {
    event.stopPropagation(); // Empêche la propagation de l'événement au parent

    const cronId = $(this).data('cron-id');
    const row = $(this).closest('.cron-test');

    const confirmation = confirm('Are you sure you want to delete this cron?');
    if (confirmation) {
      deleteCron(cronId, row);
    }
  });

  function deleteMultipleCrons(cronIds) {
    $.ajax({
      url: '/api/delete-multiple/',
      type: 'POST',
      data: JSON.stringify({ ids: Object.keys(cronIds) }),
      contentType: 'application/json',
      success: function (response) {
        console.log('Les crons ont été supprimés avec succès.');
        Object.values(cronIds).forEach(function (row) {
          row.remove();
          $('.select-all').prop('checked', false);
          updateDeleteSelectedButtonState();
        });
      },
      error: function (xhr, status, error) {
        console.error('Erreur lors de la suppression des crons:', error);
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
      const confirmation = confirm('Êtes-vous sûr de vouloir supprimer ces crons?');
      if (confirmation) {
        deleteMultipleCrons(selectedCronIds);
      }
    } else {
      alert('Veuillez sélectionner au moins un cron à supprimer.');
    }
  });

  updateDeleteSelectedButtonState();
});
