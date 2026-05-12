<template>
  <nav class="navbar navbar-expand-lg sticky-top bg-white border-bottom shadow-sm">
    <div class="container">
      <!-- Brand -->
      <router-link class="navbar-brand d-flex align-items-center gap-2" to="/">
        <span class="brand-logo">🛍️</span>
        <span class="brand-name">Vue<span class="text-orange-500">Shop</span></span>
      </router-link>

      <!-- Mobile right side: cart + toggler -->
      <div class="d-flex align-items-center gap-2 d-lg-none">
        <button @click="cartStore.toggleDrawer" class="btn position-relative p-2 border-0 bg-transparent">
          🛒
          <span v-if="cartStore.totalItems > 0" class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-orange-500" style="font-size:.65rem">
            {{ cartStore.totalItems }}
          </span>
        </button>
        <button class="navbar-toggler border-0 p-1" type="button" @click="menuOpen = !menuOpen" aria-label="Toggle navigation">
          <span v-if="!menuOpen" style="font-size:1.5rem;line-height:1;">☰</span>
          <span v-else style="font-size:1.5rem;line-height:1;">✕</span>
        </button>
      </div>

      <!-- Nav links -->
      <div :class="['w-100', menuOpen ? 'mobile-menu-open' : 'd-none d-lg-flex align-items-center']">
        <!-- Search bar -->
        <div class="mx-auto my-3 my-lg-0" style="width:100%;max-width:400px;">
          <div class="position-relative">
            <input v-model="searchQuery" @keyup.enter="handleSearch" type="search" class="form-control rounded-pill ps-4 pe-5" placeholder="Search products..." />
            <button @click="handleSearch" class="btn position-absolute end-0 top-50 translate-middle-y pe-3 border-0 bg-transparent">🔍</button>
          </div>
        </div>

        <ul class="navbar-nav ms-auto align-items-lg-center gap-1 mt-2 mt-lg-0 list-unstyled d-flex flex-column flex-lg-row">
          <li class="nav-item">
            <router-link class="nav-link fw-medium" to="/products" @click="menuOpen=false">Shop</router-link>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle fw-medium" href="#" data-bs-toggle="dropdown">Categories</a>
            <ul class="dropdown-menu shadow border-0 rounded-3">
              <li v-for="cat in productStore.categories" :key="cat.id">
                <router-link class="dropdown-item py-2" :to="`/category/${cat.slug}`" @click="menuOpen=false">
                  {{ cat.name }}
                </router-link>
              </li>
            </ul>
          </li>
          <li v-if="authStore.isLoggedIn" class="nav-item">
            <router-link class="nav-link" to="/wishlist" @click="menuOpen=false">❤️ Wishlist</router-link>
          </li>
          <li class="nav-item d-none d-lg-block">
            <button @click="cartStore.toggleDrawer" class="btn position-relative p-2 border-0 bg-transparent">
              🛒
              <span v-if="cartStore.totalItems > 0" class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-orange-500" style="font-size:.65rem">{{ cartStore.totalItems }}</span>
            </button>
          </li>
          <li v-if="authStore.isLoggedIn" class="nav-item dropdown">
            <a class="nav-link dropdown-toggle d-flex align-items-center gap-2" href="#" data-bs-toggle="dropdown">
              <span class="avatar-circle">{{ userInitial }}</span>
            </a>
            <ul class="dropdown-menu dropdown-menu-end shadow border-0 rounded-3">
              <li><h6 class="dropdown-header">{{ authStore.user?.email }}</h6></li>
              <li><router-link class="dropdown-item" to="/profile" @click="menuOpen=false">👤 Profile</router-link></li>
              <li><router-link class="dropdown-item" to="/orders" @click="menuOpen=false">📦 My Orders</router-link></li>
              <li><hr class="dropdown-divider"></li>
              <li><button class="dropdown-item text-danger" @click="handleLogout">🚪 Logout</button></li>
            </ul>
          </li>
          <li v-else class="nav-item d-flex gap-2 mt-2 mt-lg-0">
            <router-link to="/login" @click="menuOpen=false" class="btn btn-outline-secondary btn-sm rounded-pill px-3">Login</router-link>
            <router-link to="/register" @click="menuOpen=false" class="btn btn-sm rounded-pill px-3 text-white" style="background:#f97316">Register</router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/modules/auth'
import { useCartStore } from '@/store/modules/cart'
import { useProductStore } from '@/store/modules/products'

const router = useRouter()
const authStore = useAuthStore()
const cartStore = useCartStore()
const productStore = useProductStore()

const searchQuery = ref('')
const menuOpen = ref(false)

const userInitial = computed(() =>
  (authStore.user?.first_name?.[0] || authStore.user?.email?.[0] || '?').toUpperCase()
)

function handleSearch() {
  if (searchQuery.value.trim()) {
    router.push({ path: '/products', query: { search: searchQuery.value } })
    searchQuery.value = ''
    menuOpen.value = false
  }
}

function handleLogout() {
  authStore.logout()
  menuOpen.value = false
  router.push('/')
}
</script>

<style scoped>
.brand-name { font-family: 'Playfair Display', serif; font-size: 1.4rem; font-weight: 700; }
.brand-logo { font-size: 1.5rem; }
.avatar-circle {
  width: 34px; height: 34px;
  background: #f97316; color: white;
  border-radius: 50%; display: flex;
  align-items: center; justify-content: center;
  font-weight: 700; font-size: .85rem;
}
.mobile-menu-open {
  display: flex !important;
  flex-direction: column;
  width: 100%;
  padding: 12px 0 8px;
  border-top: 1px solid #e2e8f0;
  animation: slideDown 0.2s ease-out;
}
@keyframes slideDown {
  from { opacity: 0; transform: translateY(-8px); }
  to   { opacity: 1; transform: translateY(0); }
}
</style>