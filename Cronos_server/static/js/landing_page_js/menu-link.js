$(document).ready(function () {
  $('a[href^="#"]').on('click', function (event) {
    var target = $(this.getAttribute('href'));
    if (target.length) {
      event.preventDefault();
      $('html, body').animate({
        scrollTop: target.offset().top - 50
      }, 0);
    }
  });

  $(window).on('scroll', function () {
    var scrollPosition = $(window).scrollTop();

    $('.main-block').each(function () {
      const sectionTop = $(this).offset().top - 170;
      const sectionBottom = scrollPosition + 68;

      if (scrollPosition >= sectionTop && scrollPosition <= sectionBottom) {
        const currentSectionId = $(this).attr('id');

        $('#landing-menu li').removeClass('menu-active');
        $('#landing-menu li').addClass('menu-inactive');
        $('#landing-menu li').find('a[href="#' + currentSectionId + '"]').parent().removeClass('menu-inactive');
        $('#landing-menu li').find('a[href="#' + currentSectionId + '"]').parent().addClass('menu-active');
      }
    });
  });
});
