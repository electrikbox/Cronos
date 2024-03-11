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
      var sectionTop = $(this).offset().top - 200;
      var sectionBottom = sectionTop + $(this).innerHeight();

      if (scrollPosition >= sectionTop && scrollPosition <= sectionBottom) {
        var currentSectionId = $(this).attr('id');

        $('#landing-menu li').removeClass('menu-active');
        $('#landing-menu li').addClass('menu-inactive');
        $('#landing-menu li').find('a[href="#' + currentSectionId + '"]').parent().removeClass('menu-inactive');
        $('#landing-menu li').find('a[href="#' + currentSectionId + '"]').parent().addClass('menu-active');
      }
    });
  });
});
