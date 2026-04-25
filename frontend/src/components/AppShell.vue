<script setup>
import { computed } from 'vue'
import { PanelLeftOpen } from 'lucide-vue-next'
import AppSidebar from './AppSidebar.vue'
import { useUiStore } from '../stores/ui'

const ui = useUiStore()

const contentOffsetClass = computed(() => (ui.sidebarCollapsed ? 'lg:pl-[92px]' : 'lg:pl-[280px]'))
</script>

<template>
  <!-- Root container: w-full ve overflow-x-hidden eklendi -->
  <div class="min-h-dvh w-full overflow-x-hidden transition-colors duration-300"
       :class="ui.theme === 'dark' ? 'bg-[#050505] text-white' : 'bg-white text-slate-900'">
    
    <AppSidebar
      :collapsed="ui.sidebarCollapsed"
      :mobile-open="ui.mobileSidebarOpen"
      @toggle-sidebar="ui.toggleSidebar"
      @close-mobile="ui.closeMobileSidebar"
    />

    <div class="fixed right-4 top-4 z-50 flex lg:hidden items-center gap-2">
      <button
        type="button"
        class="grid size-10 place-items-center rounded-xl border app-border app-surface app-text-secondary shadow-md transition hover:app-surface-soft hover:app-text-primary"
        @click="ui.openMobileSidebar"
      >
        <PanelLeftOpen class="size-4" />
      </button>
    </div>

    <!-- main kısmına relative ve overflow-hidden ekleyerek taşan çizgileri kesiyoruz -->
    <main :class="contentOffsetClass" class="transition-all duration-300 relative overflow-hidden">
      <div class="mx-auto max-w-[1200px] px-4 py-10 sm:px-6 lg:px-10">
        <RouterView />
      </div>
    </main>
  </div>
</template>