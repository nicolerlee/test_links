import VConsole from 'vconsole'

// vConsole配置
export const initVConsole = () => {
  // 安全检查navigator是否存在
  if (typeof navigator === 'undefined') {
    console.warn('⚠️ navigator未定义，跳过vConsole初始化')
    return null
  }
  
  // 检测是否为移动设备
  const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
  
  // 检测是否为开发环境
  const isDev = import.meta.env.DEV
  
  // 检测是否为本地开发服务器
  const isLocalDev = window.location.hostname === 'localhost' || 
                     window.location.hostname === '127.0.0.1' ||
                     window.location.hostname.includes('192.168.')
  
  // 在开发环境、移动端或本地开发时启用vConsole
  if (isDev || isMobile || isLocalDev) {
    const vConsole = new VConsole({
      theme: 'dark', // 主题：dark 或 light
      maxLogNumber: 1000, // 最大日志数量
      defaultPlugins: ['system', 'network', 'element', 'storage'], // 默认插件
      onReady: function() {
        console.log('🎯 vConsole 已加载完成')
        console.log('📱 移动端调试工具已启用')
      },
      onClearLog: function() {
        console.log('🧹 vConsole 日志已清空')
      }
    })
    
    // 添加一些有用的调试信息
    console.log('🚀 应用启动中...')
    console.log('🔧 开发环境:', isDev)
    console.log('📱 移动设备:', isMobile)
    console.log('🏠 本地开发:', isLocalDev)
    console.log('🌐 当前地址:', window.location.href)
    console.log('📱 屏幕尺寸:', `${window.innerWidth}x${window.innerHeight}`)
    console.log('🌐 用户代理:', navigator.userAgent)
    
    return vConsole
  }
  
  return null
}

// 导出vConsole实例（如果需要在其他地方使用）
export let vConsoleInstance = null

// 初始化函数
export const setupVConsole = () => {
  vConsoleInstance = initVConsole()
} 