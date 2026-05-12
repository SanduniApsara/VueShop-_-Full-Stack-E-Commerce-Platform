<template>
  <div class="cart-drawer" :class="{ open: cartStore.drawerOpen }">
    <div class="d-flex flex-column h-100">
      <!-- Header -->
      <div class="d-flex align-items-center justify-content-between p-4 border-bottom">
        <h5 class="mb-0 fw-bold" style="font-family: 'Playfair Display', serif;">
          Shopping Cart
          <span v-if="cartStore.totalItems > 0" class="badge rounded-pill ms-2 text-white" style="background:#f97316; font-size:.75rem;">
            {{ cartStore.totalItems }}
          </span>
        </h5>
        <button @click="cartStore.closeDrawer" class="btn btn-light btn-sm rounded-circle p-1 lh-1">✕</button>
      </div>

      <!-- Items -->
      <div class="flex-grow-1 overflow-auto p-3">
        <div v-if="cartStore.loading" class="text-center py-5 text-muted">Loading...</div>

        <div v-else-if="cartStore.items.length === 0" class="text-center py-5">
          <div style="font-size: 3.5rem;">🛒</div>
          <h6 class="mt-3 text-muted">Your cart is empty</h6>
          <router-link to="/products" @click="cartStore.closeDrawer" class="btn-shop mt-3 d-inline-flex">
            Start Shopping
          </router-link>
        </div>

        <div v-else>
          <CartItem
            v-for="item in cartStore.items"
            :key="item.id"
            :item="item"
            @remove="cartStore.removeItem(item.id)"
            @update="qty => cartStore.updateItem(item.id, qty)"
          />
        </div>
      </div>

      <!-- Footer -->
      <div v-if="cartStore.items.length > 0" class="border-top p-4">
        <div class="d-flex justify-content-between mb-2">
          <span class="text-muted">Subtotal</span>
          <span class="fw-semibold">${{ Number(cartStore.subtotal).toFixed(2) }}</span>
        </div>
        <p class="text-xs text-muted mb-3">Shipping & taxes calculated at checkout</p>

        <router-link
          to="/checkout"
          @click="cartStore.closeDrawer"
          class="btn-shop w-100 justify-content-center d-flex"
        >
          Checkout →
        </router-link>
        <router-link
          to="/cart"
          @click="cartStore.closeDrawer"
          class="btn btn-light w-100 mt-2 rounded-pill"
        >
          View Cart
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCartStore } from '@/store/modules/cart'
import CartItem from './CartItem.vue'

const cartStore = useCartStore()
</script>
