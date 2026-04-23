<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import { Sparkles, ArrowRight } from 'lucide-vue-next'

const phrases = [
  'Ankara Üniversitesi Bilgisayar Mühendisliği',
  'Hukuki Asistan Projesi',
  'ITTA 2026 Konferansı Makalesi', ,
  'TBB Proje Sunumu',
  'Encoder Mimarisi ile NLP Tabanlı Emsal Arama',
]

const typedText = ref('')
const isDeleting = ref(false)
const phraseIndex = ref(0)
const typingSpeed = ref(80)
let typingTimer

function tickTyping() {
  const current = phrases[phraseIndex.value] ?? ''
  if (!isDeleting.value) {
    typedText.value = current.slice(0, typedText.value.length + 1)
    if (typedText.value === current) {
      isDeleting.value = true
      typingSpeed.value = 1000
    } else {
      typingSpeed.value = 80
    }
  } else {
    typedText.value = current.slice(0, Math.max(0, typedText.value.length - 1))
    if (typedText.value.length === 0) {
      isDeleting.value = false
      phraseIndex.value = (phraseIndex.value + 1) % phrases.length
      typingSpeed.value = 200
    } else {
      typingSpeed.value = 40
    }
  }
  typingTimer = window.setTimeout(tickTyping, typingSpeed.value)
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

    <section class="mx-auto max-w-[980px] py-12 text-center">
      <div class="hero-reveal-1 flex items-center justify-center gap-2 text-[13px] font-semibold app-text-primary">
        <Sparkles class="size-4 app-text-muted" />
        Hukuki Asistan
      </div>

      <h1 class="hero-reveal-2 mt-4 text-[32px] font-semibold leading-tight tracking-[0.02em] app-text-primary md:text-[44px]">
        Legal AI Tech ile hukuk araştırması artık saniyeler içinde.
      </h1>

      <div class="hero-reveal-3 mt-4 text-[12px] uppercase tracking-[0.32em] app-text-muted">
        Legal AI Tech
      </div>

      <div class="hero-reveal-4 mt-6 text-[16px] font-semibold md:text-[20px]">
        <span class="typing-gradient">{{ typedText }}</span>
        <span class="typing-caret">|</span>
      </div>

      <p class="hero-reveal-5 mt-6 text-[15px] leading-7 app-text-secondary md:text-[18px]">
        Emsal kararlar, mahkeme içtihatları ve dava stratejileri için semantik arama altyapısı.
      </p>

      <div class="hero-reveal-6 mt-8 flex justify-center">
        <RouterLink
          to="/search"
          class="inline-flex items-center gap-2 rounded-2xl app-accent-strong px-6 py-3 text-sm font-semibold shadow-sm transition hover:opacity-90"
        >
          Aramayı Başlat
          <ArrowRight class="size-4" />
        </RouterLink>
      </div>
    </section>
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

.typing-gradient {
  background: linear-gradient(120deg, #60a5fa, #22d3ee, #a78bfa);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.typing-caret {
  margin-left: 6px;
  color: var(--app-text-muted);
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

.mesh-blob {
  position: absolute;
  width: 420px;
  height: 420px;
  filter: blur(80px);
  opacity: 0.25;
  animation: floatBlob 18s ease-in-out infinite;
}

.mesh-blob-1 {
  top: -160px;
  left: -120px;
  background: rgba(30, 64, 175, 0.35);
}

.mesh-blob-2 {
  bottom: -200px;
  right: -140px;
  background: rgba(15, 23, 42, 0.35);
  animation-delay: -6s;
}

.mesh-blob-3 {
  top: 30%;
  right: 10%;
  background: rgba(51, 65, 85, 0.3);
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
