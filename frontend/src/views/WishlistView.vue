<template>
  <div class="container py-5">
    <h2 class="fw-bold mb-5">My Wishlist</h2>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-orange-500"></div>
    </div>

    <div v-else-if="products.length === 0" class="text-center py-5">
      <div style="font-size:4rem">❤️</div>
      <h5 class="mt-3">Your wishlist is empty</h5>
      <router-link to="/products" class="btn-shop mt-3 d-inline-flex">Discover Products</router-link>
    </div>

    <div v-else class="row g-4">
      <div v-for="product in products" :key="product.id" class="col-sm-6 col-lg-3">
        <ProductCard :product="product" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/utils/api'
import ProductCard from '@/components/product/ProductCard.vue'

const products = ref([])
const loading = ref(true)

onMounted(async () => {
  const { data } = await api.get('/wishlist/')
  products.value = data.products || []
  loading.value = false
})
</script>
