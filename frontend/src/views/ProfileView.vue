<template>
  <div class="container py-5" style="max-width: 760px;">
    <h2 class="fw-bold mb-5">My Profile</h2>

    <div class="card border-0 shadow-sm rounded-3 p-5">
      <div class="d-flex align-items-center gap-4 mb-5">
        <div class="avatar-lg">{{ userInitial }}</div>
        <div>
          <h5 class="fw-bold mb-1">{{ authStore.user?.first_name }} {{ authStore.user?.last_name }}</h5>
          <p class="text-muted mb-0">{{ authStore.user?.email }}</p>
        </div>
      </div>

      <div v-if="success" class="alert alert-success rounded-3 text-sm">Profile updated successfully ✅</div>
      <div v-if="error" class="alert alert-danger rounded-3 text-sm">{{ error }}</div>

      <form @submit.prevent="handleUpdate">
        <div class="row g-3">
          <div class="col-md-6">
            <label class="form-label fw-medium">First Name</label>
            <input v-model="form.first_name" class="input-shop" placeholder="First name" />
          </div>
          <div class="col-md-6">
            <label class="form-label fw-medium">Last Name</label>
            <input v-model="form.last_name" class="input-shop" placeholder="Last name" />
          </div>
          <div class="col-md-6">
            <label class="form-label fw-medium">Email</label>
            <input :value="authStore.user?.email" class="input-shop bg-gray-50" disabled />
          </div>
          <div class="col-md-6">
            <label class="form-label fw-medium">Phone</label>
            <input v-model="form.phone" class="input-shop" placeholder="+1 555 000 0000" />
          </div>
        </div>

        <div class="d-flex gap-3 mt-4">
          <button type="submit" :disabled="loading" class="btn-shop">
            {{ loading ? 'Saving...' : 'Save Changes' }}
          </button>
          <router-link to="/orders" class="btn btn-outline-secondary rounded-pill px-4">
            View Orders
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/store/modules/auth'

const authStore = useAuthStore()
const loading = ref(false)
const success = ref(false)
const error = ref('')

const form = ref({ first_name: '', last_name: '', phone: '' })

const userInitial = computed(() =>
  (authStore.user?.first_name?.[0] || authStore.user?.email?.[0] || '?').toUpperCase()
)

onMounted(() => {
  const u = authStore.user
  if (u) {
    form.value.first_name = u.first_name || ''
    form.value.last_name  = u.last_name  || ''
    form.value.phone      = u.phone      || ''
  }
})

async function handleUpdate() {
  loading.value = true
  error.value = ''
  success.value = false
  try {
    await authStore.updateProfile(form.value)
    success.value = true
    setTimeout(() => (success.value = false), 3000)
  } catch (e) {
    error.value = 'Failed to update profile.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.avatar-lg {
  width: 72px; height: 72px; border-radius: 50%;
  background: #f97316; color: white;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.75rem; font-weight: 700;
  flex-shrink: 0;
}
</style>
