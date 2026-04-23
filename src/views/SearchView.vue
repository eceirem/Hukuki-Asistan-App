<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { Search, Sparkles } from 'lucide-vue-next'
import { mockSearchCases } from '../services/mockSearch'
import CaseResultCard from '../components/CaseResultCard.vue'
import CaseDetailModal from '../components/CaseDetailModal.vue'

const query = ref('')
const k = ref(7)
const kOptions = [
  { label: 'İlk 5', value: 5 },
  { label: 'İlk 7', value: 7 },
  { label: 'İlk 10', value: 10 },
  { label: 'Tümü', value: 'all' },
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

async function runSearch() {
  hasSearched.value = true
  loading.value = true
  visibleCount.value = PAGE_SIZE
  try {
    results.value = await mockSearchCases({ query: query.value, k: k.value })
  } finally {
    loading.value = false
  }
}

function onQuickTag(tag) {
  query.value = tag
  runSearch()
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
})
</script>

<template>
  <div class="relative">
    <div class="pointer-events-none absolute inset-0 overflow-hidden">
      <div class="mesh-blob mesh-blob-1" />
      <div class="mesh-blob mesh-blob-2" />
      <div class="mesh-blob mesh-blob-3" />
    </div>

    <div
      class="sticky top-0 z-40 -mx-4 border-b app-border bg-transparent px-4 py-10 backdrop-blur-sm sm:-mx-6 sm:px-6 lg:-mx-10 lg:px-10"
    >
      <div
        class="mx-auto w-full max-w-[980px] text-center"
      >
        <div class="flex flex-col items-center gap-4">
          <div class="hero-reveal-1 flex items-center gap-2 text-[13px] font-semibold app-text-primary">
            <Sparkles class="size-4 app-text-muted" />
            Hukuki Asistan
          </div>
          <div class="hero-reveal-2 text-[28px] font-semibold leading-tight tracking-[0.02em] app-text-primary md:text-[36px]">
            Türkiye'nin hukuk zekâsı altyapısı
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
          <div class="glass-shell hero-reveal-5 rounded-3xl p-3 sm:p-4">
            <div class="search-shell flex flex-col gap-3 sm:flex-row sm:items-center">
              <div
                class="relative flex-1 rounded-2xl border app-border bg-transparent ring-0 focus-within:border-slate-300"
              >
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
                <div class="inline-flex rounded-2xl border app-border app-surface-soft p-1 shadow-sm backdrop-blur">
                  <button
                    v-for="opt in kOptions"
                    :key="opt.label"
                    type="button"
                    class="rounded-xl px-3 py-2 text-xs font-semibold transition"
                    :class="
                      k === opt.value
                        ? 'app-accent-strong shadow-sm'
                        : 'app-text-secondary hover:app-surface-soft'
                    "
                    @click="k = opt.value"
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
        <div
          v-for="i in 3"
          :key="i"
          class="h-[150px] animate-pulse rounded-2xl border app-border app-surface"
        />
      </div>

      <div v-else class="grid gap-4">
        <CaseResultCard v-for="item in visibleResults" :key="item.id" :item="item" @readMore="openDetails" />
        <div
          v-if="visibleCount < results.length"
          v-intersect="loadMoreResults"
          class="h-3 w-full"
          aria-hidden="true"
        />
      </div>

      <div v-if="!loading && results.length === 0" class="rounded-2xl border app-border app-surface p-6 text-sm app-text-muted">
        Sonuç bulunamadı. Daha genel bir ifade deneyin veya hızlı etiketlerden birini seçin.
      </div>
    </div>

    <CaseDetailModal :open="modalOpen" :case-item="selected" @close="modalOpen = false" />
  </div>
</template>

<style scoped>
.hero-reveal-1,
.hero-reveal-2,
.hero-reveal-3,
.hero-reveal-4,
.hero-reveal-5,
.hero-reveal-6 {
  animation: heroReveal 700ms ease both;
}

.hero-reveal-2 {
  animation-delay: 120ms;
}

.hero-reveal-3 {
  animation-delay: 220ms;
}

.hero-reveal-4 {
  animation-delay: 320ms;
}

.hero-reveal-5 {
  animation-delay: 420ms;
}

.hero-reveal-6 {
  animation-delay: 520ms;
}

@keyframes heroReveal {
  from {
    opacity: 0;
    transform: translateY(14px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.typing-text {
  font-weight: 600;
}

.typing-caret {
  margin-left: 4px;
  animation: blink 900ms steps(2, start) infinite;
}

@keyframes blink {
  0%,
  100% {
    opacity: 0.2;
  }
  50% {
    opacity: 1;
  }
}

.glass-shell {
  position: relative;
  background: rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.35);
  box-shadow: 0 24px 60px -28px rgba(15, 23, 42, 0.35);
  backdrop-filter: blur(18px);
}

:global(html[data-theme='dark']) .glass-shell {
  background: rgba(15, 23, 42, 0.35);
  border: 1px solid rgba(148, 163, 184, 0.25);
  box-shadow: 0 30px 80px -34px rgba(0, 0, 0, 0.7);
}

.glass-shell::before {
  content: '';
  position: absolute;
  inset: -1px;
  border-radius: 1.5rem;
  padding: 1px;
  background: linear-gradient(120deg, rgba(99, 102, 241, 0.4), rgba(14, 165, 233, 0.2), rgba(99, 102, 241, 0.1));
  mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
  -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}

.search-shell {
  transition: transform 240ms ease, box-shadow 240ms ease;
}

.search-shell:focus-within {
  transform: scale(1.015);
}

.search-shell:focus-within .search-submit {
  animation: pulseGlow 1.8s ease-in-out infinite;
}

@keyframes pulseGlow {
  0%,
  100% {
    box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.25);
  }
  50% {
    box-shadow: 0 0 0 8px rgba(59, 130, 246, 0);
  }
}

.mesh-blob {
  position: absolute;
  width: 420px;
  height: 420px;
  filter: blur(80px);
  opacity: 0.3;
  animation: floatBlob 18s ease-in-out infinite;
}

.mesh-blob-1 {
  top: -160px;
  left: -120px;
  background: rgba(30, 64, 175, 0.4);
}

.mesh-blob-2 {
  bottom: -200px;
  right: -140px;
  background: rgba(15, 23, 42, 0.4);
  animation-delay: -6s;
}

.mesh-blob-3 {
  top: 30%;
  right: 10%;
  background: rgba(51, 65, 85, 0.35);
  animation-delay: -12s;
}

:global(html[data-theme='dark']) .mesh-blob {
  opacity: 0.5;
}

@keyframes floatBlob {
  0%,
  100% {
    transform: translate3d(0, 0, 0) scale(1);
  }
  50% {
    transform: translate3d(30px, -20px, 0) scale(1.05);
  }
}
</style>

