import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  test: {
    environment: 'happy-dom',
    include: ['app/tests/**/*.spec.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['lcov', 'text', 'html'],
      reportsDirectory: './coverage',
      include: ['app/**/*.{ts,vue}'],
      exclude: [
        'app/tests/**',
        'app/**/*.spec.ts',
        '.nuxt/**',
        '.output/**',
        'node_modules/**'
      ]
    }
  }
})
