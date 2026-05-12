<template>
  <div class="container py-5">
    <div class="row g-4">
      <!-- Sidebar Filters -->
      <div class="col-lg-3">
        <div class="card border-0 shadow-sm rounded-3 p-4 sticky-top" style="top: 80px;">
          <h6 class="fw-bold mb-3">Filters</h6>

          <!-- Categories -->
          <div class="mb-4">
            <p class="text-xs fw-bold text-uppercase text-muted tracking-wide mb-2">Category</p>
            <div class="d-flex flex-column gap-1">
              <button
                @click="setCategory('')"
                :class="['filter-btn', !activeCategory && 'active']"
              >All Products</button>
              <button
                v-for="cat in productStore.categories"
                :key="cat.id"
                @click="setCategory(cat.slug)"
                :class="['filter-btn', activeCategory === cat.slug && 'active']"
              >
                {{ cat.name }}
                <span class="ms-auto text-muted small">{{ cat.product_count }}</span>
              </button>
            </div>
          </div>

          <!-- Price range -->
          <div class="mb-4">
            <p class="text-xs fw-bold text-uppercase text-muted tracking-wide mb-2">Price Range</p>
            <div class="d-flex gap-2">
              <input v-model="minPrice" type="number" class="input-shop" placeholder="Min $" @change="applyFilters" />
              <input v-model="maxPrice" type="number" class="input-shop" placeholder="Max $" @change="applyFilters" />
            </div>
          </div>

          <!-- In Stock toggle -->
          <div class="mb-4">
            <div class="form-check form-switch">
              <input v-model="inStockOnly" class="form-check-input" type="checkbox" id="inStock" @change="applyFilters">
              <label class="form-check-label fw-medium" for="inStock">In Stock Only</label>
            </div>
          </div>

          <button @click="resetFilters" class="btn btn-outline-secondary btn-sm w-100 rounded-pill">
            Clear Filters
          </button>
        </div>
      </div>

      <!-- Products Grid -->
      <div class="col-lg-9">
        <!-- Toolbar -->
        <div class="d-flex align-items-center justify-content-between flex-wrap gap-3 mb-4">
          <div>
            <h4 class="fw-bold mb-0">{{ pageTitle }}</h4>
            <p class="text-muted small mb-0">{{ productStore.totalCount }} products found</p>
          </div>
          <div class="d-flex align-items-center gap-2">
            <label class="text-sm text-muted">Sort:</label>
            <select v-model="ordering" @change="applyFilters" class="form-select form-select-sm rounded-pill" style="width: auto;">
              <option value="-created_at">Newest</option>
              <option value="price">Price: Low to High</option>
              <option value="-price">Price: High to Low</option>
              <option value="name">Name A–Z</option>
            </select>
          </div>
        </div>

        <!-- Skeleton Loading -->
        <div v-if="productStore.loading" class="row g-4">
          <div v-for="i in 9" :key="i" class="col-sm-6 col-xl-4">
            <div class="skeleton rounded-3" style="height: 360px;"></div>
          </div>
        </div>

        <!-- Products -->
        <div v-else-if="productStore.products.length > 0" class="row g-4">
          <div
            v-for="product in productStore.products"
            :key="product.id"
            class="col-sm-6 col-xl-4"
          >
            <ProductCard :product="product" />
          </div>
        </div>

        <!-- Empty state -->
        <div v-else class="text-center py-5">
          <div style="font-size: 4rem">😔</div>
          <h5 class="mt-3">No products found</h5>
          <p class="text-muted">Try adjusting your filters or search term.</p>
          <button @click="resetFilters" class="btn-shop">Clear Filters</button>
        </div>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="d-flex justify-content-center mt-5">
          <nav>
            <ul class="pagination">
              <li :class="['page-item', currentPage <= 1 && 'disabled']">
                <button class="page-link rounded-start-pill" @click="goToPage(currentPage - 1)">←</button>
              </li>
              <li v-for="page in totalPages" :key="page" :class="['page-item', page === currentPage && 'active']">
                <button class="page-link" @click="goToPage(page)">{{ page }}</button>
              </li>
              <li :class="['page-item', currentPage >= totalPages && 'disabled']">
                <button class="page-link rounded-end-pill" @click="goToPage(currentPage + 1)">→</button>
              </li>
            </ul>
          </nav>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useProductStore } from '@/store/modules/products'
import ProductCard from '@/components/product/ProductCard.vue'

const route = useRoute()
const router = useRouter()
const productStore = useProductStore()

const activeCategory = ref('')
const minPrice = ref('')
const maxPrice = ref('')
const inStockOnly = ref(false)
const ordering = ref('-created_at')
const currentPage = ref(1)

const totalPages = computed(() => Math.ceil(productStore.totalCount / 12))

const pageTitle = computed(() => {
  if (route.query.search) return `Results for "${route.query.search}"`
  if (activeCategory.value) {
    const cat = productStore.categories.find(c => c.slug === activeCategory.value)
    return cat?.name || 'Products'
  }
  return 'All Products'
})

async function applyFilters() {
  currentPage.value = 1
  await productStore.fetchProducts({
    category: activeCategory.value,
    min_price: minPrice.value,
    max_price: maxPrice.value,
    in_stock: inStockOnly.value || '',
    ordering: ordering.value,
    search: route.query.search || '',
    page: 1,
  })
}

async function setCategory(slug) {
  activeCategory.value = slug
  await applyFilters()
}

async function goToPage(page) {
  if (page < 1 || page > totalPages.value) return
  currentPage.value = page
  await productStore.fetchProducts({ page })
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function resetFilters() {
  activeCategory.value = ''
  minPrice.value = ''
  maxPrice.value = ''
  inStockOnly.value = false
  ordering.value = '-created_at'
  router.replace({ query: {} })
  productStore.fetchProducts()
}

onMounted(() => {
  if (route.query.search) {
    productStore.fetchProducts({ search: route.query.search })
  } else {
    productStore.fetchProducts()
  }
})

watch(() => route.query.search, val => {
  if (val) productStore.fetchProducts({ search: val })
})
</script>

<style scoped>
.filter-btn {
  display: flex; align-items: center;
  width: 100%; padding: 7px 12px;
  border: none; background: transparent;
  border-radius: 8px; text-align: left;
  font-size: .875rem; cursor: pointer;
  transition: all .2s; color: #1e293b;
}
.filter-btn:hover { background: #fff7ed; color: #f97316; }
.filter-btn.active { background: #fff7ed; color: #f97316; font-weight: 600; }
.page-item.active .page-link { background: #f97316; border-color: #f97316; }
</style>
