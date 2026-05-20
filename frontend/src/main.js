import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

import { createPinia } from 'pinia'
import router from './router'
import { useSavedCasesStore } from './stores/savedCases'
import { useUiStore } from './stores/ui'
import { useAuthStore } from './stores/auth'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')

useUiStore().initTheme()

;(async () => {
  const auth = useAuthStore()
  const savedCases = useSavedCasesStore()

  // Immediately populate from localStorage for a fast first render
  savedCases.hydrate()

  // Re-validate the stored token and fetch a fresh user profile from the API;
  // this also clears any stale session if the token has expired
  await auth.hydrate()

  // If a valid session was restored, fetch fresh saved cases so the sidebar
  // badge is accurate without requiring the user to navigate to the page first
  if (auth.isAuthenticated) {
    savedCases.fetchSavedCases()
  }
})()
