<template>
  <div class="view-page">
    <div class="page-header">
      <div class="header-left">
        <el-button @click="goBack" :icon="ArrowLeft">返回</el-button>
        <h2>查看小程序</h2>
      </div>
      <div class="header-actions">
        <el-button @click="editMiniprogram" type="primary">
          <el-icon><Edit /></el-icon>
          编辑
        </el-button>
      </div>
    </div>

    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="8" animated />
    </div>

    <div v-else-if="miniprogram" class="content-area">
      <!-- 小程序基本信息 -->
      <el-card class="section-card" shadow="never">
        <template #header>
          <div class="card-header">
            <h3>{{ miniprogram.name }}</h3>
            <div class="header-tags">
              <el-tag :type="miniprogram.status === 1 ? 'success' : 'danger'">
                {{ miniprogram.status === 1 ? '启用' : '禁用' }}
              </el-tag>
              <el-tag type="info">{{ miniprogram.category?.name }}</el-tag>
            </div>
          </div>
        </template>
        
        <div class="basic-info">
          <el-row :gutter="20">
            <el-col :span="12">
              <div class="info-item">
                <label>小程序ID:</label>
                <span>{{ miniprogram.id }}</span>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="info-item">
                <label>创建时间:</label>
                <span>{{ formatDateTime(miniprogram.created_at) }}</span>
              </div>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="12">
              <div class="info-item">
                <label>所属分类:</label>
                <span>{{ miniprogram.category?.name || '未知分类' }}</span>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="info-item">
                <label>更新时间:</label>
                <span>{{ formatDateTime(miniprogram.updated_at) }}</span>
              </div>
            </el-col>
          </el-row>
          <div class="info-item">
            <label>描述:</label>
            <span>{{ miniprogram.description || '暂无描述' }}</span>
          </div>
          <div class="info-item">
            <label>统计信息:</label>
            <div class="stats">
              <el-tag size="large" type="info">
                <el-icon><Link /></el-icon>
                域名配置: {{ miniprogram.domain_configs?.length || 0 }}
              </el-tag>
              <el-tag size="large" type="success">
                <el-icon><Connection /></el-icon>
                链接数量: {{ miniprogram.links?.length || 0 }}
              </el-tag>
            </div>
          </div>
        </div>
      </el-card>

      <!-- 域名配置展示 -->
      <el-card v-if="miniprogram.domain_configs?.length" class="section-card" shadow="never">
        <template #header>
          <div class="card-header">
            <h3>域名配置</h3>
            <el-tag>{{ miniprogram.domain_configs.length }} 个配置</el-tag>
          </div>
        </template>

        <div class="domain-configs">
          <div
            v-for="config in miniprogram.domain_configs"
            :key="config.id"
            class="domain-config-item"
          >
            <el-card shadow="hover">
              <template #header>
                <div class="config-header">
                  <div class="config-title">
                    <el-tag :type="getDomainTypeColor(config.domain_type)">
                      {{ getDomainTypeName(config.domain_type) }}
                    </el-tag>
                    <span>{{ config.description || '域名配置' }}</span>
                  </div>
                  <el-tag
                    :type="config.status === 1 ? 'success' : 'danger'"
                    size="small"
                  >
                    {{ config.status === 1 ? '启用' : '禁用' }}
                  </el-tag>
                </div>
              </template>

              <div class="domain-info">
                <el-row :gutter="20" v-if="config.test_domain || config.prod_domain">
                  <el-col :span="12" v-if="config.test_domain">
                    <div class="domain-item">
                      <label>测试域名:</label>
                      <div class="domain-url">
                        <el-link :href="config.test_domain" target="_blank" type="primary">
                          {{ config.test_domain }}
                          <el-icon><TopRight /></el-icon>
                        </el-link>
                      </div>
                    </div>
                  </el-col>
                  <el-col :span="12" v-if="config.prod_domain">
                    <div class="domain-item">
                      <label>正式域名:</label>
                      <div class="domain-url">
                        <el-link :href="config.prod_domain" target="_blank" type="primary">
                          {{ config.prod_domain }}
                          <el-icon><TopRight /></el-icon>
                        </el-link>
                      </div>
                    </div>
                  </el-col>
                </el-row>
                
                <div v-if="config.first_level || config.second_level || config.third_level" class="path-info">
                  <label>路径结构:</label>
                  <div class="path-breadcrumb">
                    <el-breadcrumb separator="/">
                      <el-breadcrumb-item v-if="config.first_level">{{ config.first_level }}</el-breadcrumb-item>
                      <el-breadcrumb-item v-if="config.second_level">{{ config.second_level }}</el-breadcrumb-item>
                      <el-breadcrumb-item v-if="config.third_level">{{ config.third_level }}</el-breadcrumb-item>
                    </el-breadcrumb>
                  </div>
                </div>
              </div>
            </el-card>
          </div>
        </div>
      </el-card>

      <!-- 链接展示 -->
      <el-card v-if="miniprogram.links?.length" class="section-card" shadow="never">
        <template #header>
          <div class="card-header">
            <h3>链接管理</h3>
            <el-tag>{{ activeLinks.length }} / {{ miniprogram.links.length }} 个链接</el-tag>
          </div>
        </template>

        <div class="links-section">
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
              :class="{ disabled: link.status !== 1 }"
            >
              <div class="link-header">
                <div class="link-title">
                  <el-tag size="small" type="info">{{ index + 1 }}</el-tag>
                  <span class="title-text">{{ link.title }}</span>
                  <el-tag 
                    :type="link.status === 1 ? 'success' : 'danger'" 
                    size="small"
                  >
                    {{ link.status === 1 ? '启用' : '禁用' }}
                  </el-tag>
                </div>
                <div class="link-actions">
                  <el-button
                    v-if="link.status === 1"
                    @click="copyLink(link.url)"
                    type="primary"
                    size="small"
                  >
                    <el-icon><CopyDocument /></el-icon>
                    复制链接
                  </el-button>
                </div>
              </div>
              <div class="link-url">
                <el-input
                  :value="link.url"
                  readonly
                  type="textarea"
                  :rows="2"
                  resize="none"
                />
              </div>
            </div>
          </div>
        </div>
      </el-card>

      <!-- 空状态 -->
      <div v-if="!miniprogram.domain_configs?.length && !miniprogram.links?.length" class="empty-state">
        <el-empty description="暂无配置数据">
          <el-button @click="editMiniprogram" type="primary">
            添加配置
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
import { ref, computed, onMounted } from 'vue'
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
  CopyDocument
} from '@element-plus/icons-vue'
import { miniprogramAPI } from '@/api'

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

