<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { Search, Sparkles } from 'lucide-vue-next'
import axios from 'axios'
import CaseResultCard from '../components/CaseResultCard.vue'
import CaseDetailModal from '../components/CaseDetailModal.vue'
import { useAuthStore } from '../stores/auth' // Adjust the import path if your actual store file is different

const authStore = useAuthStore()

const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000'

const query = ref('')
// Default result-set size aligns with the backend CaseSearchQuery default
// (app/schemas/case.py — `limit: int = Field(default=10, ge=1, le=100)`).
const k = ref(10)
// "Tümü" maps to the backend's maximum allowed limit (le=100). The pgvector
// HNSW scan is happy at this size and the BM25 candidate pool is 100 anyway,
// so this is effectively "everything we ranked".
const ALL_LIMIT = 100
const kOptions = [
  { label: 'İlk 5', value: 5 },
  { label: 'İlk 7', value: 7 },
  { label: 'İlk 10', value: 10 },
  { label: 'Tümü', value: ALL_LIMIT },
]

const quickTags = [
  'Telif Hakkı İhlali',
  'Marka Taklidi',
  'Haksız Rekabet',
  'Hakaret ve İftira',
  'Kişilik Haklarına Saldırı',
  'Erişimin Engellenmesi',
  'Sahte Hesap',
]

const loading = ref(false)
// `slowLoading` flips to true once a /search call has been pending longer
// than SLOW_LOADING_THRESHOLD_MS. We use it to progressively reveal the LLM
// warmup banner: short responses never show it (would be a lie), but the
// multi-second first-call cold-start of the local Turkish-Gemma model
// always trips it and the user gets a clear explanation of the wait.
const slowLoading = ref(false)
const SLOW_LOADING_THRESHOLD_MS = 1200
let slowLoadingTimer = null
const hasSearched = ref(false)
const results = ref([])
const visibleCount = ref(8)
const selected = ref(null)
const modalOpen = ref(false)
const PAGE_SIZE = 8

const activeQuickTag = computed(() => {
  const normalized = query.value.trim().toLowerCase()
  return quickTags.find((tag) => tag.toLowerCase() === normalized) ?? null
})

const visibleResults = computed(() => results.value.slice(0, visibleCount.value))

const resultCountText = computed(() => {
  if (!hasSearched.value) return ''
  if (loading.value) return 'Aranıyor...'
  return `${results.value.length} sonuç`
})

const typingPhrases = [
  'Telif Hakkı İhlali',
  'Marka Koruması',
  'İftira Davaları',
]

const typedText = ref('')
const isDeleting = ref(false)
const phraseIndex = ref(0)
const typingSpeed = ref(70)
let typingTimer

const heroPlaceholder = computed(() => `Legal AI Tech · ${typedText.value}`)

function tickTyping() {
  const current = typingPhrases[phraseIndex.value] ?? ''
  if (!isDeleting.value) {
    typedText.value = current.slice(0, typedText.value.length + 1)
    if (typedText.value === current) {
      isDeleting.value = true
      typingSpeed.value = 900
    } else {
      typingSpeed.value = 70
    }
  } else {
    typedText.value = current.slice(0, Math.max(0, typedText.value.length - 1))
    if (typedText.value.length === 0) {
      isDeleting.value = false
      phraseIndex.value = (phraseIndex.value + 1) % typingPhrases.length
      typingSpeed.value = 220
    } else {
      typingSpeed.value = 40
    }
  }
  typingTimer = window.setTimeout(tickTyping, typingSpeed.value)
}

function clearSlowLoadingTimer() {
  if (slowLoadingTimer) {
    window.clearTimeout(slowLoadingTimer)
    slowLoadingTimer = null
  }
}

async function runSearch() {
  hasSearched.value = true
  loading.value = true
  slowLoading.value = false
  clearSlowLoadingTimer()
  slowLoadingTimer = window.setTimeout(() => {
    if (loading.value) slowLoading.value = true
  }, SLOW_LOADING_THRESHOLD_MS)
  visibleCount.value = PAGE_SIZE
  try {
    const accessToken = authStore.accessToken
    if (!accessToken) {
      results.value = []
      return
    }
    const body = {
      query: query.value,
      limit: k.value,
    }
    const response = await axios.post(
      `${API_BASE}/search/`,
      body,
      {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      }
    )
    results.value = Array.isArray(response.data) ? response.data : []
  } catch (e) {
    results.value = []
  } finally {
    loading.value = false
    slowLoading.value = false
    clearSlowLoadingTimer()
  }
}

function onQuickTag(tag) {
  query.value = tag
  runSearch()
}

function onSelectLimit(value) {
  k.value = value
  // If the user already has results on screen, re-run with the new limit so
  // the change is immediate; otherwise just update state and wait for "Ara".
  if (hasSearched.value && query.value.trim().length > 0) {
    runSearch()
  }
}

function openDetails(item) {
  selected.value = item
  modalOpen.value = true
}

