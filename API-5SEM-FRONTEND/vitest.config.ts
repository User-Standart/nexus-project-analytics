import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      vue: resolve('./node_modules/vue/dist/vue.esm-bundler.js')
    }
  },
  test: {
    environment: 'happy-dom',
    globals: true
  }
})
