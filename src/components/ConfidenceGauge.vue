<script setup>
import { computed } from 'vue'

const props = defineProps({
  score: { type: Number, default: 0 },
})

const normalizedScore = computed(() => Math.max(0, Math.min(100, Number(props.score) || 0)))

const tone = computed(() => {
  if (normalizedScore.value > 85) {
    return {
      rail: 'bg-emerald-100',
      fill: 'bg-emerald-500',
      text: 'text-emerald-700',
      badge: 'bg-emerald-50 ring-emerald-200',
      label: 'Yüksek Güven',
    }
  }
  if (normalizedScore.value >= 50) {
    return {
      rail: 'bg-amber-100',
      fill: 'bg-amber-500',
      text: 'text-amber-700',
      badge: 'bg-amber-50 ring-amber-200',
      label: 'Orta Güven',
    }
  }
  return {
    rail: 'bg-rose-100',
    fill: 'bg-rose-500',
    text: 'text-rose-700',
    badge: 'bg-rose-50 ring-rose-200',
    label: 'Düşük Güven',
  }
})
</script>

<template>
  <div
    class="min-w-[172px] rounded-xl px-3 py-2 ring-1"
    :class="[tone.badge, tone.text]"
    role="img"
    :aria-label="`Model güven skoru: %${normalizedScore}`"
  >
    <div class="flex items-center justify-between gap-2 text-[11px] font-semibold">
      <span>{{ tone.label }}</span>
      <span>%{{ normalizedScore }}</span>
    </div>
    <div class="mt-2 h-1.5 w-full overflow-hidden rounded-full" :class="tone.rail">
      <div class="h-full rounded-full transition-all duration-500" :class="tone.fill" :style="{ width: `${normalizedScore}%` }" />
    </div>
  </div>
</template>
