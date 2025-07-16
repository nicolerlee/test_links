<template>
  <div class="view-page">
    <div class="page-header">
      <div class="header-left">
        <el-button @click="goBack" :icon="ArrowLeft">返回</el-button>
        <h2>{{ miniprogram?.name || '查看小程序' }}</h2>
      </div>
      <div class="header-actions">
        <el-button @click="editMiniprogram" type="info">
          <el-icon><Edit /></el-icon>
          编辑
        </el-button>
      </div>
    </div>

    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="8" animated />
    </div>

    <div v-else-if="miniprogram" class="content-area">
      <!-- 链接展示 -->
      <el-card v-if="miniprogram.links?.length" class="section-card" shadow="never">
        <template #header>
          <div class="card-header">
            <h3>链接管理</h3>
            <el-tag>{{ activeLinks.length }} / {{ miniprogram.links.length }} 个链接</el-tag>
          </div>
        </template>

        <div class="links-section">
          <!-- 环境切换标签 -->
          <div class="environment-tabs">
            <el-tabs v-model="activeEnvironment" type="card">
              <el-tab-pane label="测试环境" name="test"></el-tab-pane>
              <el-tab-pane label="正式环境" name="prod"></el-tab-pane>
            </el-tabs>
          </div>

          <!-- 链接统计 -->
          <div class="links-summary" v-if="miniprogram.links.length > 0">
            <el-row :gutter="20">
              <el-col :span="8">
                <el-statistic title="总链接数" :value="miniprogram.links.length">
                  <template #suffix>
                    <el-icon><Connection /></el-icon>
                  </template>
                </el-statistic>
              </el-col>
              <el-col :span="8">
                <el-statistic title="启用链接" :value="activeLinks.length" :value-style="{ color: '#67c23a' }">
                  <template #suffix>
                    <el-icon><Check /></el-icon>
                  </template>
                </el-statistic>
              </el-col>
              <el-col :span="8">
                <el-statistic title="禁用链接" :value="inactiveLinks.length" :value-style="{ color: '#f56c6c' }">
                  <template #suffix>
                    <el-icon><Close /></el-icon>
                  </template>
                </el-statistic>
              </el-col>
            </el-row>
          </div>

          <!-- 链接列表 -->
          <div class="links-list">
            <div
              v-for="(link, index) in sortedLinks"
              :key="link.id"
              class="link-item"
              :class="{ disabled: !isLinkEffectivelyActive(link) }"
            >
              <div class="link-row">
                <div class="link-info">
                  <el-tag size="small" type="info">{{ index + 1 }}</el-tag>
                  <span class="title-text">{{ link.title }}</span>
                  <el-tag 
                    :type="isLinkEffectivelyActive(link) ? 'success' : 'danger'" 
                    size="small"
                  >
                    {{ isLinkEffectivelyActive(link) ? '启用' : '禁用' }}
                  </el-tag>
                </div>
                <div class="link-url-inline">
                  <el-input
                    :value="getFullUrl(link)"
                    readonly
                    size="small"
                    class="url-input"
                  />
                </div>
                <div class="link-actions">
                  <el-button
                    v-if="isLinkEffectivelyActive(link)"
                    @click="copyLink(getFullUrl(link))"
                    type="primary"
                    size="small"
                  >
                    <el-icon><CopyDocument /></el-icon>
                    复制
                  </el-button>
                  <div class="qr-code-wrapper" style="position: relative;">
                    <el-button
                      v-if="isLinkEffectivelyActive(link)"
                      @mouseenter="showQrCode(link.id, getFullUrl(link))"
                      @mouseleave="hideQrCode(link.id)"
                      type="info"
                      size="small"
                    >
                      <el-icon><Share /></el-icon>
                      二维码
                    </el-button>
                    <!-- 二维码悬浮层 -->
                    <div 
                      v-if="qrCodeVisibility[link.id]" 
                      class="qr-code-tooltip"
                      @mouseenter="showQrCode(link.id, getFullUrl(link))"
                      @mouseleave="hideQrCode(link.id)"
                    >
                      <div class="qr-code-content">
                        <div class="qr-code-image">
                          <canvas :ref="(el) => qrCodeRefs[link.id] = el" class="qr-canvas"></canvas>
                        </div>
                        <div class="qr-code-info">
                          <p class="qr-code-text">扫描二维码访问链接</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </el-card>

      <!-- 空状态 -->
      <div v-if="!miniprogram.links?.length" class="empty-state">
        <el-empty description="暂无链接数据">
          <el-button @click="editMiniprogram" type="primary">
            添加链接
          </el-button>
        </el-empty>
      </div>
    </div>

    <div v-else class="error-container">
      <el-result icon="warning" title="小程序不存在" sub-title="请检查小程序ID是否正确">
        <template #extra>
          <el-button @click="goBack">返回</el-button>
        </template>
      </el-result>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  ArrowLeft,
  Edit,
  Link,
  Connection,
  TopRight,
  Check,
  Close,
  CopyDocument,
  Share
} from '@element-plus/icons-vue'
import { miniprogramAPI } from '@/api'
import QRCode from 'qrcode'

