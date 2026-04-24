import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 8001,
    proxy: {
      '/api': 'http://localhost:5001',
      '/uploads': 'http://localhost:5001',
    }
  }
})
