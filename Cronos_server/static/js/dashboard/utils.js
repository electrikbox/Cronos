$(document).ready(function () {

  $('select option[value="separator"]').prop('disabled', true);
  $('.copy_field').css('display', 'none');

  $('#id_command').change(function () {
    const command = $(this).val();
    if (command !== 'open') {
      $('.url_field').css('display', 'none');
      $('.copy_field').css('display', 'block');
    } else {
      $('.url_field').css('display', 'block');
      $('.copy_field').css('display', 'none');
    }
  });
});
