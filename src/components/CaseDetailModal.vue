<script setup>
import { computed, onMounted, onUnmounted } from 'vue'
import { XCircle, Bookmark, FileText, Scale, CheckCircle2 } from 'lucide-vue-next'
import { useSavedCasesStore } from '../stores/savedCases'

const props = defineProps({
  open: { type: Boolean, default: false },
  caseItem: { type: Object, default: null },
})

const emit = defineEmits(['close'])

const saved = useSavedCasesStore()
const isSaved = computed(() => saved.isSaved(props.caseItem?.id))

const entityPatterns = [
  /\b(?:HMK|TTK|TBK|TMK|TCK|5651)\b(?:\s*\d+(?:[-/]\d+)*)?/gu,
  /\b\d+\s+sayılı\s+Kanun\b/gu,
  /\b\d+\s*\.\s*Hukuk\s+Dairesi\b/gu,
  /\b\d+\s*\.\s*Asliye\s+(?:Hukuk|Ceza)\s+Mahkemesi\b/gu,
  /\b\d+\s*\.\s+Sulh\s+Ceza\s+Hakimliği\b/gu,
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

function highlightLegalText(text = '') {
  let highlighted = escapeHtml(text)
  for (const pattern of entityPatterns) {
    highlighted = highlighted.replace(
      pattern,
      '<mark class="modal-highlight rounded px-1 py-0.5">$&</mark>',
    )
  }
  return highlighted
}

const factsHtml = computed(() => highlightLegalText(props.caseItem?.segments?.facts_text ?? ''))
const reasoningHtml = computed(() => highlightLegalText(props.caseItem?.segments?.reasoning_text ?? ''))
const verdictHtml = computed(() => highlightLegalText(props.caseItem?.segments?.verdict_text ?? ''))

function onKeydown(e) {
  if (!props.open) return
  if (e.key === 'Escape') emit('close')
}

onMounted(() => window.addEventListener('keydown', onKeydown))
onUnmounted(() => window.removeEventListener('keydown', onKeydown))
</script>

<template>
  <Teleport to="body">
    <div
      v-if="open && caseItem"
      class="fixed inset-0 z-50 flex items-end justify-center p-4 sm:items-center"
      role="dialog"
      aria-modal="true"
    >
      <button
        type="button"
        class="absolute inset-0 modal-backdrop backdrop-blur-[8px]"
        @click="$emit('close')"
        aria-label="Close"
      />

      <div
        class="modal-surface modal-border relative w-full max-w-4xl overflow-hidden rounded-2xl shadow-[0_24px_80px_-24px_rgba(0,0,0,0.45)]"
      >
        <div class="flex items-start justify-between gap-4 border-b modal-border px-6 py-5">
          <div class="min-w-0">
            <div class="modal-title text-[13px] font-semibold tracking-[0.12em]">
              {{ caseItem.metadata.court_name }}
            </div>
            <div class="modal-meta mt-2 text-[11px] uppercase tracking-[0.2em]">
              {{ caseItem.metadata.karar_no }} • {{ caseItem.metadata.esas_no }} •
              {{ caseItem.metadata.case_subject }}
            </div>
          </div>

          <div class="flex items-center gap-2">
            <button
              type="button"
              class="inline-flex items-center gap-2 rounded-xl border app-border app-surface px-3 py-2 text-xs font-semibold app-text-primary shadow-sm transition hover:app-surface-soft"
              @click="saved.toggleCase(caseItem)"
            >
              <Bookmark class="size-4" :class="isSaved ? 'fill-current' : ''" />
              {{ isSaved ? 'Kaydedildi' : 'Kaydet' }}
            </button>
            <button
              type="button"
              class="grid size-10 place-items-center rounded-xl app-text-secondary transition hover:app-surface-soft hover:app-text-primary"
              @click="$emit('close')"
              aria-label="Close"
            >
              <XCircle class="size-4" />
            </button>
          </div>
        </div>

        <div class="modal-scroll max-h-[75vh] overflow-y-auto px-6 py-6">
          <section class="modal-accent-amber border-l pl-4">
            <div class="modal-note-title text-[12px] font-semibold tracking-[0.12em]">
              Neden bu karar getirildi?
            </div>
            <div class="modal-note-text mt-2 text-sm italic leading-relaxed">
              {{ caseItem.xai_explanation }}
            </div>
          </section>

          <div class="mt-6 grid gap-6">
            <section class="modal-accent-sky border-l pl-4">
              <div class="modal-section-title flex items-center gap-2 text-[12px] font-semibold tracking-[0.12em]">
                <FileText class="modal-icon size-3.5" />
                Olay
              </div>
              <p class="modal-section-text mt-2 whitespace-pre-line text-sm leading-relaxed" v-html="factsHtml"></p>
            </section>

            <section class="modal-accent-emerald border-l pl-4">
              <div class="modal-section-title flex items-center gap-2 text-[12px] font-semibold tracking-[0.12em]">
                <Scale class="modal-icon size-3.5" />
                Gerekçe
              </div>
              <p class="modal-section-text mt-2 whitespace-pre-line text-sm leading-relaxed" v-html="reasoningHtml"></p>
            </section>

            <section class="modal-accent-violet border-l pl-4">
              <div class="modal-section-title flex items-center gap-2 text-[12px] font-semibold tracking-[0.12em]">
                <CheckCircle2 class="modal-icon size-3.5" />
                Hüküm
              </div>
              <p class="modal-section-text mt-2 whitespace-pre-line text-sm leading-relaxed" v-html="verdictHtml"></p>
            </section>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

