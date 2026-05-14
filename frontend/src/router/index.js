import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SearchView from '../views/SearchView.vue'
import SavedCasesView from '../views/SavedCasesView.vue'
import AboutView from '../views/AboutView.vue'
import LoginView from '../views/LoginView.vue'
import { useAuthStore } from '../stores/auth'

export const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/search', name: 'search', component: SearchView, meta: { requiresAuth: true } },
  { path: '/saved', name: 'saved', component: SavedCasesView, meta: { requiresAuth: true } },
  { path: '/about', name: 'about', component: AboutView, meta: { requiresAuth: true } },
  { path: '/login', name: 'login', component: LoginView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

router.beforeEach((to) => {
  if (!to.meta?.requiresAuth) return true
  const auth = useAuthStore()
  if (auth.isAuthenticated) return true
  return { name: 'login' }
})

export default router