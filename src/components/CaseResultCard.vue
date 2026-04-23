<script setup>
import { computed } from 'vue'
import { Bookmark, ArrowRight } from 'lucide-vue-next'
import { useSavedCasesStore } from '../stores/savedCases'
import ConfidenceGauge from './ConfidenceGauge.vue'

const props = defineProps({
  item: { type: Object, required: true },
})

const emit = defineEmits(['readMore'])

const saved = useSavedCasesStore()
const isSaved = computed(() => saved.isSaved(props.item.id))

const entityPatterns = [
  /\b(?:HMK|TTK|TBK|TMK|TCK)\b(?:\s*\d+(?:[-/]\d+)*)?/gu,
  /\b\d+\s+sayılı\s+Kanun\b/gu,
  /\b\d+\s*\.\s*Hukuk\s+Dairesi\b/gu,
  /\b\d+\s*\.\s*Asliye\s+(?:Hukuk|Ceza)\s+Mahkemesi\b/gu,
  /\b\d+\s*\.\s*Sulh\s+Ceza\s+Hakimliği\b/gu,
  /\b(?:Yargıtay|Danıştay|Anayasa Mahkemesi)\b/gu,
  /\b(?:madde|maddesi|maddeleri)\b/giu,
]

function escapeHtml(input = '') {
  return input
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;')
}

function highlightEntities(text = '') {
  let highlighted = escapeHtml(text)
  for (const pattern of entityPatterns) {
    highlighted = highlighted.replace(
      pattern,
      '<mark class="rounded px-1 py-0.5 bg-amber-100 text-amber-900">$&</mark>',
    )
  }
  return highlighted
}

const highlightedSummary = computed(() => highlightEntities(props.item.summary_for_human ?? ''))
</script>

<template>
  <article
    class="group relative rounded-2xl border app-border app-surface p-5 shadow-sm transition duration-200 hover:-translate-y-[1px] hover:shadow-[0_10px_24px_-14px_rgba(0,0,0,0.25)]"
  >
    <div class="absolute right-5 top-5">
      <ConfidenceGauge :score="item.match_score" />
    </div>

    <header class="pr-28">
      <div class="text-[13px] font-semibold app-text-primary">
        {{ item.metadata.court_name }}
      </div>
      <div class="mt-1 text-xs app-text-muted">
        {{ item.metadata.karar_no }} • {{ item.metadata.esas_no }}
      </div>
    </header>

    <div class="mt-4 grid gap-3">
      <div>
        <div class="text-[11px] font-semibold uppercase tracking-[0.18em] app-text-muted">Konu</div>
        <div class="mt-1 text-sm font-normal leading-relaxed app-text-secondary">
          {{ item.metadata.case_subject || item.meta_data?.case_subject }}
        </div>
      </div>
      <div>
        <div class="text-[11px] font-semibold uppercase tracking-[0.18em] app-text-muted">Özet</div>
        <p class="mt-1 line-clamp-3 text-sm font-normal leading-relaxed app-text-secondary" v-html="highlightedSummary"></p>
      </div>
    </div>

    <div class="mt-5 flex items-center justify-between gap-3">
      <button
        type="button"
        class="inline-flex items-center gap-2 rounded-xl border border-transparent px-3 py-2 text-xs font-semibold shadow-sm transition hover:opacity-90"
        :style="{ backgroundColor: 'var(--app-accent-strong)', color: 'var(--app-accent-strong-text)' }"
        @click="$emit('readMore', item)"
      >
        İncele
        <ArrowRight class="size-4" />
      </button>

      <button
        type="button"
        class="grid size-10 place-items-center rounded-xl border app-border app-surface app-text-secondary shadow-sm transition hover:app-surface-soft"
        :class="isSaved ? 'app-text-primary' : ''"
        @click="saved.toggleCase(item)"
        :aria-label="isSaved ? 'Remove bookmark' : 'Save case'"
      >
        <Bookmark class="size-4" :class="isSaved ? 'fill-slate-900' : ''" />
      </button>
    </div>
  </article>
</template>

