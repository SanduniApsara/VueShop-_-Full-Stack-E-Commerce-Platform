<template>
  <teleport to="body">
    <div class="toast-container position-fixed bottom-0 end-0 p-3" style="z-index: 9999;">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        :class="['toast show align-items-center border-0 mb-2', toastClass(toast.type)]"
        role="alert"
      >
        <div class="d-flex">
          <div class="toast-body fw-medium">
            {{ toast.icon }} {{ toast.message }}
          </div>
          <button @click="remove(toast.id)" type="button" class="btn-close btn-close-white me-2 m-auto"></button>
        </div>
      </div>
    </div>
  </teleport>
</template>

<script setup>
import { ref } from 'vue'

const toasts = ref([])
let counter = 0

function add(message, type = 'success') {
  const id = ++counter
  const icons = { success: '✅', error: '❌', warning: '⚠️', info: 'ℹ️' }
  toasts.value.push({ id, message, type, icon: icons[type] || '✅' })
  setTimeout(() => remove(id), 3500)
}

function remove(id) {
  toasts.value = toasts.value.filter(t => t.id !== id)
}

function toastClass(type) {
  const map = {
    success: 'bg-success text-white',
    error: 'bg-danger text-white',
    warning: 'bg-warning text-dark',
    info: 'bg-info text-white',
  }
  return map[type] || 'bg-success text-white'
}

// expose so other components can use via provide/inject or event bus
defineExpose({ add })
</script>
