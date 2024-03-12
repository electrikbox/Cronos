$(document).ready(function () {
  const navbarItems = document.querySelectorAll('.navbar-item');

  navbarItems.forEach(item => {
    item.addEventListener('click', function() {
      const itemId = item.getAttribute('id');
      window.location.href = 'http://localhost:8000/' + itemId;
    });
  });
});
