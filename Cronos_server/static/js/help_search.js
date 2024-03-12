// Search bar for the help page

$(document).ready(function () {
  function handleSearch(query) {
    // Hide all sections
    $('.faq-block, .tuto-block, .about-us-block').hide();

    // Show only sections containing the query
    $('.question, .tuto, .about-us-faq').each(function () {
      const questionText = $(this).find('h3, h4').text().toLowerCase();
      const answerText = $(this).find('.answer').text().toLowerCase();

      if (questionText.includes(query) || answerText.includes(query)) {
        const block = $(this).closest('.faq-block, .tuto-block, .about-us-block');
        block.show();

        // Open block if its answer contains the query
        if (answerText.includes(query)) {
          block.find('.collapse').slideDown();
          block.find('.toggle-collapse').addClass('open');
          block.find('.toggle-collapse-button').html('▽');

          $(this).find('.answer').slideDown();
          $(this).find('.toggle-answer').addClass('open').html('▽');
        }

        $(this).show();
      } else {
        $(this).hide();
      }
    });
  }

  // Handle search input
  $('#searchInput').on('input', function () {
    const query = $(this).val().toLowerCase();
    handleSearch(query);
  });
});
