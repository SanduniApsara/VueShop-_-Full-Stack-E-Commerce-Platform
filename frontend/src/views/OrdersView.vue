<template>
  <div class="container py-5">
    <h2 class="fw-bold mb-5">My Orders</h2>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-orange-500"></div>
    </div>

    <div v-else-if="orders.length === 0" class="text-center py-5">
      <div style="font-size: 4rem">📦</div>
      <h5 class="mt-3">No orders yet</h5>
      <router-link to="/products" class="btn-shop mt-3 d-inline-flex">Start Shopping</router-link>
    </div>

    <div v-else class="d-flex flex-column gap-4">
      <div
        v-for="order in orders"
        :key="order.id"
        class="card border-0 shadow-sm rounded-3 p-4"
      >
        <div class="d-flex justify-content-between align-items-start flex-wrap gap-3">
          <div>
            <p class="text-muted text-xs mb-1">Order Number</p>
            <h6 class="fw-bold mb-0">{{ order.order_number }}</h6>
          </div>
          <div>
            <p class="text-muted text-xs mb-1">Date</p>
            <p class="fw-medium mb-0">{{ formatDate(order.created_at) }}</p>
          </div>
          <div>
            <p class="text-muted text-xs mb-1">Total</p>
            <p class="fw-bold text-orange-500 mb-0">${{ order.total }}</p>
          </div>
          <div>
            <p class="text-muted text-xs mb-1">Status</p>
            <span :class="['badge rounded-pill px-3 py-2', statusClass(order.status)]">
              {{ order.status.charAt(0).toUpperCase() + order.status.slice(1) }}
            </span>
          </div>
          <router-link :to="`/orders/${order.id}`" class="btn btn-outline-secondary btn-sm rounded-pill px-4">
            View Details
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/utils/api'

const orders = ref([])
const loading = ref(true)

onMounted(async () => {
  const { data } = await api.get('/orders/')
  orders.value = data.results || data
  loading.value = false
})

function formatDate(d) {
  return new Date(d).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })
}

function statusClass(status) {
  const map = {
    pending: 'bg-yellow-100 text-yellow-700',
    confirmed: 'bg-blue-100 text-blue-700',
    processing: 'bg-purple-100 text-purple-700',
    shipped: 'bg-indigo-100 text-indigo-700',
    delivered: 'bg-green-100 text-green-700',
    cancelled: 'bg-red-100 text-red-700',
    refunded: 'bg-gray-100 text-gray-600',
  }
  return map[status] || 'bg-gray-100 text-gray-600'
}
</script>
