<template>
  <div class="min-vh-100 d-flex align-items-center" style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-sm-10 col-md-7 col-lg-5">
          <div class="bg-white rounded-4 shadow-lg p-5">
            <!-- Logo -->
            <div class="text-center mb-5">
              <router-link to="/" class="text-decoration-none">
                <h2 class="fw-bold text-dark">🛍️ Vue<span class="text-orange-500">Shop</span></h2>
              </router-link>
              <p class="text-muted mt-2">Welcome back! Please sign in.</p>
            </div>

            <!-- Error -->
            <div v-if="error" class="alert alert-danger rounded-3 text-sm">{{ error }}</div>

            <!-- Form -->
            <form @submit.prevent="handleLogin">
              <div class="mb-3">
                <label class="form-label fw-medium">Email</label>
                <input v-model="email" type="email" class="input-shop" placeholder="you@example.com" required />
              </div>
              <div class="mb-4">
                <label class="form-label fw-medium">Password</label>
                <input v-model="password" :type="showPw ? 'text' : 'password'" class="input-shop" placeholder="Your password" required />
                <button type="button" @click="showPw = !showPw" class="btn btn-link text-muted p-0 text-sm mt-1">
                  {{ showPw ? 'Hide' : 'Show' }} password
                </button>
              </div>

              <button type="submit" :disabled="loading" class="btn-shop w-100 justify-content-center py-3">
                {{ loading ? 'Signing in...' : 'Sign In' }}
              </button>
            </form>

            <p class="text-center text-muted mt-4 mb-0">
              Don't have an account?
              <router-link to="/register" class="text-orange-500 fw-semibold text-decoration-none">Sign up</router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/store/modules/auth'
import { useCartStore } from '@/store/modules/cart'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const cartStore = useCartStore()

const email = ref('')
const password = ref('')
const showPw = ref(false)
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  loading.value = true
  error.value = ''
  try {
    await authStore.login(email.value, password.value)
    await cartStore.fetchCart()
    router.push(route.query.redirect || '/')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Invalid email or password.'
  } finally {
    loading.value = false
  }
}
</script>
