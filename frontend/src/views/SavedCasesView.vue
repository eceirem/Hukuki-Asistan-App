<script setup>
import { computed, ref } from 'vue'
import { BookmarkX, ArrowLeft, ArrowRight } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import { useSavedCasesStore } from '../stores/savedCases'
import CaseDetailModal from '../components/CaseDetailModal.vue'

const router = useRouter()
const saved = useSavedCasesStore()
const items = computed(() => saved.savedList)

const selected = ref(null)
const modalOpen = ref(false)

function openDetails(item) {
  selected.value = item
  modalOpen.value = true
}
</script>

<template>
  <div>
    <div class="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
      <div>
        <div class="text-sm font-semibold app-text-primary">Kaydedilmis Kararlar </div>
        <div class="mt-1 text-xs app-text-muted">
          Kaydettiğiniz emsal kararlar burada saklanır.
        </div>
      </div>

      <div class="flex sm:justify-end">
        <button
          type="button"
          class="mt-2 inline-flex items-center gap-2 rounded-xl border app-border app-surface px-3 py-2 text-xs font-semibold app-text-secondary shadow-sm transition hover:app-surface-soft sm:mt-6"
          @click="router.push({ name: 'search' })"
        >
          <ArrowLeft class="size-4" />
          Search
        </button>
      </div>
    </div>

    <div v-if="items.length === 0" class="mt-7 rounded-2xl border app-border app-surface p-6">
      <div class="text-sm font-semibold app-text-primary">Henuz kaydedilmis karar yok.</div>
      <div class="mt-2 text-sm app-text-secondary">
        Arama sonuçlarında yer alan yer imi ikonuna tıklayarak kararları kaydedebilirsiniz.
      </div>
    </div>

    <div v-else class="mt-7 grid gap-4 md:grid-cols-2">
      <article
        v-for="item in items"
        :key="item.id"
        class="rounded-2xl border app-border app-surface p-5 shadow-sm"
      >
        <div class="flex items-start justify-between gap-4">
          <div class="min-w-0">
            <div class="truncate text-[13px] font-semibold app-text-primary">
              {{ item.metadata.court_name }}
            </div>
            <div class="mt-1 text-xs app-text-muted">
              {{ item.metadata.karar_no }} • {{ item.metadata.esas_no }}
            </div>
          </div>

          <button
            type="button"
            class="grid size-10 place-items-center rounded-xl border app-border app-surface app-text-secondary shadow-sm transition hover:app-surface-soft"
            @click="saved.removeCase(item.id)"
            aria-label="Remove saved case"
          >
            <BookmarkX class="size-4" />
          </button>
        </div>

        <p class="mt-4 line-clamp-3 text-sm font-normal leading-relaxed app-text-secondary">
          {{ item.summary_for_human }}
        </p>

        <div class="mt-5">
          <button
            type="button"
            class="inline-flex items-center gap-2 rounded-xl app-accent-strong px-3 py-2 text-xs font-semibold shadow-sm transition hover:opacity-90"
            @click="openDetails(item)"
          >
            İncele
            <ArrowRight class="size-4" />
          </button>
        </div>
      </article>
    </div>

    <CaseDetailModal :open="modalOpen" :case-item="selected" @close="modalOpen = false" />
  </div>
</template>

