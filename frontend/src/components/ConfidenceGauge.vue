<script setup>
import { computed } from 'vue'

const props = defineProps({
  score: { type: Number, default: 0 },
})

// Backend (`crud_case.search_cases`) returns cosine similarity in [0.0, 1.0]
// over L2-normalised pgvector embeddings. Multiply by 100 to render as a
// percentage. We tolerate values already on a 0–100 scale so legacy data
// or future schema changes don't silently round to 0%.
const normalizedScore = computed(() => {
  const raw = Number(props.score)
  if (!Number.isFinite(raw)) return 0
  const pct = raw <= 1 ? raw * 100 : raw
  return Math.max(0, Math.min(100, Math.round(pct)))
})

// Thresholds calibrated for the BERTurk legal retriever:
//   • > 70%  → strong semantic match (green)
//   • 40–70% → relevant but partial match (amber)
//   • < 40%  → weak match (rose)
// These bands match what the model produces on the Turkish legal corpus —
// dense retrievers rarely exceed ~0.85 cosine similarity in practice.
const tone = computed(() => {
  if (normalizedScore.value > 70) {
    return {
      rail: 'bg-emerald-100',
      fill: 'bg-emerald-500',
      text: 'text-emerald-700',
      badge: 'bg-emerald-50 ring-emerald-200',
    }
  }
  if (normalizedScore.value >= 40) {
    return {
      rail: 'bg-amber-100',
      fill: 'bg-amber-500',
      text: 'text-amber-700',
      badge: 'bg-amber-50 ring-amber-200',
    }
  }
  return {
    rail: 'bg-rose-100',
    fill: 'bg-rose-500',
    text: 'text-rose-700',
    badge: 'bg-rose-50 ring-rose-200',
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
      <span>Eşleşme Oranı</span>
      <span>%{{ normalizedScore }}</span>
    </div>
    <div class="mt-2 h-1.5 w-full overflow-hidden rounded-full" :class="tone.rail">
      <div class="h-full rounded-full transition-all duration-500" :class="tone.fill" :style="{ width: `${normalizedScore}%` }" />
    </div>
  </div>
</template>