function loadMoreResults() {
  if (loading.value) return
  if (visibleCount.value >= results.value.length) return
  visibleCount.value = Math.min(results.value.length, visibleCount.value + PAGE_SIZE)
}

const vIntersect = {
  mounted(el, binding) {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries.some((entry) => entry.isIntersecting)) {
          binding.value?.()
        }
      },
      { rootMargin: '120px 0px' },
    )
    observer.observe(el)
    el.__observer = observer
  },
  unmounted(el) {
    el.__observer?.disconnect()
    delete el.__observer
  },
}

onMounted(() => {
  typedText.value = ''
  isDeleting.value = false
  phraseIndex.value = 0
  typingSpeed.value = 120
  tickTyping()
})

onUnmounted(() => {
  if (typingTimer) window.clearTimeout(typingTimer)
  clearSlowLoadingTimer()
})
</script>

<template>
  <div class="relative w-full overflow-x-hidden">
    <div class="pointer-events-none absolute inset-0 overflow-hidden">
      <div class="mesh-blob mesh-blob-1" />
      <div class="mesh-blob mesh-blob-2" />
      <div class="mesh-blob mesh-blob-3" />
    </div>

    <div class="relative z-10 -mx-4 border-b app-border bg-transparent px-4 py-10 sm:-mx-6 sm:px-6 lg:-mx-10 lg:px-10">
      <div class="mx-auto w-full max-w-[980px] text-center">
        <div class="flex flex-col items-center gap-4">
          <div class="hero-reveal-1 flex items-center gap-2 text-[13px] font-semibold app-text-primary">
            <Sparkles class="size-4 app-text-muted" />
            Hukuki Asistan
          </div>
          <div class="hero-reveal-2 text-[28px] font-semibold leading-tight tracking-[0.02em] app-text-primary md:text-[36px]">
            Türkiye'nin Hukuki Zekâsı Altyapısı
          </div>
          <div class="hero-reveal-3 text-[12px] uppercase tracking-[0.32em] app-text-muted">
            Legal AI Tech
          </div>
          <div class="hero-reveal-4 text-[15px] leading-7 app-text-secondary md:text-[18px]">
            <span class="typing-text">{{ typedText }}</span>
            <span class="typing-caret">|</span>
          </div>
          <div v-if="hasSearched" class="text-xs app-text-muted">
            {{ resultCountText }}
          </div>
        </div>

        <form class="mt-8" @submit.prevent="runSearch">
          <!-- glass-shell BURADA -->
          <div class="glass-shell hero-reveal-5 rounded-3xl p-3 sm:p-4">
            <div class="search-shell flex flex-col gap-3 sm:flex-row sm:items-center">
              
              <!-- search-input-shell BURADA -->
              <div class="search-input-shell relative flex-1 rounded-2xl border app-border bg-transparent ring-0 transition-all">
                <div class="absolute left-4 top-1/2 -translate-y-1/2 app-text-muted">
                  <Search class="size-5" />
                </div>
                <input
                  v-model="query"
                  type="text"
                  class="h-14 w-full rounded-2xl bg-transparent pl-12 pr-4 text-[15px] app-text-primary placeholder:app-text-muted focus:outline-none"
                  :placeholder="heroPlaceholder"
                  autocomplete="off"
                />
              </div>

              <div class="flex flex-col items-start gap-2">
                <div class="text-xs font-medium tracking-[0.08em] app-text-muted">
                  Sonuç sayısı
                </div>
                <!-- k-shell BURADA -->
                <div class="k-shell inline-flex rounded-2xl border app-border p-1 shadow-sm transition-all">
                  <button
                    v-for="opt in kOptions"
                    :key="opt.label"
                    type="button"
                    class="rounded-xl px-3 py-2 text-xs font-semibold transition"
                    :class="
                      k === opt.value
                        ? 'app-accent-strong shadow-sm active-k'
                        : 'app-text-secondary hover:app-surface-soft'
                    "
                    @click="onSelectLimit(opt.value)"
                  >
                    {{ opt.label }}
                  </button>
                </div>
              </div>

              <button
                type="submit"
                class="search-submit h-14 rounded-2xl app-accent-strong px-5 text-xs font-semibold shadow-sm transition hover:opacity-90 disabled:opacity-60"
                :disabled="loading"
              >
                {{ loading ? 'Aranıyor…' : 'Ara' }}
              </button>
            </div>
          </div>

          <div class="hero-reveal-6 mt-4 flex flex-wrap justify-center gap-2">
            <button
              v-for="tag in quickTags"
              :key="tag"
              type="button"
              class="rounded-full border px-3 py-1.5 text-xs font-medium shadow-sm transition"
              :class="
                activeQuickTag === tag
                  ? 'app-accent-strong border-transparent'
                  : 'app-border app-surface app-text-secondary hover:app-surface-soft'
              "
              @click="onQuickTag(tag)"
            >
              {{ tag }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="hasSearched" class="mt-8">
      <div v-if="loading" class="grid gap-3">
        <Transition name="warmup-fade">
          <div
            v-if="slowLoading"
            class="warmup-banner flex items-center gap-3 rounded-2xl border app-border px-4 py-3 text-[13px] app-text-secondary"
            role="status"
            aria-live="polite"
          >
            <span class="warmup-spinner" aria-hidden="true" />
            <Sparkles class="size-4 app-text-muted" aria-hidden="true" />
            <span class="leading-relaxed">
              Hukuki Yapay Zeka modeli belleğe yükleniyor
              <span class="app-text-muted">(İlk arama biraz sürebilir)…</span>
            </span>
          </div>
        </Transition>
        <div v-for="i in 3" :key="i" class="h-[150px] animate-pulse rounded-2xl border app-border app-surface" />
      </div>
      <div v-else class="grid gap-4">
        <CaseResultCard v-for="item in visibleResults" :key="item.id" :item="item" @readMore="openDetails" />
        <div v-if="visibleCount < results.length" v-intersect="loadMoreResults" class="h-3 w-full" aria-hidden="true" />
      </div>
    </div>
    <CaseDetailModal :open="modalOpen" :case-item="selected" @close="modalOpen = false" />
  </div>
</template>

<style scoped>
/* 1. ANİMASYONLAR */
.hero-reveal-1, .hero-reveal-2, .hero-reveal-3, .hero-reveal-4, .hero-reveal-5, .hero-reveal-6 {
  animation: heroReveal 700ms ease both;
}
.hero-reveal-2 { animation-delay: 120ms; }
.hero-reveal-3 { animation-delay: 220ms; }
.hero-reveal-4 { animation-delay: 320ms; }
.hero-reveal-5 { animation-delay: 420ms; }
.hero-reveal-6 { animation-delay: 520ms; }
@keyframes heroReveal { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: translateY(0); } }

