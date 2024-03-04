$(document).ready(function() {
  const carouselContainer = $("#carousel-container");
  const carouselSlides = $(".carousel-slide");
  const slideWidth = carouselSlides.first().width();
  const slideGap = parseFloat(carouselContainer.css("gap"));
  let currentIndex = 0;
  let autoScrollInterval;

  function startAutoScroll() {
    autoScrollInterval = setInterval(nextSlide, 6000);
  }

  function stopAutoScroll() {
    clearInterval(autoScrollInterval);
  }

  function nextSlide() {
    const nextIndex = (currentIndex + 1) % carouselSlides.length;
    carouselSlides.eq(currentIndex).addClass('hidden');
    carouselSlides.eq(nextIndex).removeClass('hidden');
    const scrollAmount = (slideWidth + slideGap) * nextIndex;
    carouselContainer.animate({scrollLeft: scrollAmount}, 500);
    currentIndex = nextIndex;
  }

  startAutoScroll();

  // Stop auto scroll when mouse over a slide
  carouselSlides.on('mouseenter', function() {
    stopAutoScroll();
  });

  // Restart auto scroll when mouse leaves a slide
  carouselSlides.on('mouseleave', function() {
    startAutoScroll();
  });

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
