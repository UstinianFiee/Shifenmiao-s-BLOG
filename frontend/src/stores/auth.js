import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const username = ref(localStorage.getItem('username') || '')

  async function login(user, pass) {
    const res = await api.post('/auth/login', { username: user, password: pass })
    token.value = res.data.token
    username.value = res.data.username
    localStorage.setItem('token', token.value)
    localStorage.setItem('username', username.value)
  }

  function logout() {
    token.value = ''
    username.value = ''
    localStorage.removeItem('token')
    localStorage.removeItem('username')
  }

  return { token, username, login, logout }
})
