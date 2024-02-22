$(document).ready(function () {

  $('#id_day_of_week, #id_day_of_month').change(function () {
    const selectedValue = $(this).val();
    const dayOfWeek = $('#id_day_of_week');
    const dayOfMonth = $('#id_day_of_month');

    const otherField = $(this).is(dayOfWeek) ? dayOfMonth : dayOfWeek;

    if (selectedValue !== '*') {
      otherField.val('*');
    }
  });
});
