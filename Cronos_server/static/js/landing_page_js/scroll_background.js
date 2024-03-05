$(document).ready(function() {
  $(window).scroll(function() {
      var scrollPosition = $(this).scrollTop();

      // Calculez la nouvelle position verticale de l'image de fond en fonction du défilement
      var newPosition = - scrollPosition / 5; // Utilisez un signe négatif pour inverser la direction du déplacement

      // Appliquez la nouvelle position à l'arrière-plan de .main-landing
      $('.main-landing').css('background-position', '0px ' + newPosition + 'px');
  });
});