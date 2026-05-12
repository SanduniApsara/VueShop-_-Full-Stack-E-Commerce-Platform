<template>
  <div class="container py-5">
    <div v-if="category" class="mb-5">
      <h2 class="fw-bold mb-1">{{ category.name }}</h2>
      <p class="text-muted">{{ category.description || `Browse all ${category.name} products` }}</p>
    </div>

    <div v-if="productStore.loading" class="row g-4">
      <div v-for="i in 8" :key="i" class="col-sm-6 col-lg-3">
        <div class="skeleton rounded-3" style="height:340px;"></div>
      </div>
    </div>

    <div v-else-if="productStore.products.length" class="row g-4">
      <div v-for="product in productStore.products" :key="product.id" class="col-sm-6 col-lg-3">
        <ProductCard :product="product" />
      </div>
    </div>

    <div v-else class="text-center py-5">
      <div style="font-size:4rem">😔</div>
      <h5 class="mt-3">No products in this category yet</h5>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useProductStore } from '@/store/modules/products'
import ProductCard from '@/components/product/ProductCard.vue'
import api from '@/utils/api'

const route = useRoute()
const productStore = useProductStore()
const category = ref(null)

async function load(slug) {
  try {
    const { data } = await api.get(`/categories/${slug}/`)
    category.value = data
  } catch {}
  await productStore.fetchProducts({ category: slug })
}

onMounted(() => load(route.params.slug))
watch(() => route.params.slug, slug => load(slug))
</script>
