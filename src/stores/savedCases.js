import { defineStore } from 'pinia'

const STORAGE_KEY = 'hukuki_asistan_saved_cases_v1'

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
  }),
  getters: {
    savedList: (s) =>
      Object.values(s.byId).sort((a, b) => (b?.match_score ?? 0) - (a?.match_score ?? 0)),
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
    saveCase(caseObj) {
      if (!caseObj?.id) return
      this.byId[caseObj.id] = caseObj
      this.persist()
    },
    removeCase(id) {
      if (!id) return
      delete this.byId[id]
      this.persist()
    },
    toggleCase(caseObj) {
      const id = caseObj?.id
      if (!id) return
      if (this.byId[id]) this.removeCase(id)
      else this.saveCase(caseObj)
    },
  },
})

