<template>
  <div>
    <!-- Hero Section -->
    <section class="hero-section position-relative overflow-hidden">
      <div class="hero-bg"></div>
      <div class="container position-relative py-5" style="min-height: 520px;">
        <div class="row align-items-center" style="min-height: 520px;">
          <div class="col-lg-6 animate-slide-up">
            <p class="text-orange-400 fw-semibold text-uppercase tracking-widest mb-3">New Season Arrivals</p>
            <h1 class="display-4 fw-bold text-white lh-tight mb-4">
              Discover Premium<br>
              <span class="text-orange-400">Products</span> Made<br>
              For You.
            </h1>
            <p class="text-gray-200 lead mb-5 pe-lg-5">
              Shop thousands of curated products with fast delivery and easy returns.
            </p>
            <div class="d-flex gap-3 flex-wrap">
              <router-link to="/products" class="btn-shop px-8 py-3">Shop Now →</router-link>
              <router-link to="/products?featured=true" class="btn-outline-shop text-white border-white hover:bg-white hover:text-dark px-6 py-3">
                View Featured
              </router-link>
            </div>

            <!-- Stats -->
            <div class="d-flex gap-4 mt-5 pt-2">
              <div class="text-center">
                <div class="fw-bold fs-4 text-white">50K+</div>
                <div class="text-gray-400 text-sm">Products</div>
              </div>
              <div class="text-center">
                <div class="fw-bold fs-4 text-white">10K+</div>
                <div class="text-gray-400 text-sm">Customers</div>
              </div>
              <div class="text-center">
                <div class="fw-bold fs-4 text-white">99%</div>
                <div class="text-gray-400 text-sm">Satisfaction</div>
              </div>
            </div>
          </div>
          <div class="col-lg-6 d-none d-lg-flex justify-content-center">
            <div class="hero-img-card">
              <div class="floating-badge top-badge">🔥 Best Seller</div>
              <div class="hero-placeholder">🛍️</div>
              <div class="floating-badge bottom-badge">⭐ 4.9 Rating</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Category Pills -->
    <section class="py-5 bg-light">
      <div class="container">
        <div class="d-flex gap-3 overflow-auto pb-2">
          <router-link
            v-for="cat in productStore.categories.slice(0, 8)"
            :key="cat.id"
            :to="`/category/${cat.slug}`"
            class="category-pill flex-shrink-0"
          >
            {{ cat.name }}
          </router-link>
        </div>
      </div>
    </section>

    <!-- Featured Products -->
    <section class="py-5">
      <div class="container">
        <div class="d-flex align-items-center justify-content-between mb-4">
          <div>
            <h2 class="fw-bold mb-1">Featured Products</h2>
            <p class="text-muted mb-0">Hand-picked items just for you</p>
          </div>
          <router-link to="/products?featured=true" class="btn-outline-shop">View All →</router-link>
        </div>

        <!-- Loading skeletons -->
        <div v-if="productStore.loading" class="row g-4">
          <div v-for="i in 4" :key="i" class="col-sm-6 col-lg-3">
            <div class="skeleton rounded-xl" style="height: 360px;"></div>
          </div>
        </div>

        <div v-else class="row g-4">
          <div
            v-for="product in productStore.featured.slice(0, 8)"
            :key="product.id"
            class="col-sm-6 col-lg-3"
          >
            <ProductCard :product="product" />
          </div>
        </div>
      </div>
    </section>

    <!-- Value Props Banner -->
    <section class="py-5" style="background: #0f172a;">
      <div class="container">
        <div class="row g-4">
          <div v-for="prop in valueProps" :key="prop.icon" class="col-sm-6 col-lg-3 text-center">
            <div class="mb-3" style="font-size: 2.5rem;">{{ prop.icon }}</div>
            <h6 class="text-white fw-bold mb-1">{{ prop.title }}</h6>
            <p class="text-gray-400 text-sm mb-0">{{ prop.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Newsletter -->
    <section class="py-5 bg-orange-50">
      <div class="container text-center">
        <h2 class="fw-bold mb-2">Stay in the loop</h2>
        <p class="text-muted mb-4">Get exclusive deals and new arrivals straight to your inbox.</p>
        <div class="d-flex gap-2 justify-content-center flex-wrap">
          <input type="email" class="input-shop" placeholder="Enter your email" style="max-width: 360px;" />
          <button class="btn-shop">Subscribe</button>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useProductStore } from '@/store/modules/products'
import ProductCard from '@/components/product/ProductCard.vue'

const productStore = useProductStore()

onMounted(async () => {
  await productStore.fetchFeatured()
})

const valueProps = [
  { icon: '🚚', title: 'Free Shipping', desc: 'On orders over $50' },
  { icon: '🔄', title: 'Easy Returns', desc: '30-day hassle-free returns' },
  { icon: '🔒', title: 'Secure Payment', desc: 'Your data is always safe' },
  { icon: '💬', title: '24/7 Support', desc: "We're always here for you" },
]
</script>

<style scoped>
.hero-section { background: #0f172a; }
.hero-bg {
  position: absolute; inset: 0;
  background: radial-gradient(ellipse at 60% 50%, rgba(249,115,22,.15) 0%, transparent 70%);
}

.hero-img-card {
  position: relative; width: 320px; height: 400px;
  background: linear-gradient(135deg, #1e293b, #334155);
  border-radius: 24px; display: flex; align-items: center; justify-content: center;
  box-shadow: 0 40px 80px rgba(0,0,0,.4);
}
.hero-placeholder { font-size: 8rem; }

.floating-badge {
  position: absolute; right: -20px;
  background: white; border-radius: 12px;
  padding: 8px 16px; font-weight: 600;
  font-size: .85rem; box-shadow: 0 4px 20px rgba(0,0,0,.15);
}
.top-badge { top: 40px; }
.bottom-badge { bottom: 60px; }

.category-pill {
  display: inline-flex; align-items: center;
  padding: 8px 20px; border-radius: 100px;
  background: white; border: 2px solid #e2e8f0;
  font-weight: 500; font-size: .875rem;
  text-decoration: none; color: #1e293b;
  transition: all .2s; white-space: nowrap;
}
.category-pill:hover {
  background: #f97316; border-color: #f97316; color: white;
}
</style>
