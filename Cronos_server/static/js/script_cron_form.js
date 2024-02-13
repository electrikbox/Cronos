$(document).ready(function () {
  // Gestion du changement des sélecteurs
  $('#id_day_of_week, #id_day_of_month').change(function () {
    const selectedValue = $(this).val();
    const dayOfWeek = $('#id_day_of_week');
    const dayOfMonth = $('#id_day_of_month');
    const otherField = $(this).is(dayOfWeek) ? dayOfMonth : dayOfWeek;

    if (selectedValue !== '*') {
      otherField.val('*');
    }
  });

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

  $('.pause-cron').click(function () {
    // Select p from nearest .cron class
    var paragraph = $(this).closest('.cron').find('p');

    // Check if color is not saved
    if (!paragraph.data('previous-color')) {
      paragraph.data('previous-color', paragraph.css('color'));
    }

    // Change color to grey if it's not grey, else restore previous color
    if (paragraph.css('color') === 'rgb(128, 128, 128)') {
      paragraph.css('color', paragraph.data('previous-color'));
    } else {
      paragraph.css('color', 'grey');
    }

    var icon = $(this).find('ion-icon');

    if (icon.attr('name') === 'pause-circle-outline') {
      icon.attr('name', 'play-circle-outline');
    } else {
      icon.attr('name', 'pause-circle-outline');
    }
  });
});
