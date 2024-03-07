$(document).ready(function() {
  $(window).scroll(function() {
    const scrollPosition = $(this).scrollTop();
    const header = $('header');
    const div1 = $('.div1');
    const blur = $('#blurBackground');

    if (scrollPosition > 1) {
      blur.css('height', '50px');
      header.css('opacity', '0.7');
      header.css('transition', '0.5s');
      header.css('position', 'fixed');header.css('transition', '0.5s');
      div1.css('margin-top', '50px');
    } else {
      blur.css('height', '0px');
      header.css('opacity', '1');
      header.css('transition', '0.2s');
      header.css('position', 'static');
      div1.css('margin-top', '0px');
    }
  });
});