import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  base: '/assets/syncedoffice/js/cms/',
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  experimental: {
    renderBuiltUrl(filename, { hostType }) {
      return '/assets/syncedoffice/js/cms/' + filename
    }
  },
  build: {
    outDir: '../../public/js/cms',
    emptyOutDir: true,
    manifest: true,
    rollupOptions: {
      output: {
        entryFileNames: 'cms-app.js',
        chunkFileNames: 'chunks/[name]-[hash].js',
        assetFileNames: 'assets/[name]-[hash].[ext]',
      },
    },
  },
  server: {
    port: 8081,
    proxy: {
      '/api': {
        target: 'http://localhost:8002',
        changeOrigin: true,
      },
    },
  },
})