// 计算属性
const activeLinks = computed(() => {
  return miniprogram.value?.links?.filter(link => link.status === 1) || []
})

const inactiveLinks = computed(() => {
  return miniprogram.value?.links?.filter(link => link.status !== 1) || []
})

const sortedLinks = computed(() => {
  return miniprogram.value?.links?.slice().sort((a, b) => a.sort_order - b.sort_order) || []
})

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

const getDomainTypeName = (type) => {
  const typeMap = {
    default: '默认',
    order: '订购',
    receive: '领取',
    pay: '付费',
    share: '分享',
    custom: '自定义'
  }
  return typeMap[type] || type
}

const getDomainTypeColor = (type) => {
  const colorMap = {
    default: '',
    order: 'warning',
    receive: 'success',
    pay: 'danger',
    share: 'info',
    custom: 'primary'
  }
  return colorMap[type] || ''
}

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

// 生命周期
onMounted(() => {
  loadData()
})
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
  margin-bottom: 20px;
  padding-bottom: 20px;
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

.loading-container,
.error-container {
  background: white;
  border-radius: 8px;
  padding: 40px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.08);
}

.content-area {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.section-card {
  border: 1px solid #ebeef5;
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
  font-size: 18px;
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
  padding: 10px 0;
}

.links-summary {
  margin-bottom: 30px;
  padding: 20px;
  background: #fafafa;
  border-radius: 8px;
}

.links-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.link-item {
  border: 1px solid #ebeef5;
  border-radius: 8px;
  padding: 15px;
  transition: all 0.3s;
}

.link-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.link-item.disabled {
  opacity: 0.6;
  background: #f5f7fa;
}

.link-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.link-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.title-text {
  font-weight: 500;
  color: #303133;
}

.link-url {
  margin-top: 10px;
}

.empty-state {
  padding: 40px;
  text-align: center;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.08);
}

:deep(.el-card__header) {
  background-color: #fafafa;
  border-bottom: 1px solid #ebeef5;
}

:deep(.el-statistic__content) {
  display: flex;
  align-items: center;
  justify-content: center;
}

:deep(.el-textarea__inner) {
  background: #f5f7fa;
  border: 1px solid #dcdfe6;
}
</style> 