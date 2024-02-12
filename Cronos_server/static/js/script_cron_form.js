$(document).ready(function() {
  // Gestion du changement des sélecteurs
  $('#id_day_of_week, #id_day_of_month').change(function() {
    const selectedValue = $(this).val();
    const dayOfWeek = $('#id_day_of_week');
    const dayOfMonth = $('#id_day_of_month');
    const otherField = $(this).is(dayOfWeek) ? dayOfMonth : dayOfWeek;

    if (selectedValue !== '*') {
      otherField.val('*');
    }
  });

  $('.delete-cron').click(function() {
    const cronId = $(this).data('cron-id');
    const confirmation = confirm('Are you sure you want to delete this cron?');

    if (confirmation) {
      $.post(`/api/crons/${cronId}/delete/`, {
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
      })
      .done(function(response) {
        location.reload();
      })
      .catch(function(xhr) {
        console.log(`${xhr.status}: ${xhr.responseText}`);
        alert('Failed to delete cron');
      });
    }
  });

  // Gestion de la soumission du formulaire
  // $('#cron-create-form').submit(function(e) {
  //   e.preventDefault(); // Empêche l'envoi par défaut du formulaire

  //   $.post('http://localhost:8000/dashboard/', $(this).serialize())
  //     .done(function(response) {
  //       $('#cron-list-container').html(response);
  //       $('#cron-create-form')[0].reset();
  //     })
  //     .catch(function(xhr) {
  //       console.log(xhr.status + ": " + xhr.responseText);
  //       var errors = xhr.responseJSON.error;
  //       for (var key in errors) {
  //         $('#' + key + '-error').text(errors[key][0]);
  //       }
  //     });
  // });
});

