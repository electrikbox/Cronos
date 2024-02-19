$(document).ready(function () {

  $('select option[value="separator"]').prop('disabled', true);

  $('#id_command').change(function () {
    const command = $(this).val();
    if (command !== 'open') {
      $('.url_field').css('display', 'none');
    } else {
      $('.url_field').css('display', 'block');
    }
  });
});
