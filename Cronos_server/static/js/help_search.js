$(document).ready(function () {
  $('#searchInput').on('input', function () {
    var query = $(this).val().toLowerCase();
    $('.question, .tuto').each(function () {
      var questionText = $(this).find('h3').text().toLowerCase();
      var answerText = $(this).find('.answer').text().toLowerCase();
      if (
        questionText.indexOf(query) !== -1 ||
        answerText.indexOf(query) !== -1
      ) {
        $(this).show();
      } else {
        $(this).hide();
      }
    });
  });
});
