<template>
  <div class="space-y-16">
    <section class="rounded-[32px] border app-border app-surface p-4 md:p-6">
      <div class="relative overflow-hidden rounded-2xl border app-border app-surface-soft bg-white">
        
        <button
          type="button"
          class="absolute left-4 top-1/2 z-20 -translate-y-1/2 rounded-full border app-border bg-white/85 px-3 py-2 text-sm font-semibold text-slate-900 transition hover:bg-[#0f1d3a] hover:text-white"
          @click="prevSlide"
        >
          ‹
        </button>
        <button
          type="button"
          class="absolute right-4 top-1/2 z-20 -translate-y-1/2 rounded-full border app-border bg-white/85 px-3 py-2 text-sm font-semibold text-slate-900 transition hover:bg-[#0f1d3a] hover:text-white"
          @click="nextSlide"
        >
          ›
        </button>

        <div class="relative h-[72vh] w-full overflow-hidden rounded-xl border app-border app-surface sm:h-[78vh] lg:h-[84vh] bg-white flex items-center justify-center">
          
          <transition name="fade">
            <img 
              :key="currentSlide" 
              :src="`/slides/slide-${currentSlide}.jpg`" 
              alt="Sunum Slaytı"
              class="absolute inset-0 w-full h-full object-contain bg-white"
            />
          </transition>

        </div>
      </div>
    </section>

    <section class="rounded-3xl border app-border app-surface p-6 space-y-5">
      <div>
        <div class="text-xs uppercase tracking-[0.25em] app-text-muted">Roadmap</div>
        <h3 class="text-2xl font-semibold app-text-primary">Kilit Aşamalar</h3>
      </div>
      <ol class="space-y-4">
        <li v-for="step in milestones" :key="step.title" class="rounded-2xl border app-border app-surface-soft p-4">
          <div class="text-sm font-semibold app-text-primary">{{ step.title }}</div>
          <p class="mt-2 text-xs app-text-muted">{{ step.detail }}</p>
        </li>
      </ol>
    </section>

    <section class="space-y-6">
      <div class="flex items-end justify-between">
        <div>
          <div class="text-xs uppercase tracking-[0.25em] app-text-muted">Galeri</div>
          <h2 class="text-2xl font-semibold app-text-primary">Sunum ve Atölye Fotoğrafları</h2>
        </div>
        <div class="text-xs app-text-muted hidden md:block">Bilişim Vadisi Ödülü - Barolar Birliği Çalıştayı ve Sunumu - Konferans Katılımı</div>
      </div>
      <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <div
          v-for="card in gallery"
          :key="card.title"
          class="group relative overflow-hidden rounded-3xl border app-border app-surface-soft"
        >
          <div class="absolute inset-0 bg-gradient-to-br from-sky-400/10 via-transparent to-amber-400/10 opacity-0 transition-opacity group-hover:opacity-100" />
          <img :src="`/gallery/${card.image}`" :alt="card.title" class="h-56 w-full object-cover transition-transform duration-500 group-hover:scale-105" />
          <div class="relative space-y-2 p-5">
            <div class="text-xs uppercase tracking-[0.2em] app-text-muted">{{ card.location }}</div>
            <div class="text-lg font-semibold app-text-primary">{{ card.title }}</div>
            <div class="text-xs app-text-muted">{{ card.note }}</div>
          </div>
        </div>
      </div>
    </section>

    <section class="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
      <div class="rounded-3xl border app-border app-surface p-6 space-y-6">
        <div>
          <div class="text-xs uppercase tracking-[0.25em] app-text-muted">Hocalar</div>
          <h2 class="text-2xl font-semibold app-text-primary">Akademik Danışmanlar</h2>
        </div>
        <div class="space-y-4">
          <div v-for="mentor in mentors" :key="mentor.name" class="rounded-2xl border app-border app-surface-soft p-4">
            <div class="text-lg font-semibold app-text-primary">{{ mentor.name }}</div>
            <div class="text-sm app-text-secondary">{{ mentor.role }}</div>
            <div class="mt-2 text-xs app-text-muted">{{ mentor.focus }}</div>
            <a
              v-if="mentor.email"
              :href="'mailto:' + mentor.email"
              class="mt-3 inline-flex text-xs font-semibold app-text-primary underline"
            >
              {{ mentor.email }}
            </a>
          </div>
        </div>
      </div>

      <div class="rounded-3xl border app-border app-surface p-6">
        <div class="flex items-center justify-between">
          <div>
            <div class="text-xs uppercase tracking-[0.25em] app-text-muted">Ekip</div>
            <h2 class="text-2xl font-semibold app-text-primary">Projeyi Tasarlayanlar</h2>
          </div>
          <div class="text-xs app-text-muted">Araştırma + Ürün</div>
        </div>
        <div class="mt-6 grid gap-4 md:grid-cols-2">
          <div v-for="member in team" :key="member.name" class="rounded-2xl border app-border app-surface-soft p-4">
            <div class="text-sm font-semibold app-text-primary">{{ member.name }}</div>
            <div class="text-xs app-text-secondary">{{ member.role }}</div>
            <div class="mt-2 text-xs app-text-muted">{{ member.bio }}</div>
            <a
              v-if="member.email"
              :href="'mailto:' + member.email"
              class="mt-3 inline-flex text-xs font-semibold app-text-primary underline"
            >
              {{ member.email }}
            </a>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const currentSlide = ref(1)
