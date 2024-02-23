// Toggle the answer when clicking on the question

$(document).ready(function () {
  $('.toggle-answer').click(function () {
    // Find the closest question or tutorial
    const question = $(this).closest('.question, .tuto');
    const answer = question.find('.answer');
    // Toggle the answer
    answer.slideToggle();
    // Change the arrow
    $(this).toggleClass('open');

    if ($(this).hasClass('open')) {
      $(this).html('▽');
    } else {
      $(this).html('▶︎');
    }
  });
});
