// Toggle visibility of password fields
document.addEventListener('DOMContentLoaded', function () {
  const passwordInputs = document.querySelectorAll('input[type="password"]');

  passwordInputs.forEach(function (passwordInput) {
    const showPwd = document.createElement('span');
    showPwd.textContent = '▲ SHOW';
    showPwd.classList.add('showPwd');

    passwordInput.insertAdjacentElement('afterend', showPwd);

    showPwd.addEventListener('click', function () {
      if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        showPwd.textContent = '▽ HIDE';
      } else {
        passwordInput.type = 'password';
        showPwd.textContent = '▲ SHOW';
      }
    });
  });
});
