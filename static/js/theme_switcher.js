(() => {
  'use strict'

  const themeSwitch = document.querySelector('#theme-switch')
  const getStoredTheme = () => localStorage.getItem('theme')
  const setStoredTheme = theme => localStorage.setItem('theme', theme)

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
  setTheme(getPreferredTheme())
  updateIcon()

  // Evento de clique para alternar o tema
  themeSwitch.addEventListener("click", () => {
    const currentTheme = document.documentElement.getAttribute('data-bs-theme')
    const theme = currentTheme === 'light' ? 'dark' : 'light'
    setStoredTheme(theme)
    setTheme(theme)
    updateIcon()

    // Adicionar classe .clicked para ativar a transição
    themeSwitch.classList.add('clicked')

    // Remover a classe .clicked após a transição
    setTimeout(() => {
      themeSwitch.classList.remove('clicked')
    }, 200) // O tempo aqui deve corresponder à duração da transição no CSS (0.2s)
  })
})()
