<template>
  <div class="min-h-[70vh] grid place-items-center">
    <div class="w-full max-w-md">
      <div class="rounded-3xl border app-border app-surface p-8 shadow-xl">
        <div class="text-center space-y-2">
          <div class="text-xs uppercase tracking-[0.35em] app-text-muted">Akademik Giriş</div>
          <h2 class="text-3xl font-semibold app-text-primary">Hukuki Asistan</h2>
          <p class="text-sm app-text-secondary">Üniversite erişim paneli</p>
        </div>

        <div class="mt-6 grid grid-cols-2 gap-2 rounded-2xl border app-border app-surface-soft p-1 text-xs font-semibold">
          <button
            type="button"
            class="rounded-xl px-3 py-2 transition"
            :class="mode === 'login' ? 'app-surface app-text-primary' : 'app-text-muted'"
            @click="mode = 'login'"
          >
            Giriş Yap
          </button>
          <button
            type="button"
            class="rounded-xl px-3 py-2 transition"
            :class="mode === 'register' ? 'app-surface app-text-primary' : 'app-text-muted'"
            @click="mode = 'register'"
          >
            Kayıt Ol
          </button>
        </div>

        <form class="mt-6 space-y-5" @submit.prevent="handleSubmit">
          <div class="space-y-4">
            <div v-if="mode === 'register'">
              <label class="block text-xs font-semibold uppercase tracking-[0.2em] app-text-muted">Ad Soyad</label>
              <input
                v-model="name"
                type="text"
                required
                class="mt-2 w-full rounded-2xl border app-border app-surface-soft px-4 py-3 text-sm app-text-primary placeholder:app-text-muted focus:outline-none focus:ring-2 focus:ring-slate-300"
                placeholder="Ad Soyad"
              >
            </div>
            <div>
              <label class="block text-xs font-semibold uppercase tracking-[0.2em] app-text-muted">E-posta</label>
              <input
                v-model="email"
                type="email"
                required
                class="mt-2 w-full rounded-2xl border app-border app-surface-soft px-4 py-3 text-sm app-text-primary placeholder:app-text-muted focus:outline-none focus:ring-2 focus:ring-slate-300"
                placeholder="akademik@ankara.edu.tr"
              >
            </div>
            <div>
              <label class="block text-xs font-semibold uppercase tracking-[0.2em] app-text-muted">Şifre</label>
              <input
                v-model="password"
                type="password"
                required
                class="mt-2 w-full rounded-2xl border app-border app-surface-soft px-4 py-3 text-sm app-text-primary placeholder:app-text-muted focus:outline-none focus:ring-2 focus:ring-slate-300"
                placeholder="••••••••"
              >
            </div>
          </div>

          <div v-if="error" class="rounded-2xl border border-rose-200 bg-rose-50 px-4 py-2 text-xs text-rose-600">
            {{ error }}
          </div>
          <div v-if="message" class="rounded-2xl border border-emerald-200 bg-emerald-50 px-4 py-2 text-xs text-emerald-700">
            {{ message }}
          </div>

          <button
            type="submit"
            class="w-full rounded-2xl bg-slate-900 px-4 py-3 text-sm font-semibold text-white transition hover:bg-[#0f1d3a] dark:bg-white dark:text-black dark:hover:bg-slate-200"
          >
            {{ mode === 'login' ? 'Giriş Yap' : 'Kayıt Ol' }}
          </button>
        </form>

        <div class="mt-6 rounded-2xl border app-border app-surface-soft px-4 py-3 text-xs app-text-muted text-center">
          {{ mode === 'login' ? 'Giriş için kayıtlı bir hesap kullanın.' : 'Kayıt olduktan sonra giriş yapabilirsiniz.' }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()
const mode = ref('login')
const name = ref('')
const email = ref('')
const password = ref('')
const error = ref('')
const message = ref('')

const handleSubmit = async () => {
  error.value = ''
  message.value = ''

  if (mode.value === 'register') {
    const result = auth.register({ name: name.value.trim(), email: email.value.trim(), password: password.value })
    if (!result.ok) {
      error.value = result.message
      return
    }
    message.value = 'Kayit basarili. Yonlendiriliyorsunuz.'
    router.push('/')
    return
  }

  const result = await auth.login(email.value.trim(), password.value)
  if (!result.ok) {
    error.value = result.message
    return
  }
  router.push('/')
}
</script>