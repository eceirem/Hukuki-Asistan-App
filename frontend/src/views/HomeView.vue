<script setup>
// Script kısmın aynı, dokunmana gerek yok.
import { onMounted, onUnmounted, ref } from 'vue'
import { Sparkles, ArrowRight } from 'lucide-vue-next'

const phrases = [
  'Ankara Üniversitesi Bilgisayar Mühendisliği',
  'Hukuki Asistan Projesi',
  'ITTA 2026 Konferansı Makalesi',
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
  <div class="hero-wrap relative overflow-hidden rounded-[2rem] border transition-all duration-500 md:h-[calc(100dvh-164px)]">
    <!-- ARKA PLAN EFEKTLERİ -->
    <div class="pointer-events-none absolute inset-0">
      <div class="hero-orb hero-orb-1" />
      <div class="hero-orb hero-orb-2" />
      <div class="hero-orb hero-orb-3" />
      <div class="hero-grid" />
      <div class="hero-noise" />
    </div>

    <section class="relative mx-auto flex h-full max-w-[980px] flex-col justify-center px-6 py-7 text-center md:px-10 md:py-8">
      <div class="hero-reveal-1 hero-badge mx-auto inline-flex items-center gap-2 rounded-full border px-4 py-2 text-[12px] font-semibold transition-colors">
        <Sparkles class="size-4 text-violet-500 dark:text-cyan-400" />
        Legal AI Tech Platformu
      </div>

      <h1 class="hero-reveal-2 hero-title mt-5 text-[34px] font-extrabold leading-[1.04] tracking-[-0.03em] md:text-[56px]">
        Hukuk araştırması için <span class="headline-gradient">yeni jenerasyon</span> bir yapay zekâ deneyimi.
      </h1>

      <div class="hero-reveal-3 hero-subtitle mt-4 text-[10px] uppercase tracking-[0.35em]">
        Hukuki Asistan ile tanışın
      </div>

      <div class="hero-reveal-4 hero-typing mt-5 text-[17px] font-semibold md:text-[22px]">
        <span class="typing-gradient">{{ typedText || 'Semantik Emsal Arama' }}</span>
        <span class="typing-caret">|</span>
      </div>

      <p class="hero-reveal-5 hero-desc mx-auto mt-5 max-w-[700px] text-[14px] leading-6 md:text-[17px]">
        Emsal kararları, mahkeme içtihatlarını ve dava argümanlarını tek katmanda okuyarak en güçlü stratejiyi daha kısa sürede inşa edin.
      </p>

      <div class="hero-reveal-6 mt-7 flex flex-wrap items-center justify-center gap-3">
        <RouterLink to="/search" class="hero-cta-primary inline-flex items-center gap-2 rounded-2xl px-7 py-3.5 text-sm font-semibold transition">
          Aramayı Başlat <ArrowRight class="size-4" />
        </RouterLink>
        <RouterLink to="/saved" class="hero-cta-secondary inline-flex items-center gap-2 rounded-2xl border px-7 py-3.5 text-sm font-semibold transition">
          Kaydedilenleri Gör
        </RouterLink>
      </div>
    </section>
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

/* 2. ANA KAPSAYICI (HERO WRAP) - BURASI KRİTİK */
.hero-wrap {
  min-height: 500px;
  transition: all 0.5s ease-in-out;
}

/* LIGHT MODE */
:root:not(.dark) .hero-wrap,
html:not(.dark) .hero-wrap {
  background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%) !important;
  border-color: #e2e8f0 !important;
}

/* DARK MODE - LACİVERT/MOR (ZORLANMIŞ) */
/* Seçicileri artırdık ki hiçbir şey bunu ezemesin */
:global(html.dark) .hero-wrap,
:global(html[data-theme='dark']) .hero-wrap {
  background: linear-gradient(180deg, #020617 0%, #0f172a 100%) !important;
  background-color: #020617 !important; /* Düz renk garantisi */
  border-color: rgba(255, 255, 255, 0.1) !important;
}

/* 3. METİN RENKLERİ - DARK MODE */
:global(html.dark) .hero-title, :global(html.dark) .hero-desc { color: #ffffff !important; }
:global(html.dark) .hero-subtitle { color: #94a3b8 !important; }
:global(html.dark) .hero-badge { background: rgba(255, 255, 255, 0.05) !important; color: #ffffff !important; }

/* 4. ORBS (RENKLİ KÜRELER) */
.hero-orb { position: absolute; border-radius: 999px; filter: blur(80px); animation: floatBlob 16s ease-in-out infinite; }
.hero-orb-1 { width: 340px; height: 340px; top: -120px; left: -80px; background: rgba(56, 189, 248, 0.4); }
.hero-orb-2 { width: 440px; height: 440px; top: -90px; right: -180px; background: rgba(139, 92, 246, 0.3); animation-delay: -6s; }
.hero-orb-3 { width: 300px; height: 300px; bottom: -120px; left: 50%; background: rgba(236, 72, 153, 0.2); animation-delay: -12s; }

/* 5. DİĞER EFEKTLER */
.hero-grid {
  position: absolute; inset: 0;
  background-image: linear-gradient(to right, rgba(255,255,255,0.05) 1px, transparent 1px), 
                    linear-gradient(to bottom, rgba(255,255,255,0.05) 1px, transparent 1px);
  background-size: 40px 40px;
  mask-image: radial-gradient(circle at center, black 30%, transparent 95%);
}

.headline-gradient { background: linear-gradient(120deg, #0ea5e9, #22d3ee 45%, #f43f5e 78%); -webkit-background-clip: text; background-clip: text; color: transparent; }
.typing-gradient { background: linear-gradient(120deg, #38bdf8, #818cf8, #fb7185); -webkit-background-clip: text; background-clip: text; color: transparent; }
.hero-cta-primary { background: linear-gradient(130deg, #0ea5e9, #6366f1 50%, #d946ef); color: white !important; }

@keyframes floatBlob { 0%, 100% { transform: translate(0, 0); } 50% { transform: translate(20px, -20px); } }
</style>