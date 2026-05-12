import { defineStore } from 'pinia'
import api from '@/utils/api'
import { useAuthStore } from './auth'

export const useCartStore = defineStore('cart', {
  state: () => ({
    cart: null,
    loading: false,
    drawerOpen: false,
  }),

  getters: {
    totalItems: state => state.cart?.total_items || 0,
    subtotal: state => state.cart?.subtotal || 0,
    items: state => state.cart?.items || [],
  },

  actions: {
    async fetchCart() {
      const auth = useAuthStore()
      if (!auth.isLoggedIn) return
      this.loading = true
      try {
        const { data } = await api.get('/cart/')
        this.cart = data
      } finally {
        this.loading = false
      }
    },

    async addItem(productId, quantity = 1) {
      const auth = useAuthStore()
      if (!auth.isLoggedIn) {
        window.location.href = '/login'
        return
      }
      const { data } = await api.post('/cart/add/', { product_id: productId, quantity })
      this.cart = data
      this.drawerOpen = true
    },

    async updateItem(itemId, quantity) {
      const { data } = await api.put(`/cart/update/${itemId}/`, { quantity })
      this.cart = data
    },

    async removeItem(itemId) {
      const { data } = await api.delete(`/cart/update/${itemId}/`)
      this.cart = data
    },

    toggleDrawer() { this.drawerOpen = !this.drawerOpen },
    openDrawer()   { this.drawerOpen = true },
    closeDrawer()  { this.drawerOpen = false },
  },
})
