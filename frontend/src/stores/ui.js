import { defineStore } from 'pinia'

const THEME_KEY = 'hukuki_asistan_theme_v1'

function resolveInitialTheme() {
  const saved = localStorage.getItem(THEME_KEY)
  if (saved === 'dark' || saved === 'light') return saved
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

export const useUiStore = defineStore('ui', {
  state: () => ({
    sidebarCollapsed: false,
    mobileSidebarOpen: false,
    theme: 'light',
  }),
  actions: {
    applyTheme(mode) {
      // Hem data-theme hem de Tailwind'in resmi 'dark' class'ını ekliyoruz. Çakışma bitiyor.
      document.documentElement.setAttribute('data-theme', mode)
      if (mode === 'dark') {
        document.documentElement.classList.add('dark')
      } else {
        document.documentElement.classList.remove('dark')
      }
      this.theme = mode
    },
    initTheme() {
      const mode = resolveInitialTheme()
      this.applyTheme(mode)
    },
    toggleTheme() {
      const mode = this.theme === 'dark' ? 'light' : 'dark'
      this.applyTheme(mode)
      localStorage.setItem(THEME_KEY, mode)
    },
    toggleSidebar() {
      this.sidebarCollapsed = !this.sidebarCollapsed
    },
    openMobileSidebar() {
      this.mobileSidebarOpen = true
    },
    closeMobileSidebar() {
      this.mobileSidebarOpen = false
    },
  },
})