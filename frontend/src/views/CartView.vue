<template>
  <div class="container py-5">
    <h2 class="fw-bold mb-5">Shopping Cart</h2>

    <div v-if="cartStore.loading" class="text-center py-5">
      <div class="spinner-border text-orange-500"></div>
    </div>

    <div v-else-if="cartStore.items.length === 0" class="text-center py-5">
      <div style="font-size:4rem">🛒</div>
      <h5 class="mt-3">Your cart is empty</h5>
      <router-link to="/products" class="btn-shop mt-3 d-inline-flex">Continue Shopping</router-link>
    </div>

    <div v-else class="row g-5">
      <!-- Items -->
      <div class="col-lg-8">
        <div class="card border-0 shadow-sm rounded-3 p-4">
          <div v-for="item in cartStore.items" :key="item.id" class="d-flex gap-4 py-4 border-bottom align-items-start">
            <img
              :src="item.product.image || '/placeholder.jpg'"
              :alt="item.product.name"
              class="rounded-3 object-fit-cover flex-shrink-0"
              style="width:96px;height:96px;"
            />
            <div class="flex-grow-1">
              <p class="text-xs text-orange-500 mb-1 text-uppercase tracking-wide">{{ item.product.category_name }}</p>
              <h6 class="fw-semibold mb-2">{{ item.product.name }}</h6>
              <p class="text-orange-500 fw-bold mb-3">${{ item.product.price }}</p>
              <div class="d-flex align-items-center gap-3">
                <div class="d-flex align-items-center border rounded-pill overflow-hidden">
                  <button @click="decrement(item)" class="btn border-0 px-3 py-1">−</button>
                  <span class="px-3 fw-medium">{{ item.quantity }}</span>
                  <button @click="increment(item)" class="btn border-0 px-3 py-1">+</button>
                </div>
                <button @click="cartStore.removeItem(item.id)" class="btn btn-link text-danger p-0 text-sm">Remove</button>
              </div>
            </div>
            <div class="text-end flex-shrink-0">
              <p class="fw-bold fs-6 mb-0">${{ Number(item.line_total).toFixed(2) }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Summary -->
      <div class="col-lg-4">
        <div class="card border-0 shadow-sm rounded-3 p-4 sticky-top" style="top: 80px;">
          <h6 class="fw-bold mb-4">Order Summary</h6>
          <div class="d-flex justify-content-between mb-2 text-sm">
            <span class="text-muted">Subtotal ({{ cartStore.totalItems }} items)</span>
            <span>${{ Number(cartStore.subtotal).toFixed(2) }}</span>
          </div>
          <div class="d-flex justify-content-between mb-2 text-sm">
            <span class="text-muted">Shipping</span>
            <span class="text-green-600">Free over $50</span>
          </div>
          <hr />
          <div class="d-flex justify-content-between fw-bold mb-4">
            <span>Estimated Total</span>
            <span class="text-orange-500 fs-5">${{ Number(cartStore.subtotal).toFixed(2) }}</span>
          </div>
          <router-link to="/checkout" class="btn-shop w-100 justify-content-center d-flex py-3">
            Proceed to Checkout →
          </router-link>
          <router-link to="/products" class="btn btn-light w-100 rounded-pill mt-2">
            Continue Shopping
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useCartStore } from '@/store/modules/cart'

const cartStore = useCartStore()

onMounted(() => cartStore.fetchCart())

function increment(item) {
  cartStore.updateItem(item.id, item.quantity + 1)
}
function decrement(item) {
  if (item.quantity > 1) cartStore.updateItem(item.id, item.quantity - 1)
  else cartStore.removeItem(item.id)
}
</script>
