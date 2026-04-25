<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { Scale, Search, Bookmark, Home, UserCircle2, PanelLeftClose, PanelLeftOpen, Sun, Moon } from 'lucide-vue-next'
import { useSavedCasesStore } from '../stores/savedCases'
import { useUiStore } from '../stores/ui'

const props = defineProps({
  collapsed: { type: Boolean, default: false },
  mobileOpen: { type: Boolean, default: false },
})

const emit = defineEmits(['closeMobile', 'toggleSidebar'])
const ui = useUiStore()
const route = useRoute()
const saved = useSavedCasesStore()

const nav = computed(() => [
  { name: 'Ana Sayfa', to: { name: 'home' }, icon: Home, active: route.name === 'home' },
  { name: 'Ara', to: { name: 'search' }, icon: Search, active: route.name === 'search' },
  { name: 'Kaydedilmiş Kararlar', to: { name: 'saved' }, icon: Bookmark, active: route.name === 'saved', badge: saved.savedCount },
])

const desktopWidthClass = computed(() => (props.collapsed ? 'lg:w-[92px]' : 'lg:w-[280px]'))
</script>

<template>
  <div v-if="mobileOpen" class="fixed inset-0 z-40 bg-black/40 backdrop-blur-[2px] lg:hidden" @click="emit('closeMobile')" />

  <aside
    class="fixed inset-y-0 left-0 z-50 flex border-r app-border app-surface dark:bg-[#0B0E14] dark:border-white/5 backdrop-blur-xl lg:z-40 lg:flex-col"
    :class="[desktopWidthClass, mobileOpen ? 'translate-x-0' : '-translate-x-full', 'w-[280px] transition-all duration-200 lg:translate-x-0']"
  >
    <div class="px-6 pt-6">
      <RouterLink :to="{ name: 'home' }" class="flex items-center" :class="collapsed ? 'justify-center' : 'gap-3'" @click="emit('closeMobile')">
        <div class="grid size-11 place-items-center rounded-xl border app-border app-surface shadow-[0_0_28px_rgba(59,130,246,0.08)]">
          <Scale class="size-5 app-text-primary" />
        </div>
        <div v-if="!collapsed" class="leading-tight">
          <div class="text-[15px] font-semibold tracking-[0.08em] app-text-primary">Hukuki Asistan</div>
          <div class="text-xs app-text-muted">Legal AI Tech</div>
        </div>
      </RouterLink>
    </div>

    <nav class="mt-7 px-3">
      <ul class="space-y-1">
        <li v-for="item in nav" :key="item.name">
          <RouterLink :to="item.to" class="group flex items-center justify-between rounded-xl px-3 py-2 text-[13px] font-medium transition"
            :class="item.active ? 'app-accent shadow-sm' : 'app-text-secondary app-hover-surface'" @click="emit('closeMobile')">
            <span class="flex items-center" :class="collapsed ? 'w-full justify-center' : 'gap-3'">
              <component :is="item.icon" class="size-4" :class="item.active ? 'app-text-primary' : 'app-text-muted group-hover:app-text-primary'" />
              <span v-if="!collapsed">{{ item.name }}</span>
            </span>
            <span v-if="item.badge && !collapsed" class="ml-3 inline-flex min-w-[24px] items-center justify-center rounded-full px-2 py-0.5 text-[11px]"
              :class="item.active ? 'bg-white/15 app-text-primary' : 'app-surface-soft app-text-muted'">
              {{ item.badge }}
            </span>
          </RouterLink>
        </li>
      </ul>
    </nav>

    <div class="mt-auto px-3 pb-4 space-y-2">
      <!-- Relocated Theme Toggle -->
      <button @click="ui.toggleTheme" class="flex w-full items-center gap-3 rounded-xl border app-border app-surface px-3 py-2 text-[13px] font-medium app-text-secondary transition hover:app-surface-soft">
        <Sun v-if="ui.theme === 'dark'" class="size-4" />
        <Moon v-else class="size-4" />
        <span v-if="!collapsed">{{ ui.theme === 'dark' ? 'Açık Tema' : 'Koyu Tema' }}</span>
      </button>

      <div class="rounded-2xl border app-border app-surface px-3 py-3 shadow-sm">
        <div class="flex items-center gap-3">
          <div class="grid size-10 place-items-center rounded-xl border app-border app-surface-soft">
            <UserCircle2 class="size-5 app-text-secondary" />
          </div>
          <div v-if="!collapsed" class="min-w-0 flex-1">
            <div class="truncate text-[13px] font-medium app-text-primary">Misafir</div>
            <div class="truncate text-xs app-text-muted">Profil ve ayarlar</div>
          </div>
          <button type="button" class="grid size-9 place-items-center rounded-xl border app-border app-surface app-text-secondary transition hover:app-surface-soft hover:app-text-primary" @click="emit('toggleSidebar')">
            <PanelLeftOpen v-if="collapsed" class="size-4" />
            <PanelLeftClose v-else class="size-4" />
          </button>
        </div>
      </div>
    </div>
  </aside>
</template>