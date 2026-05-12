import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/store/modules/auth'

const routes = [
  {
    path: '/',
    component: () => import('@/views/HomeView.vue'),
    meta: { title: 'Home' }
  },
  {
    path: '/products',
    component: () => import('@/views/ProductsView.vue'),
    meta: { title: 'Shop' }
  },
  {
    path: '/products/:slug',
    component: () => import('@/views/ProductDetailView.vue'),
    meta: { title: 'Product' }
  },
  {
    path: '/category/:slug',
    component: () => import('@/views/CategoryView.vue'),
    meta: { title: 'Category' }
  },
  {
    path: '/cart',
    component: () => import('@/views/CartView.vue'),
    meta: { title: 'Cart' }
  },
  {
    path: '/checkout',
    component: () => import('@/views/CheckoutView.vue'),
    meta: { title: 'Checkout', requiresAuth: true }
  },
  {
    path: '/orders',
    component: () => import('@/views/OrdersView.vue'),
    meta: { title: 'My Orders', requiresAuth: true }
  },
  {
    path: '/orders/:id',
    component: () => import('@/views/OrderDetailView.vue'),
    meta: { title: 'Order Detail', requiresAuth: true }
  },
  {
    path: '/wishlist',
    component: () => import('@/views/WishlistView.vue'),
    meta: { title: 'Wishlist', requiresAuth: true }
  },
  {
    path: '/profile',
    component: () => import('@/views/ProfileView.vue'),
    meta: { title: 'Profile', requiresAuth: true }
  },
  {
    path: '/login',
    component: () => import('@/views/LoginView.vue'),
    meta: { title: 'Login', guestOnly: true }
  },
  {
    path: '/register',
    component: () => import('@/views/RegisterView.vue'),
    meta: { title: 'Register', guestOnly: true }
  },
  {
    path: '/:pathMatch(.*)*',
    component: () => import('@/views/NotFoundView.vue'),
    meta: { title: '404 - Not Found' }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, saved) {
    if (saved) return saved
    return { top: 0, behavior: 'smooth' }
  }
})

router.beforeEach((to, from, next) => {
  document.title = `${to.meta.title} | VueShop`
  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    next({ path: '/login', query: { redirect: to.fullPath } })
  } else if (to.meta.guestOnly && auth.isLoggedIn) {
    next('/')
  } else {
    next()
  }
})

export default router
