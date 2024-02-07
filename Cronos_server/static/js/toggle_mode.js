document.addEventListener('DOMContentLoaded', function () {
  const modeToggle = document.querySelector('#toggle_mode input[type="checkbox"]');
  const body = document.body;

  // Fonction pour définir le mode dans la session Storage
  function setMode(mode) {
    body.classList.remove('light-mode', 'dark-mode');
    body.classList.add(mode);
    sessionStorage.setItem('mode', mode);
    modeToggle.checked = mode === 'dark-mode';
  }

  // Fonction pour récupérer le mode depuis la session Storage
  function getMode() {
    const mode = sessionStorage.getItem('mode') || "light-mode";
    return mode;
  }

  // Appliquer le mode lors du chargement de la page
  const currentMode = getMode();
  setMode(currentMode);

  // Gérer le changement de mode
  modeToggle.addEventListener('change', function () {
    if (modeToggle.checked) {
      setMode('dark-mode');
    } else {
      setMode('light-mode');
    }
  });
});
