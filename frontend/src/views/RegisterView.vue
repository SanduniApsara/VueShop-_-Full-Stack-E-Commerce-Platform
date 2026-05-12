<template>
  <div class="min-vh-100 d-flex align-items-center" style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-sm-10 col-md-7 col-lg-5">
          <div class="bg-white rounded-4 shadow-lg p-5">
            <div class="text-center mb-5">
              <router-link to="/" class="text-decoration-none">
                <h2 class="fw-bold text-dark">🛍️ Vue<span class="text-orange-500">Shop</span></h2>
              </router-link>
              <p class="text-muted mt-2">Create your free account</p>
            </div>

            <div v-if="error" class="alert alert-danger rounded-3 text-sm">{{ error }}</div>
            <div v-if="success" class="alert alert-success rounded-3 text-sm">
              Account created! <router-link to="/login">Sign in now →</router-link>
            </div>

            <form @submit.prevent="handleRegister" v-if="!success">
              <div class="row g-3 mb-3">
                <div class="col-6">
                  <label class="form-label fw-medium">First Name</label>
                  <input v-model="form.first_name" class="input-shop" placeholder="John" />
                </div>
                <div class="col-6">
                  <label class="form-label fw-medium">Last Name</label>
                  <input v-model="form.last_name" class="input-shop" placeholder="Doe" />
                </div>
              </div>
              <div class="mb-3">
                <label class="form-label fw-medium">Email</label>
                <input v-model="form.email" type="email" class="input-shop" placeholder="you@example.com" required />
              </div>
              <div class="mb-3">
                <label class="form-label fw-medium">Password</label>
                <input v-model="form.password" type="password" class="input-shop" placeholder="Min. 8 characters" required />
              </div>
              <div class="mb-4">
                <label class="form-label fw-medium">Confirm Password</label>
                <input v-model="form.password2" type="password" class="input-shop" placeholder="Repeat password" required />
              </div>
              <button type="submit" :disabled="loading" class="btn-shop w-100 justify-content-center py-3">
                {{ loading ? 'Creating Account...' : 'Create Account' }}
              </button>
            </form>

            <p class="text-center text-muted mt-4 mb-0">
              Already have an account?
              <router-link to="/login" class="text-orange-500 fw-semibold text-decoration-none">Sign in</router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/store/modules/auth'

const authStore = useAuthStore()
const loading = ref(false)
const error = ref('')
const success = ref(false)

const form = ref({ first_name: '', last_name: '', email: '', password: '', password2: '' })

async function handleRegister() {
  loading.value = true
  error.value = ''
  try {
    await authStore.register(form.value)
    success.value = true
  } catch (e) {
    const data = e.response?.data
    error.value = data?.email?.[0] || data?.password?.[0] || data?.detail || 'Registration failed.'
  } finally {
    loading.value = false
  }
}
</script>