/* 2. ANA ARAMA KABUĞU (O GRİ PERDEYİ YOK EDEN KISIM) */
.glass-shell {
  transition: all 0.4s ease-in-out;
}

/* DARK MODE ZORLAMASI */
/* :deep() kullanarak Vue'nun data-v attribute'larını baypas ediyoruz */
:global(.dark) :deep(.glass-shell),
:global(html[data-theme='dark']) :deep(.glass-shell),
:global(.dark) .glass-shell {
  background: #0f172a !important; /* TAM NAVY BLUE */
  background-color: #0f172a !important;
  border: 1px solid rgba(56, 189, 248, 0.2) !important;
  backdrop-filter: none !important; /* Gri pusun sebebi bu, sildik! */
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7) !important;
}

/* 3. INPUT ALANI (İÇ KUTU) */
:global(.dark) :deep(.search-input-shell) {
  background: #020617 !important;
  border-color: rgba(255, 255, 255, 0.1) !important;
}

/* 4. SONUÇ SAYISI (K-SHELL) */
:global(.dark) :deep(.k-shell) {
  background: #1e293b !important;
  border-color: rgba(255, 255, 255, 0.1) !important;
}

/* 5. TYPING VE METİNLER */
.typing-text { font-weight: 600; color: #38bdf8; }
.typing-caret { margin-left: 4px; animation: blink 900ms steps(2, start) infinite; color: #38bdf8; }
@keyframes blink { 0%, 100% { opacity: 0.2; } 50% { opacity: 1; } }

:global(.dark) .app-text-primary { color: #ffffff !important; }
:global(.dark) .app-text-secondary { color: #e2e8f0 !important; }

/* 6. ARA BUTONU */
.search-submit {
  background: linear-gradient(135deg, #0ea5e9, #6366f1) !important;
  color: white !important;
  border: none !important;
}

/* ARKA PLAN BLOBLARI */
.mesh-blob { position: absolute; width: 420px; height: 420px; filter: blur(80px); opacity: 0.2; }
:global(.dark) .mesh-blob-1 { background: rgba(30, 58, 138, 0.4); }

/* LLM WARMUP BANNER — appears only when /search takes longer than the
 * SLOW_LOADING_THRESHOLD_MS (~1.2 s). Soft gradient backdrop so it reads as
 * a status hint, not an error. */
.warmup-banner {
  background:
    linear-gradient(135deg, rgba(14, 165, 233, 0.08), rgba(99, 102, 241, 0.08));
  border-color: rgba(14, 165, 233, 0.25);
}
:global(.dark) .warmup-banner {
  background:
    linear-gradient(135deg, rgba(14, 165, 233, 0.18), rgba(99, 102, 241, 0.18));
  border-color: rgba(56, 189, 248, 0.35);
}

.warmup-spinner {
  display: inline-block;
  width: 14px;
  height: 14px;
  border-radius: 9999px;
  border: 2px solid rgba(14, 165, 233, 0.25);
  border-top-color: #0ea5e9;
  animation: warmup-spin 0.9s linear infinite;
}
@keyframes warmup-spin { to { transform: rotate(360deg); } }

.warmup-fade-enter-active,
.warmup-fade-leave-active {
  transition: opacity 280ms ease, transform 280ms ease;
}
.warmup-fade-enter-from,
.warmup-fade-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>