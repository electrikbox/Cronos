$(document).ready(function () {
  updateCopyField();

  $('select option[value="separator"]').prop('disabled', true);
  // $('.copy_field').css('display', 'none');

  function updateCopyField() {
    const command = $('#id_command').val();
    if (command === 'cp' || command === 'ls') {
      $('.url_field').css('display', 'none');
      $('.copy_field').css('display', 'block');
    } else if (command === 'open'){
      $('.url_field').css('display', 'block');
      $('.copy_field').css('display', 'none');
    } else {
      $('.url_field').css('display', 'none');
      $('.copy_field').css('display', 'none');
    }
  }

  $('#id_command').change(function () {
    updateCopyField();
  });
});
