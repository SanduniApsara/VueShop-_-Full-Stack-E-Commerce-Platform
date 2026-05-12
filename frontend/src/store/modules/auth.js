import { defineStore } from 'pinia'
import api from '@/utils/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user') || 'null'),
    accessToken: localStorage.getItem('access_token') || null,
    refreshToken: localStorage.getItem('refresh_token') || null,
  }),

  getters: {
    isLoggedIn: state => !!state.accessToken && !!state.user,
  },

  actions: {
    async login(email, password) {
      const { data } = await api.post('/auth/login/', { email, password })
      this.accessToken = data.access
      this.refreshToken = data.refresh
      this.user = data.user
      localStorage.setItem('access_token', data.access)
      localStorage.setItem('refresh_token', data.refresh)
      localStorage.setItem('user', JSON.stringify(data.user))
    },

    async register(payload) {
      await api.post('/auth/register/', payload)
    },

    logout() {
      this.user = null
      this.accessToken = null
      this.refreshToken = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
    },

    async fetchProfile() {
      const { data } = await api.get('/auth/profile/')
      this.user = data
      localStorage.setItem('user', JSON.stringify(data))
    },

    async updateProfile(payload) {
      const { data } = await api.patch('/auth/profile/', payload)
      this.user = data
      localStorage.setItem('user', JSON.stringify(data))
    },
  },
})
