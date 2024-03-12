// Toggle the answer when clicking on the question

$(document).ready(function () {
  $('.toggle-answer, .h4-help').click(function () {
    // Find the closest question or tutorial
    const question = $(this).closest('.question, .tuto, .about-us-faq');
    const answer = question.find('.answer');
    // Toggle the answer
    answer.slideToggle();
    // Change the arrow
    question.find('.toggle-answer').toggleClass('open');

    if (question.find('.toggle-answer').hasClass('open')) {
      question.find('.toggle-answer').html('▽');
    } else {
      question.find('.toggle-answer').html('▶︎');
    }
  });
});


// Toggle the block when clicking on the title

$(document).ready(function () {
  $('.toggle-collapse').click(function () {
    const collapse = $(this).closest('.block-title').next('.collapse');
    collapse.slideToggle();

    $(this).toggleClass('open');

    const button = $(this).closest('.block-title').find('.toggle-collapse-button');
    button.toggleClass('open');

    if (button.hasClass('open')) {
      button.html('▽');
    } else {
      button.html('◀︎');
    }
  });

  $('.toggle-collapse-button').click(function (event) {
    // Prevent the click event from bubbling up to the parent element
    event.stopPropagation();

    const collapse = $(this).closest('.block-title').next('.collapse');
    collapse.toggleClass('open');

    if (collapse.hasClass('open')) {
      collapse.slideDown();
      $(this).html('▽');
    } else {
      collapse.slideUp();
      $(this).html('◀︎');
    }
  });
});
