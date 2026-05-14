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
useAuthStore().hydrate()

// hydrate after pinia is available
useSavedCasesStore().hydrate()
