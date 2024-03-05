$(document).ready(function() {
  const carouselSlides = $(".carousel-slide");
  const lightbox = $("#lightbox");
  const lightboxImg = $("#lightbox-img");

  function centerLightbox() {
    const windowWidth = $(window).width();
    const windowHeight = $(window).height();
    const lightboxWidth = lightboxImg.width();
    const lightboxHeight = lightboxImg.height();

    const top = (windowHeight - lightboxHeight) / 2;
    const left = (windowWidth - lightboxWidth) / 2;

    lightbox.css({
        top: top,
        left: left
    });
  }

  // Make the lightbox appear when clicking on a slide
  carouselSlides.on('click', function() {
    const imgSrc = $(this).attr('src');
    lightboxImg.attr('src', imgSrc);
    lightbox.fadeIn(300);
    centerLightbox();
  });

  // Close the lightbox when clicking on the close button or outside the lightbox
  $('#close-lightbox, #lightbox').on('click', function() {
    lightbox.fadeOut(300);
  });

  // Center the lightbox when the window is resized
  $(window).on('resize', function() {
    centerLightbox();
  });
});
