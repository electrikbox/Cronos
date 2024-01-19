$(document).ready(function () {
  $('#id_day_of_week').change(function () {
    var selectedDayOfWeek = $(this).val();
    var dayOfMonthField = $('#id_day_of_month');

    if (selectedDayOfWeek !== '*') {
      dayOfMonthField.val('*');
    }
  });
  $('#id_day_of_month').change(function () {
    var selectedDayOfMonth = $(this).val();
    var dayOfWeekField = $('#id_day_of_week');

    if (selectedDayOfMonth !== '*') {
      dayOfWeekField.val('*');
    }
  });
});