$(document).ready(function () {
  $('.toggle-answer').click(function () {
    var question = $(this).closest('.question, .tuto');
    var answer = question.find('.answer');
    answer.slideToggle();
    $(this).toggleClass('open');

    if ($(this).hasClass('open')) {
      $(this).html('▽');
    } else {
      $(this).html('▶︎');
    }
  });
});
