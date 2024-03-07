$(document).ready(function() {
  // Fonction pour la navigation avec un décalage
  $('a[href^="#"]').on('click', function(event) {
    var target = $(this.getAttribute('href'));
    if (target.length) {
      event.preventDefault();
      $('html, body').animate({
        scrollTop: target.offset().top - 50
      }, 0);
    }
  });
});