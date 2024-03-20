// Slider for applicaion (landing page)

$(document).ready(function () {
  let slideIndex = 0;
  let $slides = $('.gallery-app-img');

  carousel();

  function carousel() {
    $slides.eq(slideIndex).fadeIn(2000); // apparition = 2 seconds

    setTimeout(function () {
      $slides.eq(slideIndex).fadeOut(1000, function() {
        // disparition = 1 second
        $(this).css('display', 'none');

        slideIndex++;
        if (slideIndex >= $slides.length) {
          slideIndex = 0;
        }

        $slides.eq(slideIndex).fadeIn(2000); // apparition = 2 seconds

        carousel();
      });
    }, 5000); // stop after 5 seconds
  }
});
