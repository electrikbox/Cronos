$(document).ready(function () {
  $('.toggle-answer').click(function () {
    const question = $(this).closest('.question, .tuto');
    const answer = question.find('.answer');
    answer.slideToggle();
    $(this).toggleClass('open');

    if ($(this).hasClass('open')) {
      $(this).html('▽');
    } else {
      $(this).html('▶︎');
    }
  });
});
