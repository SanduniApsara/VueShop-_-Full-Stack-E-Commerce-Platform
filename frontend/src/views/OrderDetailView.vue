<template>
  <div class="container py-5" style="max-width: 860px;">
    <router-link to="/orders" class="btn btn-link text-muted text-decoration-none ps-0 mb-4 d-inline-flex align-items-center gap-1">
      ← Back to Orders
    </router-link>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-orange-500"></div>
    </div>

    <div v-else-if="order">
      <!-- Header -->
      <div class="d-flex flex-wrap justify-content-between align-items-start gap-3 mb-5">
        <div>
          <h2 class="fw-bold mb-1">Order {{ order.order_number }}</h2>
          <p class="text-muted mb-0">Placed on {{ formatDate(order.created_at) }}</p>
        </div>
        <span :class="['badge rounded-pill px-4 py-2 fs-6', statusClass(order.status)]">
          {{ order.status.charAt(0).toUpperCase() + order.status.slice(1) }}
        </span>
      </div>

      <div class="row g-4">
        <!-- Items -->
        <div class="col-lg-8">
          <div class="card border-0 shadow-sm rounded-3 p-4 mb-4">
            <h6 class="fw-bold mb-4">Items Ordered</h6>
            <div
              v-for="item in order.items"
              :key="item.id"
              class="d-flex gap-3 align-items-center py-3 border-bottom last:border-0"
            >
              <div class="bg-gray-100 rounded-2 d-flex align-items-center justify-content-center flex-shrink-0" style="width:60px;height:60px;">
                📦
              </div>
              <div class="flex-grow-1">
                <p class="fw-medium mb-0">{{ item.product_name }}</p>
                <p class="text-muted text-sm mb-0">SKU: {{ item.product_sku || 'N/A' }} &nbsp;|&nbsp; Qty: {{ item.quantity }}</p>
              </div>
              <div class="text-end">
                <p class="fw-bold mb-0">${{ Number(item.line_total).toFixed(2) }}</p>
                <p class="text-muted text-xs mb-0">${{ item.unit_price }} each</p>
              </div>
            </div>
          </div>

          <!-- Shipping -->
          <div class="card border-0 shadow-sm rounded-3 p-4">
            <h6 class="fw-bold mb-3">Shipping Address</h6>
            <p class="mb-1 fw-medium">{{ order.shipping_name }}</p>
            <p class="text-muted mb-1">{{ order.shipping_street }}</p>
            <p class="text-muted mb-1">{{ order.shipping_city }}, {{ order.shipping_state }} {{ order.shipping_postal_code }}</p>
            <p class="text-muted mb-0">{{ order.shipping_country }}</p>
            <div class="mt-3 pt-3 border-top" v-if="order.tracking_number">
              <p class="text-sm mb-0">
                📦 Tracking: <span class="fw-semibold text-orange-500">{{ order.tracking_number }}</span>
              </p>
            </div>
          </div>
        </div>

        <!-- Summary -->
        <div class="col-lg-4">
          <div class="card border-0 shadow-sm rounded-3 p-4">
            <h6 class="fw-bold mb-4">Order Summary</h6>
            <div class="d-flex flex-column gap-2 text-sm">
              <div class="d-flex justify-content-between">
                <span class="text-muted">Subtotal</span>
                <span>${{ order.subtotal }}</span>
              </div>
              <div class="d-flex justify-content-between">
                <span class="text-muted">Shipping</span>
                <span>${{ order.shipping_cost }}</span>
              </div>
              <div class="d-flex justify-content-between">
                <span class="text-muted">Tax</span>
                <span>${{ order.tax }}</span>
              </div>
            </div>
            <hr />
            <div class="d-flex justify-content-between fw-bold">
              <span>Total</span>
              <span class="text-orange-500 fs-5">${{ order.total }}</span>
            </div>

            <hr />
            <div class="text-sm">
              <p class="text-muted mb-1">Payment</p>
              <p class="fw-medium mb-0">
                {{ order.is_paid ? '✅ Paid' : '⏳ Pending payment' }}
              </p>
            </div>

            <div class="mt-3 text-sm">
              <p class="text-muted mb-1">Shipping Method</p>
              <p class="fw-medium mb-0 text-capitalize">{{ order.shipping_method }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/utils/api'

const route = useRoute()
const order = ref(null)
const loading = ref(true)

onMounted(async () => {
  const { data } = await api.get(`/orders/${route.params.id}/`)
  order.value = data
  loading.value = false
})

function formatDate(d) {
  return new Date(d).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })
}

function statusClass(status) {
  const map = {
    pending: 'bg-warning text-dark',
    confirmed: 'bg-primary text-white',
    processing: 'bg-purple text-white',
    shipped: 'bg-info text-white',
    delivered: 'bg-success text-white',
    cancelled: 'bg-danger text-white',
    refunded: 'bg-secondary text-white',
  }
  return map[status] || 'bg-secondary text-white'
}
</script>
