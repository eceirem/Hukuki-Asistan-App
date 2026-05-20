import { defineStore } from 'pinia'
import axios from 'axios'
import { useAuthStore } from './auth'

const STORAGE_KEY = 'hukuki_asistan_saved_cases_v1'
const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000'

function safeParse(json, fallback) {
  try {
    return JSON.parse(json) ?? fallback
  } catch {
    return fallback
  }
}

export const useSavedCasesStore = defineStore('savedCases', {
  state: () => ({
    /** @type {Record<string, any>} */
    byId: {},
    loading: false,
    error: null,
  }),
  getters: {
    savedList: (s) =>
      Object.values(s.byId).sort((a, b) => (b?.id ?? 0) - (a?.id ?? 0)),
    savedCount: (s) => Object.keys(s.byId).length,
    isSaved: (s) => (id) => Boolean(s.byId[id]),
  },
  actions: {
    hydrate() {
      const raw = localStorage.getItem(STORAGE_KEY)
      const parsed = safeParse(raw, { byId: {} })
      if (parsed?.byId && typeof parsed.byId === 'object') this.byId = parsed.byId
    },
    persist() {
      localStorage.setItem(STORAGE_KEY, JSON.stringify({ byId: this.byId }))
    },
    clearState() {
      this.byId = {}
      this.loading = false
      this.error = null
      localStorage.removeItem(STORAGE_KEY)
    },

    async fetchSavedCases() {
      const auth = useAuthStore()
      if (!auth.accessToken) return
      this.loading = true
      this.error = null
      try {
        const res = await axios.get(`${API_BASE}/users/me/saved-cases`, {
          headers: { Authorization: `Bearer ${auth.accessToken}` },
        })
        const cases = Array.isArray(res.data) ? res.data : []
        const newById = {}
        for (const c of cases) {
          if (c?.id != null) newById[c.id] = c
        }
        this.byId = newById
        this.persist()
      } catch (err) {
        this.error = err?.response?.data?.detail ?? 'Kaydedilen kararlar yüklenemedi.'
      } finally {
        this.loading = false
      }
    },

    async saveCase(caseObj) {
      if (!caseObj?.id) return
      this.byId[caseObj.id] = caseObj
      this.persist()
      const auth = useAuthStore()
      if (!auth.accessToken) return
      try {
        await axios.post(
          `${API_BASE}/users/me/saved-cases/${caseObj.id}`,
          {},
          { headers: { Authorization: `Bearer ${auth.accessToken}` } },
        )
      } catch {
        // Saved locally; backend sync failed silently
      }
    },

    async removeCase(id) {
      if (id == null) return
      delete this.byId[id]
      this.persist()
      const auth = useAuthStore()
      if (!auth.accessToken) return
      try {
        await axios.delete(`${API_BASE}/users/me/saved-cases/${id}`, {
          headers: { Authorization: `Bearer ${auth.accessToken}` },
        })
      } catch {
        // Removed locally; backend sync failed silently
      }
    },

    async toggleCase(caseObj) {
      const id = caseObj?.id
      if (id == null) return
      if (this.byId[id]) await this.removeCase(id)
      else await this.saveCase(caseObj)
    },
  },
})
