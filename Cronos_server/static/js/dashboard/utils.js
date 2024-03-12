$(document).ready(function () {
  updateCopyField();

  $('select option[value="separator"]').prop('disabled', true);
  // $('.copy_field').css('display', 'none');

  function updateCopyField() {
    const command = $('#id_command').val();
    if (command === 'cp' || command === 'ls') {
      $('.url_field').css('display', 'none');
      $('.copy_field').css('display', 'block');
      $('.help_create_text').css('display', 'block');
    } else if (command === 'open'){
      $('.url_field').css('display', 'block');
      $('.copy_field').css('display', 'none');
      $('.help_create_text').css('display', 'block');
    } else {
      $('.url_field').css('display', 'none');
      $('.copy_field').css('display', 'none');
    }

    if (command === 'ls') {
      $('.help_create_text').html(
        "ℹ️ This command will <strong>list all files</strong> founded with the name you entered in a txt file inside Cronos folder in your home directory. Special character <strong>'*'</strong> can be used to select all file names with the given extension (ex: *.gif)"
      );
    } else if (command === 'cp') {
      $('.help_create_text').html(
        "ℹ️ This command will <strong>copy all files</strong> bearing the name you entered into a folder inside Cronos folder in your home directory. Special character <strong>'*'</strong> can be used to select all files with the given extension (ex: *.gif)"
      );
    } else if (command === 'open') {
      $('.help_create_text').html(
        'ℹ️ This command simply <strong>opens the given url</strong> in a new tab in your default brower'
      );
    } else {
      $('.help_create_text').text('').css('display', 'none');
    }
  }

  $('#id_command').change(function () {
    updateCopyField();
  });
});
