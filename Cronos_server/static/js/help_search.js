// Search bar for the help page

$(document).ready(function () {
  $('#searchInput').on('input', function () {
    const query = $(this).val().toLowerCase();
    // Hide all questions and tutorials
    $('.question, .tuto').each(function () {
      // Check if the question or answer contains the query
      const questionText = $(this).find('h3, h4').text().toLowerCase();
      const answerText = $(this).find('.answer').text().toLowerCase();
      if (
        // If the question or answer contains the query, show it
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