const totalSlides = 15 // Toplam PNG sayısı
let slideTimer = null

const milestones = [
  { title: 'Literatür taraması ve hipotez', detail: 'Hukukta semantik arama için sorun tanımı ve araştırma kapsamı.' },
  { title: 'Veri toplama ve temizleme', detail: 'Taranmış kararların VisionLM ile ön işlemesi ve doğrulama süreci.' },
  { title: 'Modelleme ve deneme', detail: 'Retrieve + Re-rank deneyleri ve kalite metrikleri.' },
  { title: 'Yayın Süreci', detail: 'ITTA 26 konferansı için bildiri hazırlığı.' },
  { title: 'Teslim ve Sunum', detail: 'Web sitesi geliştirme, Proje Pazarı final sunum' },
]

const gallery = [
  { title: 'Barolar Birliği Sunumu', location: 'TBB', note: 'Proje/Ürün Sunumları', image: 'sunum-tbb.jpg' },
  { title: 'Yapay Zeka ve Avukatlık Çalıştayı', location: 'TBB', note: 'Law Bridge Ürün Tanıtımı', image: 'calistay-tbb.jpg' },
  { title: 'ITTA Konferansı', location: 'Azerbaycan', note: 'Bildiri Sunumu', image: 'itta-kübra-refik-hoca.jpg' },
  { title: 'Ekip Fotoğrafı', location: 'Adalet Bakanlığı', note: 'Bilişim Vadisi Ödülleri', image: 'toplu.jpg' },
]

const mentors = [
  { name: 'Refik Samet', role: 'Akademik Danışman', focus: 'Ankara Üniversitesi', email: 'samet@eng.ankara.edu.tr' },  
  { name: 'Yusuf Evren Aykaç', role: 'Akademik Danışman', focus: 'Yıldırım Beyazıt Üniversitesi', email: 'evrenaykac@gmail.com' },
]

const team = [
  { name: 'Ece İrem Şişer', role: 'Model geliştirme + frontend', bio: 'Ankara Üniversitesi', email: 'eceiremsiser@gmail.com' },
  { name: 'Derda Sina Günay', role: 'Model geliştirme + backend', bio: 'Ankara Üniversitesi', email: 'gunayderdasina@gmail.com' },
  { name: 'Kübra Kovayçin', role: 'Model geliştirme', bio: 'LawBridge takım lideri', email: 'kkovaycin@gmail.com' },
]

const preserveScroll = () => {
  const y = window.scrollY
  requestAnimationFrame(() => {
    window.scrollTo({ top: y })
  })
}

// 5 Saniyelik Temiz Sayaç
const startTimer = () => {
  if (slideTimer) clearInterval(slideTimer)
  slideTimer = setInterval(() => {
    nextSlide()
  }, 5000)
}

const stopTimer = () => {
  if (slideTimer) clearInterval(slideTimer)
}

const nextSlide = () => {
  preserveScroll()
  currentSlide.value = currentSlide.value >= totalSlides ? 1 : currentSlide.value + 1
  startTimer() // Tuşa basılınca sayacı sıfırla
}

const prevSlide = () => {
  preserveScroll()
  currentSlide.value = currentSlide.value <= 1 ? totalSlides : currentSlide.value - 1
  startTimer() // Tuşa basılınca sayacı sıfırla
}

// Resimleri önceden yükle (Preload) ki interneti yavaş olsa bile sıfır gecikme olsun
const preloadImages = () => {
  for (let i = 1; i <= totalSlides; i++) {
    const img = new Image()
    img.src = `/slides/slide-${i}.jpg`
  }
}

onMounted(() => {
  preloadImages()
  startTimer()
})

onUnmounted(() => {
  stopTimer()
})
</script>

<style scoped>
/* Vue'nun Native Geçiş Efekti (Crossfade) */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s ease-in-out;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>