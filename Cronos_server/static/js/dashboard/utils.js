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

    if (command === 'ls') {
      $('.help_create_text').text('ℹ️ This command will list all files founded with the name you enter to a txt file inside Cronos folder in your personal directory. you can use \'*\' to select all files name with the given extension (exemple: *.gif).');
    } else if (command === 'cp') {
      $('.help_create_text').text('ℹ️ This command will copy all files founded with the name you enter to a folder inside Cronos folder in your personal directory. you can use \'*\' to select all files name with the given extension (exemple: *.gif).');
    } else if (command === 'open') {
      $('.help_create_text').text('ℹ️ This command will simply open the given url in your brower.');
    } else {
      $('.help_create_text').text('');
    }
  }

  $('#id_command').change(function () {
    updateCopyField();
  });
});
