(() => {
  'use strict'

  const themeSwitch = document.querySelector('#theme-switch')

  const getStoredTheme = () => {
    const match = document.cookie.match(new RegExp('(^| )theme=([^;]+)'));
    if (match) return match[2];
    return null;
  }

  const setStoredTheme = (theme) => {
    document.cookie = "theme=" + theme + "; path=/";
  }

  const getPreferredTheme = () => {
    const storedTheme = getStoredTheme()
    if (storedTheme) {
      return storedTheme
    }
    return 'light' // Tema padrão é 'light'
  }

  const setTheme = theme => {
    document.documentElement.setAttribute('data-bs-theme', theme)
  }

  const updateIcon = () => {
    const currentTheme = document.documentElement.getAttribute('data-bs-theme')
    if (currentTheme === 'dark') {
      themeSwitch.querySelector('.sun-icon').style.display = 'block'
      themeSwitch.querySelector('.moon-icon').style.display = 'none'
    } else {
      themeSwitch.querySelector('.sun-icon').style.display = 'none'
      themeSwitch.querySelector('.moon-icon').style.display = 'block'
    }
  }

  // Inicializa o tema e os ícones
  const preferredTheme = getPreferredTheme();
  setTheme(preferredTheme)
  updateIcon()

  // Evento de clique para alternar o tema
  themeSwitch.addEventListener("click", () => {
    const currentTheme = document.documentElement.getAttribute('data-bs-theme')
    const theme = currentTheme === 'light' ? 'dark' : 'light'
    setStoredTheme(theme)
    setTheme(theme)
    updateIcon()
    console.log('Tema alterado para:', theme)

    // Ocultar o conteúdo principal e exibir o carregador
    document.getElementById('main-content').style.display = 'none';
    document.getElementById('loading-spinner').style.display = 'flex';

    // Recarregar a página para atualizar os gráficos
    window.location.reload();
  })
})()
