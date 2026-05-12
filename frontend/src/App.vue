<template>
  <div id="app">
    <TheNavbar />
    <CartDrawer />
    <div class="overlay" :class="{ show: cartStore.drawerOpen }" @click="cartStore.closeDrawer" />

    <main class="min-vh-100">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <TheFooter />
    <ToastNotification />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import TheNavbar from '@/components/layout/TheNavbar.vue'
import TheFooter from '@/components/layout/TheFooter.vue'
import CartDrawer from '@/components/cart/CartDrawer.vue'
import ToastNotification from '@/components/ui/ToastNotification.vue'
import { useCartStore } from '@/store/modules/cart'
import { useProductStore } from '@/store/modules/products'
import { useAuthStore } from '@/store/modules/auth'

const cartStore = useCartStore()
const productStore = useProductStore()
const authStore = useAuthStore()

onMounted(async () => {
  await productStore.fetchCategories()
  if (authStore.isLoggedIn) {
    await cartStore.fetchCart()
  }
})
</script>
