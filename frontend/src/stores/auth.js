import { defineStore } from 'pinia'

const USERS_KEY = 'hukuki_asistan_users_v1'
const CURRENT_KEY = 'hukuki_asistan_current_user_v1'

function safeParse(json, fallback) {
  try {
    return JSON.parse(json) ?? fallback
  } catch {
    return fallback
  }
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    /** @type {{ name: string, email: string } | null} */
    currentUser: null,
    /** @type {Array<{ name: string, email: string, password: string }>} */
    users: [],
  }),
  getters: {
    isAuthenticated: (s) => Boolean(s.currentUser),
    displayName: (s) => s.currentUser?.name ?? 'Misafir',
    displaySubline: () => 'Profil ve ayarlar',
  },
  actions: {
    hydrate() {
      const usersRaw = localStorage.getItem(USERS_KEY)
      const currentRaw = localStorage.getItem(CURRENT_KEY)
      this.users = safeParse(usersRaw, [])
      this.currentUser = safeParse(currentRaw, null)
    },
    persistUsers() {
      localStorage.setItem(USERS_KEY, JSON.stringify(this.users))
    },
    persistCurrent() {
      localStorage.setItem(CURRENT_KEY, JSON.stringify(this.currentUser))
    },
    register({ name, email, password }) {
      if (!name || !email || !password) {
        return { ok: false, message: 'Lutfen tum alanlari doldurun.' }
      }
      const exists = this.users.find((u) => u.email.toLowerCase() === email.toLowerCase())
      if (exists) {
        return { ok: false, message: 'Bu e-posta zaten kayitli.' }
      }
      const user = { name, email, password }
      this.users.push(user)
      this.persistUsers()
      this.currentUser = { name, email }
      this.persistCurrent()
      return { ok: true }
    },
    login(email, password) {
      const user = this.users.find((u) => u.email.toLowerCase() === email.toLowerCase())
      if (!user) {
        return { ok: false, message: 'Boyle bir kullanici bulunamadi.' }
      }
      if (user.password !== password) {
        return { ok: false, message: 'Sifre hatali.' }
      }
      this.currentUser = { name: user.name, email: user.email }
      this.persistCurrent()
      return { ok: true }
    },
    logout() {
      this.currentUser = null
      this.persistCurrent()
    },
  },
})