const router = useRouter()

// Props
const props = defineProps({
  id: {
    type: String,
    required: true
  }
})

// 响应式数据
const loading = ref(true)
const miniprogram = ref(null)

// 环境切换
const activeEnvironment = ref('test')

// 二维码相关状态
const qrCodeVisibility = ref({})
const qrCodeRefs = ref({})
const qrCodeTimeouts = ref({})

// 计算属性
const activeLinks = computed(() => {
  if (miniprogram.value?.status !== 1) {
    return [];
  }
  return miniprogram.value?.links?.filter(link => link.status === 1) || []
})

const inactiveLinks = computed(() => {
  if (miniprogram.value?.status !== 1) {
    return miniprogram.value?.links || [];
  }
  return miniprogram.value?.links?.filter(link => link.status !== 1) || []
})

const sortedLinks = computed(() => {
  return miniprogram.value?.links?.slice().sort((a, b) => a.sort_order - b.sort_order) || []
})

const isLinkEffectivelyActive = (link) => {
  if (!link || !miniprogram.value) return false;
  return miniprogram.value.status === 1 && link.status === 1;
}

// 方法
const loadData = async () => {
  try {
    loading.value = true
    const data = await miniprogramAPI.getMiniprogram(props.id)
    miniprogram.value = data
  } catch (error) {
    ElMessage.error('加载数据失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

// 刷新数据
const refreshData = async () => {
  await loadData()
  ElMessage.success('数据已刷新')
}

// 页面获得焦点时刷新数据
const handleVisibilityChange = () => {
  if (!document.hidden) {
    loadData()
  }
}

// 生命周期
onMounted(() => {
  loadData()
  // 监听页面可见性变化
  document.addEventListener('visibilitychange', handleVisibilityChange)
})

// 清理定时器和事件监听
onBeforeUnmount(() => {
  // 清理所有二维码定时器
  Object.values(qrCodeTimeouts.value).forEach(timeout => {
    clearTimeout(timeout)
  })
  qrCodeTimeouts.value = {}
  
  // 移除事件监听
  document.removeEventListener('visibilitychange', handleVisibilityChange)
})


const formatDateTime = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

const copyLink = async (url) => {
  try {
    await navigator.clipboard.writeText(url)
    ElMessage.success('链接已复制到剪贴板')
  } catch (error) {
    // 降级方案
    const textArea = document.createElement('textarea')
    textArea.value = url
    document.body.appendChild(textArea)
    textArea.select()
    try {
      document.execCommand('copy')
      ElMessage.success('链接已复制到剪贴板')
    } catch (err) {
      ElMessage.error('复制失败，请手动复制')
    }
    document.body.removeChild(textArea)
  }
}

const editMiniprogram = () => {
  router.push(`/edit/${props.id}`)
}

const goBack = () => {
  router.back()
}

// 获取完整URL
const getFullUrl = (link) => {
  if (!link) return ''
  
  // 根据链接的domain_type查找对应的域名配置
  let domainConfig = null
  
  if (link.domain_type) {
    // 如果链接有domain_type，查找对应的域名配置
    domainConfig = miniprogram.value?.domain_configs?.find(config => config.domain_type === link.domain_type)
  }
  
  // 如果没有找到对应的域名配置，使用默认域名配置
  if (!domainConfig) {
    domainConfig = miniprogram.value?.domain_configs?.find(config => config.domain_type === 'default')
  }
  
  if (!domainConfig) {
    return link.url
  }
  
  // 根据环境选择域名
  const domain = activeEnvironment.value === 'test' ? domainConfig.test_domain : domainConfig.prod_domain
  if (!domain) {
    return link.url
  }
  
  // 构建完整URL
  let fullUrl = domain
  
  // 添加路径层级
  if (domainConfig.first_level) {
    fullUrl += `/${domainConfig.first_level}`
  }
  if (domainConfig.second_level) {
    fullUrl += `/${domainConfig.second_level}`
  }
  if (domainConfig.third_level) {
    fullUrl += `/${domainConfig.third_level}`
  }
  
  // 添加链接路径
  const linkPath = link.url.startsWith('/') ? link.url : `/${link.url}`
  fullUrl += linkPath
  
  return fullUrl
}

// 二维码相关方法
const showQrCode = async (linkId, url) => {
  // 清除隐藏的延迟器
  if (qrCodeTimeouts.value[linkId]) {
    clearTimeout(qrCodeTimeouts.value[linkId])
    delete qrCodeTimeouts.value[linkId]
  }
  
  // 显示二维码
  qrCodeVisibility.value[linkId] = true
  
  // 等待DOM更新后生成二维码
  await nextTick()
  setTimeout(() => {
    generateQrCode(linkId, url)
  }, 50) // 短暂延迟确保DOM完全渲染
}

const hideQrCode = (linkId) => {
  // 设置延迟隐藏二维码，避免鼠标快速移动时闪烁
  qrCodeTimeouts.value[linkId] = setTimeout(() => {
    qrCodeVisibility.value[linkId] = false
    delete qrCodeTimeouts.value[linkId]
  }, 300) // 300毫秒延迟，给用户更多时间
}

const generateQrCode = async (linkId, url) => {
  try {
    const canvas = qrCodeRefs.value[linkId]
    console.log('Canvas element:', canvas, 'URL:', url)
    
    if (canvas) {
      // 设置canvas尺寸
      canvas.width = 160
      canvas.height = 160
      
      // 清理canvas
      const ctx = canvas.getContext('2d')
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      
      // 生成二维码
      await QRCode.toCanvas(canvas, url, {
        width: 160,
        height: 160,
        margin: 2,
        color: {
          dark: '#000000',
          light: '#ffffff'
        },
        errorCorrectionLevel: 'M'
      })
      
      console.log('二维码生成成功')
    } else {
      console.error('Canvas element not found')
    }
  } catch (error) {
    console.error('生成二维码失败:', error)
    ElMessage.error('生成二维码失败: ' + error.message)
  }
}
</script>

<style scoped>
.view-page {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ebeef5;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 15px;
}

.header-left h2 {
  margin: 0;
  color: #303133;
  font-weight: 600;
}

/* 页面标题样式 */
.page-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding: 12px 0;
  border-bottom: 1px solid #e4e7ed;
}

.page-title h2 {
  margin: 0;
  color: #303133;
  font-weight: 600;
  font-size: 20px;
}

.title-tags {
  display: flex;
  gap: 10px;
}

.loading-container,
.error-container {
  background: white;
  border-radius: 6px;
  padding: 30px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.08);
}

.content-area {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.section-card {
  border: 1px solid #ebeef5;
  min-height: 500px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  color: #303133;
  font-weight: 600;
  font-size: 16px;
}

.header-tags {
  display: flex;
  gap: 10px;
}

.basic-info {
  padding: 10px 0;
}

.info-item {
  margin-bottom: 20px;
}

.info-item label {
  display: inline-block;
  width: 100px;
  color: #606266;
  font-weight: 500;
  margin-bottom: 5px;
}

.info-item span {
  color: #303133;
}

.stats {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
  margin-top: 5px;
}

.domain-configs {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.domain-config-item {
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  overflow: hidden;
}

.config-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.config-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.domain-info {
  padding: 10px 0;
}

.domain-item {
  margin-bottom: 15px;
}

.domain-item label {
  display: block;
  color: #606266;
  font-weight: 500;
  margin-bottom: 5px;
}

.domain-url {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
}

.path-info {
  margin-top: 15px;
}

.path-info label {
  display: block;
  color: #606266;
  font-weight: 500;
  margin-bottom: 5px;
}

.path-breadcrumb {
  background: #f5f7fa;
  padding: 8px 12px;
  border-radius: 4px;
}

.links-section {
  padding: 20px 0;
}

.environment-tabs {
  margin-bottom: 15px;
  padding: 0 16px;
}

.environment-tabs :deep(.el-tabs__header) {
  margin-bottom: 0;
}

.environment-tabs :deep(.el-tabs__nav) {
  border: 1px solid #e4e7ed;
  border-radius: 6px;
  overflow: hidden;
}

.environment-tabs :deep(.el-tabs__item) {
  border: none;
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 500;
}

.environment-tabs :deep(.el-tabs__item.is-active) {
  background: #409eff;
  color: white;
}

.environment-tabs :deep(.el-tabs__item:hover) {
  background: #ecf5ff;
  color: #409eff;
}

.environment-tabs :deep(.el-tabs__item.is-active:hover) {
  background: #409eff;
  color: white;
}

.links-summary {
  margin-bottom: 15px;
  padding: 12px 16px;
  background: #fafafa;
  border-radius: 6px;
}

.links-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.link-item {
  border: 1px solid #ebeef5;
  border-radius: 6px;
  padding: 8px 12px;
  transition: all 0.3s;
  min-height: 40px;
}

.link-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.link-item.disabled {
  opacity: 0.6;
  background: #f5f7fa;
}

.link-row {
  display: flex;
  align-items: center;
  gap: 15px;
  width: 100%;
  min-height: 40px;
}

.link-info {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
  min-width: 200px;
}

.title-text {
  font-weight: 500;
  color: #303133;
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.link-url-inline {
  flex: 1;
  min-width: 0;
}

.url-input {
  width: 100%;
}

.link-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.qr-code-wrapper {
  position: relative;
}

.empty-state {
  padding: 30px;
  text-align: center;
  background: white;
  border-radius: 6px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.08);
}

:deep(.el-card__header) {
  background-color: #fafafa;
  border-bottom: 1px solid #ebeef5;
  padding: 12px 16px;
}

:deep(.el-card__body) {
  padding: 16px;
  min-height: 400px;
}

:deep(.el-statistic__content) {
  display: flex;
  align-items: center;
  justify-content: center;
}

:deep(.el-statistic) {
  --el-statistic-content-font-size: 20px;
}

:deep(.el-statistic__head) {
  font-size: 13px;
  margin-bottom: 4px;
}

:deep(.el-textarea__inner) {
  background: #f5f7fa;
  border: 1px solid #dcdfe6;
}

/* 二维码相关样式 */
.qr-code-tooltip {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 8px;
  z-index: 1000;
  background: white;
  border: 1px solid #e4e7ed;
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  padding: 4px;
  width: fit-content;
}

.qr-code-tooltip::before {
  content: '';
  position: absolute;
  top: -6px;
  right: 20px;
  width: 0;
  height: 0;
  border-left: 6px solid transparent;
  border-right: 6px solid transparent;
  border-bottom: 6px solid white;
}

.qr-code-tooltip::after {
  content: '';
  position: absolute;
  top: -7px;
  right: 20px;
  width: 0;
  height: 0;
  border-left: 7px solid transparent;
  border-right: 7px solid transparent;
  border-bottom: 7px solid #e4e7ed;
}

.qr-code-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.qr-code-image {
  flex-shrink: 0;
}

.qr-canvas {
  width: 160px;
  height: 160px;
  display: block;
}

.qr-code-info {
  text-align: center;
  padding: 2px 0;
}

.qr-code-text {
  margin: 0;
  font-size: 12px;
  color: #606266;
}

/* 按钮层级样式 */
:deep(.el-button--info) {
  background: white;
  border-color: #d1d5db;
  color: #374151;
}

:deep(.el-button--info:hover) {
  background: #f9fafb;
  border-color: #9ca3af;
  color: #111827;
}

:deep(.el-button--info:active) {
  background: #f3f4f6;
  border-color: #6b7280;
  color: #111827;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .link-row {
    flex-direction: column;
    gap: 10px;
    align-items: stretch;
  }
  
  .link-info {
    min-width: auto;
  }
  
  .link-actions {
    justify-content: flex-end;
  }
  
  .qr-code-tooltip {
    top: 50%;
    right: 100%;
    bottom: auto;
    left: auto;
    transform: translateY(-50%);
    margin: 0 8px 0 0;
  }
  
  .qr-code-tooltip::before {
    top: 50%;
    right: -6px;
    left: auto;
    transform: translateY(-50%);
    border: 6px solid transparent;
    border-left-color: white;
    border-right: none;
  }
  
  .qr-code-tooltip::after {
    top: 50%;
    right: -7px;
    left: auto;
    transform: translateY(-50%);
    border: 7px solid transparent;
    border-left-color: #e4e7ed;
    border-right: none;
  }
}
</style> 