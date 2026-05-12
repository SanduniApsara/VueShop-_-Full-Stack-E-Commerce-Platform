<template>
  <div class="container py-5" v-if="product">
    <nav class="mb-4">
      <ol class="breadcrumb">
        <li class="breadcrumb-item"><router-link to="/">Home</router-link></li>
        <li class="breadcrumb-item"><router-link to="/products">Shop</router-link></li>
        <li class="breadcrumb-item text-muted">{{ product.name }}</li>
      </ol>
    </nav>

    <div class="row g-5">
      <!-- Image Gallery -->
      <div class="col-lg-6">
        <div class="product-img-wrap rounded-3 overflow-hidden mb-3" style="height: 480px; background: #f8fafc;">
          <img :src="activeImage || product.image" :alt="product.name" class="w-100 h-100 object-fit-cover" />
        </div>
        <div v-if="product.images?.length" class="d-flex gap-2 overflow-auto pb-1">
          <div
            v-for="img in [{ image: product.image }, ...product.images]"
            :key="img.image"
            @click="activeImage = img.image"
            :class="['thumb-img', activeImage === img.image && 'active']"
          >
            <img :src="img.image" class="w-100 h-100 object-fit-cover" />
          </div>
        </div>
      </div>

      <!-- Product Info -->
      <div class="col-lg-6">
        <p class="text-orange-500 fw-medium text-uppercase tracking-wide mb-2">{{ product.category?.name }}</p>
        <h1 class="fw-bold mb-3" style="font-size: 1.75rem; line-height: 1.3;">{{ product.name }}</h1>

        <!-- Rating -->
        <div class="d-flex align-items-center gap-2 mb-4">
          <div class="d-flex">
            <span v-for="i in 5" :key="i" :class="i <= Math.round(product.average_rating) ? 'star-filled' : 'star-empty'">★</span>
          </div>
          <span class="text-muted small">{{ product.average_rating }} ({{ product.review_count }} reviews)</span>
        </div>

        <!-- Price -->
        <div class="d-flex align-items-center gap-3 mb-4">
          <span class="fw-bold" style="font-size: 2rem;">${{ product.price }}</span>
          <span v-if="product.compare_price" class="text-muted text-decoration-line-through fs-5">${{ product.compare_price }}</span>
          <span v-if="product.discount_percent > 0" class="badge bg-red-100 text-red-600 rounded-pill px-3 py-2">
            {{ product.discount_percent }}% OFF
          </span>
        </div>

        <p class="text-muted mb-4">{{ product.short_description || product.description?.slice(0, 200) }}</p>

        <!-- Stock -->
        <div class="mb-4">
          <span v-if="product.is_in_stock" class="badge bg-green-100 text-green-700 rounded-pill px-3 py-2">
            ✅ In Stock ({{ product.stock }} left)
          </span>
          <span v-else class="badge bg-red-100 text-red-700 rounded-pill px-3 py-2">
            ❌ Out of Stock
          </span>
        </div>

        <!-- Quantity + Add to Cart -->
        <div class="d-flex gap-3 mb-4 flex-wrap">
          <div class="qty-control d-flex align-items-center border rounded-pill">
            <button @click="qty > 1 && qty--" class="btn border-0 px-3">−</button>
            <span class="px-3 fw-bold">{{ qty }}</span>
            <button @click="qty < product.stock && qty++" class="btn border-0 px-3">+</button>
          </div>
          <button
            @click="addToCart"
            :disabled="!product.is_in_stock || adding"
            class="btn-shop flex-grow-1 justify-content-center"
            style="font-size: 1rem;"
          >
            {{ adding ? 'Adding...' : '🛒 Add to Cart' }}
          </button>
          <button @click="toggleWishlist" class="btn btn-outline-secondary rounded-circle p-2">
            {{ inWishlist ? '❤️' : '🤍' }}
          </button>
        </div>

        <!-- Tags -->
        <div v-if="product.tags?.length" class="d-flex flex-wrap gap-2 mb-4">
          <span v-for="tag in product.tags" :key="tag.id" class="badge bg-gray-100 text-gray-600 rounded-pill px-3 py-2">
            #{{ tag.name }}
          </span>
        </div>

        <!-- Divider info -->
        <div class="border rounded-3 p-3 bg-gray-50">
          <div class="d-flex gap-4 text-sm text-muted flex-wrap">
            <span>🚚 Free shipping over $50</span>
            <span>🔄 30-day returns</span>
            <span>🔒 Secure checkout</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Description Tabs -->
    <div class="mt-5">
      <ul class="nav nav-tabs border-0 mb-4">
        <li v-for="tab in tabs" :key="tab.id" class="nav-item">
          <button :class="['nav-link', activeTab === tab.id && 'active fw-semibold']" @click="activeTab = tab.id">
            {{ tab.label }}
          </button>
        </li>
      </ul>

      <div v-if="activeTab === 'description'" class="text-muted lh-lg" v-html="formattedDescription"></div>
      <div v-if="activeTab === 'reviews'">
        <div v-if="product.reviews?.length === 0" class="text-muted text-center py-4">No reviews yet. Be the first!</div>
        <div v-else class="d-flex flex-column gap-3">
          <div v-for="review in product.reviews" :key="review.id" class="card border-0 bg-gray-50 rounded-3 p-4">
            <div class="d-flex justify-content-between mb-2">
              <strong>{{ review.user_name }}</strong>
              <div class="d-flex">
                <span v-for="i in 5" :key="i" :class="i <= review.rating ? 'star-filled' : 'star-empty'" style="font-size:.8rem">★</span>
              </div>
            </div>
            <p class="fw-medium mb-1">{{ review.title }}</p>
            <p class="text-muted small mb-0">{{ review.body }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div v-else-if="productStore.loading" class="container py-5 text-center">
    <div class="spinner-border text-orange-500"></div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useProductStore } from '@/store/modules/products'
import { useCartStore } from '@/store/modules/cart'

const route = useRoute()
const productStore = useProductStore()
const cartStore = useCartStore()

const qty = ref(1)
const adding = ref(false)
const inWishlist = ref(false)
const activeImage = ref(null)
const activeTab = ref('description')

const product = computed(() => productStore.currentProduct)

const formattedDescription = computed(() =>
  product.value?.description?.replace(/\n/g, '<br>') || ''
)

const tabs = [
  { id: 'description', label: 'Description' },
  { id: 'reviews', label: `Reviews (${product.value?.review_count || 0})` },
]

async function addToCart() {
  adding.value = true
  try {
    await cartStore.addItem(product.value.id, qty.value)
  } finally {
    adding.value = false
  }
}

function toggleWishlist() { inWishlist.value = !inWishlist.value }

onMounted(async () => {
  await productStore.fetchProduct(route.params.slug)
})
</script>

<style scoped>
.thumb-img {
  width: 72px; height: 72px; flex-shrink: 0;
  border-radius: 8px; overflow: hidden; cursor: pointer;
  border: 2px solid transparent; transition: border-color .2s;
}
.thumb-img.active { border-color: #f97316; }
.qty-control button { line-height: 1; padding: 8px 14px; }
.nav-tabs .nav-link { color: #64748b; border: none; border-bottom: 2px solid transparent; }
.nav-tabs .nav-link.active { color: #f97316; border-bottom-color: #f97316; background: none; }
</style>
