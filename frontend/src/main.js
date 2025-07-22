import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import zhCn from 'element-plus/es/locale/lang/zh-cn'

// 引入vConsole配置
import { setupVConsole } from './utils/vconsole'

import App from './App.vue'
import router from './router'

// 初始化vConsole
setupVConsole()

// 防止移动端双击放大
const preventDoubleTapZoom = () => {
  let lastTouchEnd = 0
  document.addEventListener('touchend', (event) => {
    const now = (new Date()).getTime()
    if (now - lastTouchEnd <= 300) {
      event.preventDefault()
    }
    lastTouchEnd = now
  }, false)
  
  // 禁用双击选择文本
  document.addEventListener('dblclick', (event) => {
    event.preventDefault()
  }, false)
  
  // 禁用双击缩放
  document.addEventListener('touchstart', (event) => {
    if (event.touches.length > 1) {
      event.preventDefault()
    }
  }, { passive: false })
  
  let initialTouchDistance = 0
  document.addEventListener('touchmove', (event) => {
    if (event.touches.length === 2) {
      const touch1 = event.touches[0]
      const touch2 = event.touches[1]
      const distance = Math.sqrt(
        Math.pow(touch2.clientX - touch1.clientX, 2) +
        Math.pow(touch2.clientY - touch1.clientY, 2)
      )
      
      if (initialTouchDistance === 0) {
        initialTouchDistance = distance
      } else {
        const scale = distance / initialTouchDistance
        if (scale > 1.1 || scale < 0.9) {
          event.preventDefault()
        }
      }
    }
  }, { passive: false })
  
  document.addEventListener('touchend', () => {
    initialTouchDistance = 0
  }, false)
}

// 在移动端启用防双击放大
if (typeof window !== 'undefined' && typeof navigator !== 'undefined') {
  const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
  if (isMobile) {
    preventDoubleTapZoom()
  }
}

const app = createApp(App)

// 注册所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(createPinia())
app.use(router)
app.use(ElementPlus, {
  locale: zhCn,
})

app.mount('#app') 