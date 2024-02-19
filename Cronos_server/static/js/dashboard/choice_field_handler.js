$(document).ready(function () {

  $('#dow, #dom').change(function () {
    const selectedValue = $(this).val();
    const dayOfWeek = $('#dow');
    const dayOfMonth = $('#dom');

    const otherField = $(this).is(dayOfWeek) ? dayOfMonth : dayOfWeek;

    if (selectedValue !== '*') {
      otherField.val('*');
    }
  });
});
