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
        <div class="text-sm font-semibold text-slate-900">Kaydedilmiş Kararlar </div>
        <div class="mt-1 text-xs text-slate-500">
          Kaydettiğiniz emsal kararlar burada saklanır.
        </div>
      </div>

      <div class="flex sm:justify-end">
        <button
          type="button"
          class="mt-2 inline-flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-3 py-2 text-xs font-semibold text-slate-700 shadow-sm transition hover:bg-slate-50 sm:mt-6"
          @click="router.push({ name: 'search' })"
        >
          <ArrowLeft class="size-4" />
          Search
        </button>
      </div>
    </div>

    <div v-if="items.length === 0" class="mt-7 rounded-2xl border border-slate-200 bg-white p-6">
      <div class="text-sm font-semibold text-slate-900">Henüz kaydedilmiş karar yok.</div>
      <div class="mt-2 text-sm text-slate-600">
        Arama sonuçlarında yer alan yer imi ikonuna tıklayarak kararları kaydedebilirsiniz.
      </div>
    </div>

    <div v-else class="mt-7 grid gap-4 md:grid-cols-2">
      <article
        v-for="item in items"
        :key="item.id"
        class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"
      >
        <div class="flex items-start justify-between gap-4">
          <div class="min-w-0">
            <div class="truncate text-[13px] font-semibold text-slate-900">
              {{ item.metadata.court_name }}
            </div>
            <div class="mt-1 text-xs text-slate-500">
              {{ item.metadata.karar_no }} • {{ item.metadata.esas_no }}
            </div>
          </div>

          <button
            type="button"
            class="grid size-10 place-items-center rounded-xl border border-slate-200 bg-white text-slate-700 shadow-sm transition hover:bg-slate-50"
            @click="saved.removeCase(item.id)"
            aria-label="Remove saved case"
          >
            <BookmarkX class="size-4" />
          </button>
        </div>

        <p class="mt-4 line-clamp-3 text-sm font-normal leading-relaxed text-slate-700">
          {{ item.summary_for_human }}
        </p>

        <div class="mt-5">
          <button
            type="button"
            class="inline-flex items-center gap-2 rounded-xl bg-slate-900 px-3 py-2 text-xs font-semibold text-white shadow-sm transition hover:bg-slate-800"
            @click="openDetails(item)"
          >
            İncele
            <Arrow
            Right class="size-4" />
          </button>
        </div>
      </article>
    </div>

    <CaseDetailModal :open="modalOpen" :case-item="selected" @close="modalOpen = false" />
  </div>
</template>

