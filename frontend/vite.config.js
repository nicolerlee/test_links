import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

// 获取后端URL，支持环境变量配置
const getBackendUrl = () => {
  // // 优先使用环境变量
  // if (process.env.VITE_BACKEND_URL) {
  //   return process.env.VITE_BACKEND_URL
  // }
  // // 开发环境使用localhost
  // if (process.env.NODE_ENV === 'development') {
  //   return 'http://localhost:8000'
  // }
  // 生产环境使用Docker服务名
  return 'http://backend:8000'
}

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  server: {
    host: '0.0.0.0',  // 允许外部IP访问
    port: 3000,
    proxy: {
      '/api': {
        target: getBackendUrl(),
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
  },
}) 