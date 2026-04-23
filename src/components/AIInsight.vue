<script setup>
import { computed } from 'vue'
import { Sparkles } from 'lucide-vue-next'

const props = defineProps({
  item: { type: Object, required: true },
})

// Metni AI anlayacak şekilde "Summary for Human" odaklı hazırlar
const executiveSummary = computed(() => {
  const primary = props.item?.summary_for_human ?? ''
  const reasoning = props.item?.segments?.reasoning_text ?? ''
  
  // İlk cümleyi çekerek kısa tutar
  const compactReasoning = reasoning
    .split(/[.!?]+/)
    .map((part) => part.trim())
    .filter(Boolean)
    .slice(0, 1)
    .join('. ')

  return [primary, compactReasoning].filter(Boolean).join(' ')
})
</script>

<template>
  <!-- Section: Gri kutu (bg-slate) kaldırıldı, transparan ve border-left eklendi -->
  <section class="mt-4 border-l-2 app-border pl-4 py-2" aria-label="Legal AI Tech Summary">
    <div class="flex items-center gap-2 mb-2">
      <Sparkles class="size-3.5 text-amber-500 opacity-80" />
      <span class="text-[10px] uppercase tracking-widest app-text-muted font-bold">
        Özet Analiz
      </span>
    </div>
    
    <!-- Özet Metni: Artık doğrudan okunabilir ve tema uyumlu -->
    <p class="text-sm font-medium leading-relaxed app-text-secondary italic">
      "{{ executiveSummary }}"
    </p>
  </section>
</template>