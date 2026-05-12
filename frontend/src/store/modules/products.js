import { defineStore } from 'pinia'
import api from '@/utils/api'

export const useProductStore = defineStore('products', {
  state: () => ({
    products: [],
    currentProduct: null,
    categories: [],
    featured: [],
    totalCount: 0,
    loading: false,
    filters: {
      search: '',
      category: '',
      min_price: '',
      max_price: '',
      ordering: '-created_at',
      in_stock: '',
      page: 1,
    },
  }),

  actions: {
    async fetchProducts(params = {}) {
      this.loading = true
      try {
        const query = { ...this.filters, ...params }
        // Remove empty values
        Object.keys(query).forEach(k => !query[k] && delete query[k])
        const { data } = await api.get('/products/', { params: query })
        this.products = data.results
        this.totalCount = data.count
      } finally {
        this.loading = false
      }
    },

    async fetchProduct(slug) {
      this.loading = true
      try {
        const { data } = await api.get(`/products/${slug}/`)
        this.currentProduct = data
        return data
      } finally {
        this.loading = false
      }
    },

    async fetchFeatured() {
      const { data } = await api.get('/products/featured/')
      this.featured = data
    },

    async fetchCategories() {
      const { data } = await api.get('/categories/')
      this.categories = data.results || data
    },

    setFilter(key, value) {
      this.filters[key] = value
      this.filters.page = 1
    },

    resetFilters() {
      this.filters = {
        search: '', category: '', min_price: '', max_price: '',
        ordering: '-created_at', in_stock: '', page: 1,
      }
    },
  },
})
