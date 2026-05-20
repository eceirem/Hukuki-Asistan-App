<script setup>
import { computed, onMounted, ref } from 'vue'
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

onMounted(() => {
  saved.fetchSavedCases()
})
</script>

<template>
  <div>
    <div class="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
      <div>
        <div class="text-sm font-semibold app-text-primary">Kaydedilmiş Kararlar</div>
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
          Ara
        </button>
      </div>
    </div>

    <!-- Loading skeleton -->
    <div v-if="saved.loading" class="mt-7 grid gap-3 md:grid-cols-2">
      <div v-for="i in 4" :key="i" class="h-[160px] animate-pulse rounded-2xl border app-border app-surface" />
    </div>

    <!-- Error state -->
    <div v-else-if="saved.error" class="mt-7 rounded-2xl border border-red-200 bg-red-50 p-6 dark:border-red-800 dark:bg-red-950">
      <div class="text-sm font-semibold text-red-600 dark:text-red-400">{{ saved.error }}</div>
      <button
        type="button"
        class="mt-3 text-xs font-semibold text-red-500 underline hover:no-underline"
        @click="saved.fetchSavedCases()"
      >
        Tekrar dene
      </button>
    </div>

    <!-- Empty state -->
    <div v-else-if="items.length === 0" class="mt-7 rounded-2xl border app-border app-surface p-6">
      <div class="text-sm font-semibold app-text-primary">Henüz kaydedilmiş karar yok.</div>
      <div class="mt-2 text-sm app-text-secondary">
        Arama sonuçlarında yer alan yer imi ikonuna tıklayarak kararları kaydedebilirsiniz.
      </div>
    </div>

    <!-- Cases grid -->
    <div v-else class="mt-7 grid gap-4 md:grid-cols-2">
      <article
        v-for="item in items"
        :key="item.id"
        class="rounded-2xl border app-border app-surface p-5 shadow-sm"
      >
        <div class="flex items-start justify-between gap-4">
          <div class="min-w-0">
            <div class="truncate text-[13px] font-semibold app-text-primary">
              {{ item.mahkeme ?? '—' }}
            </div>
            <div class="mt-1 text-xs app-text-muted">
              {{ item.karar_no ?? '—' }} • {{ item.esas_no ?? '—' }}
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
          {{ item.sum_human ?? item.dava_konusu ?? '' }}
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

    <CaseDetailModal
      v-if="selected != null"
      :open="modalOpen"
      :case-item="selected"
      @close="modalOpen = false"
    />
  </div>
</template>
