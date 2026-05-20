import { defineStore } from 'pinia'
import axios from 'axios'
import { useSavedCasesStore } from './savedCases'

const CURRENT_KEY = 'hukuki_asistan_current_user_v1'
const TOKEN_KEY = 'hukuki_asistan_access_token_v1'

function safeParse(json, fallback) {
  try {
    if (typeof json !== 'string' || !json) return fallback
    return JSON.parse(json)
  } catch {
    return fallback
  }
}

const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    /** @type {{ name: string, email: string } | null} */
    currentUser: null,
    /** maintains API compat, not used in backend mode */
    users: [],
    /** @type {string|null} */
    accessToken: null,
  }),
  getters: {
    isAuthenticated: (s) => Boolean(s.currentUser && s.accessToken),
    displayName: (s) => {
      if (!s.currentUser) return 'Misafir'
      const parts = [s.currentUser.name, s.currentUser.surname].filter(Boolean)
      return parts.length > 0 ? parts.join(' ') : 'Misafir'
    },
    displaySubline: () => 'Profil ve ayarlar',
  },
  actions: {
    async hydrate() {
      const currentRaw = localStorage.getItem(CURRENT_KEY)
      const tokenRaw = localStorage.getItem(TOKEN_KEY)
      this.currentUser = safeParse(currentRaw, null)
      this.accessToken = typeof tokenRaw === 'string' ? tokenRaw : null

      if (this.accessToken) {
        try {
          const userRes = await axios.get(`${API_BASE}/users/me`, {
            headers: { Authorization: `Bearer ${this.accessToken}` },
          })
          this.currentUser = userRes.data
          this.persistAuth()
        } catch {
          // Token expired or invalid — clear stale session
          this.currentUser = null
          this.accessToken = null
          this.persistAuth()
        }
      }
    },
    persistAuth() {
      localStorage.setItem(CURRENT_KEY, JSON.stringify(this.currentUser))
      if (this.accessToken) {
        localStorage.setItem(TOKEN_KEY, this.accessToken)
      } else {
        localStorage.removeItem(TOKEN_KEY)
      }
    },
    async register({ name, email, password }) {
      if (!name || !email || !password) {
        return { ok: false, message: 'Lutfen tum alanlari doldurun.' }
      }
      // Split name into first and surname
      const parts = name.trim().split(/\s+/)
      const firstName = parts.length > 0 ? parts[0] : ''
      const surname = parts.length > 1 ? parts.slice(1).join(' ') : ''
      try {
        const res = await axios.post(`${API_BASE}/auth/register`, {
          name: firstName,
          surname: surname,
          email,
          password,
        })
        // Optional: auto-login
        return { ok: true }
      } catch (err) {
        let msg = 'Beklenmeyen bir hata olustu.'
        if (err.response?.data?.detail) {
          msg = err.response.data.detail
        }
        return { ok: false, message: msg }
      }
    },
    async login(email, password) {
      if (!email || !password) {
        return { ok: false, message: 'Lutfen e-posta ve sifrenizi girin.' }
      }
      try {
        const formData = new FormData()
        formData.append('username', email)
        formData.append('password', password)
        const tokenRes = await axios.post(`${API_BASE}/auth/login`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        })
        const { access_token } = tokenRes.data
        if (!access_token) {
          return { ok: false, message: 'Giris basarisiz.' }
        }
        this.accessToken = access_token
        // Get user profile
        const userRes = await axios.get(`${API_BASE}/users/me`, {
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        })
        this.currentUser = userRes.data
        this.persistAuth()
        useSavedCasesStore().fetchSavedCases()
        return { ok: true }
      } catch (err) {
        let msg = 'Beklenmeyen bir hata olustu.'
        // Try to extract backend error, including OAuth2/validation errors
        if (err.response?.data?.detail) {
          msg = err.response.data.detail
        } else if (err.response?.data?.error) {
          msg = err.response.data.error
        }
        return { ok: false, message: msg }
      }
    },
    logout() {
      useSavedCasesStore().clearState()
      this.currentUser = null
      this.accessToken = null
      this.persistAuth()
    },
  },
})
