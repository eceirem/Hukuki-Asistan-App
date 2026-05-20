<script setup>
import { computed, ref } from 'vue'

// Generic "Daha fazla göster / Daha az göster" wrapper for long-form fields
// like tam_olay / gerekce / hüküm. Truncates on the RAW text (never on HTML),
// so optional inline highlighting (`formatter`) is always applied to a
// well-formed substring — no broken <mark> tags possible.
const props = defineProps({
  text: { type: String, default: '' },
  limit: { type: Number, default: 300 },
  formatter: { type: Function, default: null },
  textClass: { type: String, default: '' },
  expandLabel: { type: String, default: 'Daha fazla göster' },
  collapseLabel: { type: String, default: 'Daha az göster' },
})

const isExpanded = ref(false)

const safeText = computed(() => props.text ?? '')

const needsTruncation = computed(() => safeText.value.length > props.limit)

// Try to clip on the nearest word boundary inside the soft tail so we don't
// cut a word mid-syllable — keeps Turkish words like "kararının" intact.
function clipAtWordBoundary(input, max) {
  if (input.length <= max) return input
  const hardSlice = input.slice(0, max)
  const lastSpace = hardSlice.lastIndexOf(' ')
  const safeStart = Math.floor(max * 0.8)
  return lastSpace > safeStart ? hardSlice.slice(0, lastSpace) : hardSlice
}

const visibleText = computed(() => {
  if (!needsTruncation.value || isExpanded.value) return safeText.value
  return `${clipAtWordBoundary(safeText.value, props.limit).trimEnd()}…`
})

const renderedHtml = computed(() =>
  props.formatter ? props.formatter(visibleText.value) : null,
)

function toggle() {
  isExpanded.value = !isExpanded.value
}
</script>

<template>
  <div>
    <p
      v-if="formatter"
      :class="textClass"
      v-html="renderedHtml"
    ></p>
    <p v-else :class="textClass">{{ visibleText }}</p>

    <button
      v-if="needsTruncation"
      type="button"
      class="expandable-toggle mt-2 inline-flex items-center text-xs font-semibold tracking-wide transition-colors hover:underline focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2"
      @click="toggle"
    >
      {{ isExpanded ? collapseLabel : expandLabel }}
    </button>
  </div>
</template>

<style scoped>
.expandable-toggle {
  cursor: pointer;
  color: var(--app-accent-strong, #2563eb);
  letter-spacing: 0.02em;
}

.expandable-toggle:hover {
  opacity: 0.85;
}

.expandable-toggle:focus-visible {
  --tw-ring-color: var(--app-accent-strong, #2563eb);
  border-radius: 4px;
}
</style>
