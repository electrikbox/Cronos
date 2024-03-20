// Square background img scroll effect

$(document).ready(function() {
  $(window).scroll(function() {
      const scrollPosition = $(this).scrollTop();
      const newPosition = - scrollPosition / 10;

      $('.main-landing').css('background-position', '0px ' + newPosition + 'px');
  });
});
