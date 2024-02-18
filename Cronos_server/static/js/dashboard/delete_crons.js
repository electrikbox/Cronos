$(document).ready(function () {

  const csrfTokenInput = $('input[name=csrfmiddlewaretoken]');
  const deleteSelectedButton = $('.delete-selected');
  const pauseSelectedButton = $('.pause-selected');

  function updateDeleteSelectedButtonState() {
    const checkedCrons = $('.cron input[type="checkbox"]:checked');
    const isEnabled = checkedCrons.length > 0;
    deleteSelectedButton.prop('disabled', !isEnabled);
    pauseSelectedButton.prop('disabled', !isEnabled);
  }

  $('.cron input[type="checkbox"]').change(updateDeleteSelectedButtonState);

  async function deleteCron(cronId, row) {
      try {
        const response = await fetch(`/api/crons/${cronId}/delete/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfTokenInput.val()
          }
        });
        if (!response.ok) {
          throw new Error('Failed to delete cron');
        }
        row.remove();
      } catch (error) {
        console.error('Delete cron error:', error);
        alert('Failed to delete cron');
      }
    }

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
        });
      },
      error: function (xhr, status, error) {
        console.error('Erreur lors de la suppression des crons:', error);
      }
    });
  }

  function getSelectedCronIds() {
    const selectedCronIds = {};
    $('.cron input[type="checkbox"]:checked').each(function () {
      const cronId = $(this).closest('.cron').find('.delete-cron').data('cron-id');
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
