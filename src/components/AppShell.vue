<script setup>
import { computed } from 'vue'
import { Moon, Sun, PanelLeftOpen } from 'lucide-vue-next'
import AppSidebar from './AppSidebar.vue'
import { useUiStore } from '../stores/ui'

const ui = useUiStore()

// Yan menü açık/kapalıyken içeriğin ne kadar kayacağını hesaplar
const contentOffsetClass = computed(() => (ui.sidebarCollapsed ? 'lg:pl-[92px]' : 'lg:pl-[280px]'))
</script>

<template>
  <!-- En dış div: Gerçek siyah arka plan burada başlar -->
  <div class="min-h-dvh app-bg app-text-primary transition-colors duration-300">
    <AppSidebar
      :collapsed="ui.sidebarCollapsed"
      :mobile-open="ui.mobileSidebarOpen"
      @toggle-sidebar="ui.toggleSidebar"
      @close-mobile="ui.closeMobileSidebar"
    />

    <!-- Sağ üst kontrol butonları -->
    <div class="fixed right-4 top-4 z-50 flex items-center gap-2">
      <button
        type="button"
        class="grid size-10 place-items-center rounded-xl border app-border app-surface app-text-secondary shadow-md transition hover:app-surface-soft hover:app-text-primary"
        :aria-label="ui.theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'"
        @click="ui.toggleTheme"
      >
        <Sun v-if="ui.theme === 'dark'" class="size-4" />
        <Moon v-else class="size-4" />
      </button>

      <button
        type="button"
        class="grid size-10 place-items-center rounded-xl border app-border app-surface app-text-secondary shadow-md transition lg:hidden hover:app-surface-soft hover:app-text-primary"
        aria-label="Open navigation"
        @click="ui.openMobileSidebar"
      >
        <PanelLeftOpen class="size-4" />
      </button>
    </div>

    <!-- Ana İçerik Alanı -->
    <main :class="contentOffsetClass" class="transition-all duration-300">
      <div class="mx-auto max-w-[1200px] px-4 py-10 sm:px-6 lg:px-10">
        <RouterView />
      </div>
    </main>
  </div>
</template>