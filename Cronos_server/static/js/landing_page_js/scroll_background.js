$(document).ready(function() {
  $(window).scroll(function() {
      var scrollPosition = $(this).scrollTop();
      var newPosition = - scrollPosition / 10;

      $('.main-landing').css('background-position', '0px ' + newPosition + 'px');
  });
});
