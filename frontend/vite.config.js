import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    proxy: {
      '/data': 'http://localhost:8000',
      '/stats': 'http://localhost:8000',
      '/insights': 'http://localhost:8000',
      '/search': 'http://localhost:8000',
      '/filter': 'http://localhost:8000',
      '/recommend': 'http://localhost:8000'
    }
  }
})