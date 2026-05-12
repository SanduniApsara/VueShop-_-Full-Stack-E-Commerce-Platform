<template>
  <div class="card-shop group cursor-pointer animate-fade-in" @click="goToProduct">
    <!-- Image -->
    <div class="product-img-wrap relative" style="height: 240px; background: #f8fafc;">
      <img
        :src="product.image || '/placeholder.jpg'"
        :alt="product.name"
        class="w-100 h-100 object-fit-cover"
        loading="lazy"
      />
      <!-- Badges -->
      <span v-if="product.discount_percent > 0" class="badge-sale">-{{ product.discount_percent }}%</span>
      <span v-else-if="isNew" class="badge-new">New</span>

      <!-- Quick Add overlay -->
      <div class="quick-add-overlay">
        <button
          @click.stop="addToCart"
          :disabled="!product.is_in_stock || adding"
          class="btn text-white rounded-pill px-4 py-2 fw-medium"
          style="background: rgba(249,115,22,.9); backdrop-filter: blur(4px);"
        >
          <span v-if="adding">Adding...</span>
          <span v-else-if="!product.is_in_stock">Out of Stock</span>
          <span v-else>Add to Cart</span>
        </button>
      </div>

      <!-- Wishlist btn -->
      <button
        @click.stop="toggleWishlist"
        class="wishlist-btn"
        :class="{ active: inWishlist }"
        title="Add to wishlist"
      >
        {{ inWishlist ? '❤️' : '🤍' }}
      </button>
    </div>

    <!-- Info -->
    <div class="p-4">
      <p class="text-xs text-orange-500 font-medium uppercase tracking-wide mb-1">
        {{ product.category_name }}
      </p>
      <h3 class="text-sm font-semibold text-gray-800 mb-2 line-clamp-2 leading-snug">
        {{ product.name }}
      </h3>

      <!-- Stars -->
      <div class="d-flex align-items-center gap-1 mb-3">
        <span v-for="i in 5" :key="i" :class="i <= Math.round(product.average_rating) ? 'star-filled' : 'star-empty'" style="font-size:.85rem">★</span>
        <span class="text-xs text-gray-400 ms-1">({{ product.review_count }})</span>
      </div>

      <!-- Price -->
      <div class="d-flex align-items-center gap-2">
        <span class="fw-bold text-lg text-gray-900">${{ product.price }}</span>
        <span v-if="product.compare_price" class="text-sm text-gray-400 text-decoration-line-through">
          ${{ product.compare_price }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '@/store/modules/cart'

const props = defineProps({
  product: { type: Object, required: true }
})

const router = useRouter()
const cartStore = useCartStore()

const adding = ref(false)
const inWishlist = ref(false)

const isNew = computed(() => {
  const created = new Date(props.product.created_at)
  const now = new Date()
  return (now - created) / (1000 * 60 * 60 * 24) < 30
})

function goToProduct() {
  router.push(`/products/${props.product.slug}`)
}

async function addToCart() {
  adding.value = true
  try {
    await cartStore.addItem(props.product.id)
  } finally {
    adding.value = false
  }
}

function toggleWishlist() {
  inWishlist.value = !inWishlist.value
}
</script>

<style scoped>
.quick-add-overlay {
  position: absolute; inset: 0;
  display: flex; align-items: flex-end; justify-content: center;
  padding-bottom: 16px;
  opacity: 0; transition: opacity .25s;
  background: linear-gradient(to top, rgba(0,0,0,.15), transparent);
}
.card-shop:hover .quick-add-overlay { opacity: 1; }

.wishlist-btn {
  position: absolute; top: 10px; right: 10px;
  background: white; border: none; border-radius: 50%;
  width: 34px; height: 34px; display: flex; align-items: center; justify-content: center;
  font-size: 1rem; cursor: pointer; box-shadow: 0 2px 8px rgba(0,0,0,.1);
  transition: transform .2s;
}
.wishlist-btn:hover { transform: scale(1.1); }
</style>
