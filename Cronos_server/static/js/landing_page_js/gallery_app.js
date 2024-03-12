$(document).ready(function () {
  let slideIndex = 0;
  let $slides = $('.gallery-app-img');

  carousel();

  function carousel() {
    $slides.eq(slideIndex).fadeIn(2000);

    setTimeout(function () {
      $slides.eq(slideIndex).fadeOut(1000, function() {
        $(this).css('display', 'none');

        slideIndex++;
        if (slideIndex >= $slides.length) {
          slideIndex = 0;
        }

        $slides.eq(slideIndex).fadeIn(2000);

        carousel();
      });
    }, 5000);
  }
});

