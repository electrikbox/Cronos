$(document).ready(function () {
  let slideIndex = 0;
  let $slides = $('.gallery-app-img');

  carousel();

  function carousel() {
    $slides.eq(slideIndex).fadeIn(1000);

    setTimeout(function () {
      $slides.hide();
      slideIndex++;
      if (slideIndex >= $slides.length) {
        slideIndex = 0;
      }
      carousel();
    }, 6000);
  }
});
