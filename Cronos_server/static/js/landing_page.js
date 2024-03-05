$(document).ready(function () {
  $('#log-login').click(function () {
    window.location.href = 'http://localhost:8000/accounts/login'
  });

  $('#log-register').click(function () {
    window.location.href = 'http://localhost:8000/accounts/signup'
  });
});
