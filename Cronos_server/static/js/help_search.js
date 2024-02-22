$(document).ready(function () {
  $('#searchInput').on('input', function () {
    const query = $(this).val().toLowerCase();
    $('.question, .tuto').each(function () {
      const questionText = $(this).find('h3').text().toLowerCase();
      const answerText = $(this).find('.answer').text().toLowerCase();
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
