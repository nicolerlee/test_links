<template>
  <div class="edit-page">
    <div class="page-header">
      <div class="header-left">
        <el-button @click="goBack" :icon="ArrowLeft">返回</el-button>
        <h2>编辑小程序</h2>
      </div>
      <div class="header-actions">
        <el-button @click="saveAll" type="info" :loading="saving">
          <el-icon><Check /></el-icon>
          保存所有修改
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
            <el-tag :type="miniprogram.status === 1 ? 'success' : 'danger'">
              {{ miniprogram.status === 1 ? '启用' : '禁用' }}
            </el-tag>
          </div>
        </template>
        
        <el-form ref="basicFormRef" :model="basicForm" label-width="120px">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="小程序ID">
                <el-input v-model="basicForm.id" disabled />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="小程序名称">
                <el-input v-model="basicForm.name" />
              </el-form-item>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="分类">
                <el-select v-model="basicForm.category_id" style="width: 100%">
                  <el-option
                    v-for="category in categories"
                    :key="category.id"
                    :label="category.name"
                    :value="category.id"
                  />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="状态">
                <el-switch
                  v-model="basicForm.status"
                  :active-value="1"
                  :inactive-value="0"
                  active-text="启用"
                  inactive-text="禁用"
                />
              </el-form-item>
            </el-col>
          </el-row>
          <el-form-item label="描述">
            <el-input
              v-model="basicForm.description"
              type="textarea"
              :rows="3"
              placeholder="请输入小程序描述"
            />
          </el-form-item>
        </el-form>
      </el-card>

      <!-- 域名配置 -->
      <el-card class="section-card" shadow="never">
        <template #header>
          <div class="card-header">
            <h3>域名配置</h3>
            <el-button @click="addDomainConfig" type="success" size="small">
              <el-icon><Plus /></el-icon>
              新增域名配置
            </el-button>
          </div>
        </template>

        <div class="domain-configs">
          <div
            v-for="(config, index) in domainConfigs"
            :key="config.id || `new-${index}`"
            class="domain-config-item"
          >
            <el-card shadow="hover">
              <template #header>
                <div class="config-header">
                  <div class="config-title">
                    <el-tag>{{ config.domain_type }}</el-tag>
                    <span>{{ config.description || '域名配置' }}</span>
                  </div>
                  <el-button
                    @click="removeDomainConfig(index)"
                    type="danger"
                    size="small"
                    :icon="Delete"
                    plain
                  />
                </div>
              </template>

              <el-form label-width="100px">
                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="域名类型">
                      <el-select v-model="config.domain_type" style="width: 100%">
                        <el-option label="默认" value="default" />
                        <el-option label="订购" value="order" />
                        <el-option label="领取" value="receive" />
                        <el-option label="付费" value="pay" />
                        <el-option label="分享" value="share" />
                        <el-option label="自定义" value="custom" />
                      </el-select>
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item label="描述">
                      <el-input v-model="config.description" placeholder="域名用途描述" />
                    </el-form-item>
                  </el-col>
                </el-row>
                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="测试域名">
                      <el-input v-model="config.test_domain" placeholder="https://test.example.com" />
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item label="正式域名">
                      <el-input v-model="config.prod_domain" placeholder="https://prod.example.com" />
                    </el-form-item>
                  </el-col>
                </el-row>
                <el-row :gutter="20">
                  <el-col :span="8">
                    <el-form-item label="一级目录">
                      <el-input v-model="config.first_level" placeholder="一级目录" />
                    </el-form-item>
                  </el-col>
                  <el-col :span="8">
                    <el-form-item label="二级目录">
                      <el-input v-model="config.second_level" placeholder="二级目录" />
                    </el-form-item>
                  </el-col>
                  <el-col :span="8">
                    <el-form-item label="三级目录">
                      <el-input v-model="config.third_level" placeholder="三级目录" />
                    </el-form-item>
                  </el-col>
                </el-row>
              </el-form>
            </el-card>
          </div>
        </div>
      </el-card>

            <!-- 链接管理 -->
      <el-card class="section-card" shadow="never">
        <template #header>
          <div class="card-header">
            <h3>链接管理</h3>
            <div class="mode-switch">
              <el-button-group>
                <el-button 
                  @click="linkEditMode = 'single'" 
                  :type="linkEditMode === 'single' ? 'success' : 'default'"
                  size="small"
                >
                  <el-icon><Edit /></el-icon>
                  单条编辑
                </el-button>
                <el-button 
                  @click="linkEditMode = 'batch'" 
                  :type="linkEditMode === 'batch' ? 'success' : 'default'"
                  size="small"
                >
                  <el-icon><Operation /></el-icon>
                  批量编辑
                </el-button>
              </el-button-group>
            </div>
          </div>
        </template>

        <!-- 单条编辑模式 -->
        <div v-if="linkEditMode === 'single'" class="links-table">
          <div class="table-header">
            <span class="table-title">链接列表</span>
            <el-button 
              @click="addLink" 
              type="primary" 
              size="small"
            >
              <el-icon><Plus /></el-icon>
              新增链接
            </el-button>
          </div>
          <el-table :data="links" stripe>
            <el-table-column label="排序" width="80">
              <template #default="{ row }">
                <el-input-number
                  v-model="row.sort_order"
                  :min="0"
                  :max="999"
                  size="small"
                  controls-position="right"
                />
              </template>
            </el-table-column>
            <el-table-column label="标题" min-width="200">
              <template #default="{ row }">
                <el-input v-model="row.title" placeholder="请输入链接标题" />
              </template>
            </el-table-column>
            <el-table-column label="URL" min-width="300">
              <template #default="{ row }">
                <el-input v-model="row.url" placeholder="请输入链接URL" />
              </template>
            </el-table-column>
            <el-table-column label="状态" width="100">
              <template #default="{ row }">
                <el-switch
                  v-model="row.status"
                  :active-value="1"
                  :inactive-value="0"
                />
              </template>
            </el-table-column>
            <el-table-column label="操作" width="100">
              <template #default="{ $index }">
                <el-button
                  @click="removeLink($index)"
                  type="danger"
                  size="small"
                  :icon="Delete"
                  plain
                />
              </template>
            </el-table-column>
          </el-table>
        </div>

        <!-- 批量编辑模式 -->
        <div v-else class="batch-edit-container">
          <div class="batch-mode-header">
            <span class="batch-mode-title">批量编辑模式</span>
            <el-tag type="info" size="small">当前共 {{ links.length }} 个链接</el-tag>
          </div>
          
          <!-- 批量导入区域 -->
          <el-card class="batch-import-card" shadow="never">
            <template #header>
              <div class="card-header">
                <h4>批量导入链接</h4>
                <el-button @click="showImportHelp = !showImportHelp" type="text" size="small">
                  <el-icon><QuestionFilled /></el-icon>
                  导入格式说明
                </el-button>
              </div>
            </template>
            
            <div v-if="showImportHelp" class="import-help">
              <el-alert
                title="导入格式说明"
                type="info"
                :closable="false"
                show-icon
              >
                <template #default>
                  <p>请按以下格式输入链接信息，每行一个链接：</p>
                  <p><strong>格式：</strong> 标题 URL 排序(可选)</p>
                  <p><strong>说明：</strong> 用单个或多个空格分隔，标题可以包含空格</p>
                  <p><strong>示例：</strong></p>
                  <pre>投流链接 /pages/readerPage/readerPage?id=123 1
退出登录 /pages/mine/mine 2
首页链接 /pages/index/index</pre>
                </template>
              </el-alert>
            </div>

            <el-form label-width="100px">
              <el-form-item label="导入内容">
                <el-input
                  v-model="batchImportText"
                  type="textarea"
                  :rows="8"
                  placeholder="请输入链接信息，每行一个链接&#10;格式：标题 URL 排序(可选)&#10;示例：投流链接 /pages/readerPage/readerPage?id=123 1"
                />
              </el-form-item>
              <el-form-item>
                <el-button @click="parseBatchImport" type="primary">
                  <el-icon><DocumentAdd /></el-icon>
                  解析并导入
                </el-button>
                <el-button @click="clearBatchImport" type="default">
                  <el-icon><RefreshLeft /></el-icon>
                  清空
                </el-button>
              </el-form-item>
            </el-form>
          </el-card>

          <!-- 批量操作区域 -->
          <el-card class="batch-operations-card" shadow="never">
            <template #header>
              <div class="card-header">
                <h4>批量操作</h4>
                <div class="batch-actions">
                  <el-button
                    @click="selectAllLinks"
                    :disabled="links.length === 0"
                    size="small"
                  >
                    全选
                  </el-button>
                  <el-button
                    @click="selectNoneLinks"
                    :disabled="selectedLinks.length === 0"
                    size="small"
                  >
                    取消全选
                  </el-button>
                  <el-button
                    @click="batchUpdateStatus(1)"
                    :disabled="selectedLinks.length === 0"
                    type="success"
                    size="small"
                    plain
                  >
                    <el-icon><Check /></el-icon>
                    批量启用
                  </el-button>
                  <el-button
                    @click="batchUpdateStatus(0)"
                    :disabled="selectedLinks.length === 0"
                    type="warning"
                    size="small"
                    plain
                  >
                    <el-icon><Close /></el-icon>
                    批量禁用
                  </el-button>
                  <el-button
                    @click="batchDeleteLinks"
                    :disabled="selectedLinks.length === 0"
                    type="danger"
                    size="small"
                    plain
                  >
                    <el-icon><Delete /></el-icon>
                    批量删除
                  </el-button>
                </div>
              </div>
            </template>

            <div class="batch-table">
              <el-table 
                :data="links" 
                stripe 
                @selection-change="handleSelectionChange"
                :row-key="(row) => row.id || row._tempId"
              >
                <el-table-column type="selection" width="55" />
                <el-table-column label="排序" width="100">
                  <template #default="{ row }">
                    <el-input-number
                      v-model="row.sort_order"
                      :min="0"
                      :max="999"
                      size="small"
                      controls-position="right"
                    />
                  </template>
                </el-table-column>
                <el-table-column label="标题" min-width="200">
                  <template #default="{ row }">
                    <el-input v-model="row.title" placeholder="请输入链接标题" size="small" />
                  </template>
                </el-table-column>
                <el-table-column label="URL" min-width="300">
                  <template #default="{ row }">
                    <el-input v-model="row.url" placeholder="请输入链接URL" size="small" />
                  </template>
                </el-table-column>
                <el-table-column label="状态" width="100">
                  <template #default="{ row }">
                    <el-switch
                      v-model="row.status"
                      :active-value="1"
                      :inactive-value="0"
                      size="small"
                    />
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="100">
                  <template #default="{ $index }">
                    <el-button
                      @click="removeLink($index)"
                      type="danger"
                      size="small"
                      :icon="Delete"
                      plain
                    />
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </el-card>
        </div>
      </el-card>
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
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  ArrowLeft,
  Check,
  Plus,
  Delete,
  Edit,
  Operation,
  QuestionFilled,
  DocumentAdd,
  RefreshLeft,
  Close
} from '@element-plus/icons-vue'
import { miniprogramAPI, categoryAPI, domainConfigAPI, linkAPI } from '@/api'

const router = useRouter()
const route = useRoute()

// Props
const props = defineProps({
  id: {
    type: String,
    required: true
  }
})

// 响应式数据
const loading = ref(true)
const saving = ref(false)
const miniprogram = ref(null)
const categories = ref([])

// 表单数据
const basicForm = reactive({
  id: '',
  name: '',
  category_id: '',
  description: '',
  status: 1
})

const domainConfigs = ref([])
const links = ref([])

// 批量编辑相关数据
const linkEditMode = ref('single') // 'single' 或 'batch'
const batchImportText = ref('')
const showImportHelp = ref(false)
const selectedLinks = ref([])
let tempIdCounter = 0

// 方法
const loadData = async () => {
  try {
    loading.value = true
    
    // 并行加载数据
    const [miniprogramData, categoriesData] = await Promise.all([
      miniprogramAPI.getMiniprogram(props.id),
      categoryAPI.getCategories()
    ])
    
    if (!miniprogramData) {
      return
    }
    
    miniprogram.value = miniprogramData
    categories.value = categoriesData
    
    // 填充基本信息表单
    Object.assign(basicForm, {
      id: miniprogramData.id,
      name: miniprogramData.name,
      category_id: miniprogramData.category_id,
      description: miniprogramData.description || '',
      status: miniprogramData.status
    })
    
    // 设置域名配置和链接
    domainConfigs.value = miniprogramData.domain_configs || []
    links.value = (miniprogramData.links || []).map(link => ({
      ...link,
      _tempId: link.id || `temp_${++tempIdCounter}`
    }))
    
  } catch (error) {
    ElMessage.error('加载数据失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

const addDomainConfig = () => {
  domainConfigs.value.push({
    miniprogram_id: props.id,
    domain_type: 'default',
    test_domain: '',
    prod_domain: '',
    first_level: '',
    second_level: '',
    third_level: '',
    description: '',
    status: 1,
    _isNew: true
  })
}

const removeDomainConfig = async (index) => {
  const config = domainConfigs.value[index]
  
  if (config.id && !config._isNew) {
    try {
      await ElMessageBox.confirm('确定要删除这个域名配置吗？', '确认删除', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      })
      
      await domainConfigAPI.deleteDomainConfig(config.id)
      ElMessage.success('删除成功')
    } catch (error) {
      if (error !== 'cancel') {
        ElMessage.error('删除失败')
        return
      } else {
        return
      }
    }
  }
  
  domainConfigs.value.splice(index, 1)
}

const addLink = () => {
  links.value.push({
    miniprogram_id: props.id,
    title: '',
    url: '',
    sort_order: links.value.length,
    status: 1,
    _isNew: true,
    _tempId: `temp_${++tempIdCounter}`
  })
}

const removeLink = async (index) => {
  const link = links.value[index]
  
  if (link.id && !link._isNew) {
    try {
      await ElMessageBox.confirm('确定要删除这个链接吗？', '确认删除', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      })
      
      await linkAPI.deleteLink(link.id)
      ElMessage.success('删除成功')
    } catch (error) {
      if (error !== 'cancel') {
        ElMessage.error('删除失败')
        return
      } else {
        return
      }
    }
  }
  
  links.value.splice(index, 1)
}

const saveAll = async () => {
  try {
    saving.value = true
    
    // 1. 更新基本信息
    await miniprogramAPI.updateMiniprogram(props.id, {
      name: basicForm.name,
      category_id: basicForm.category_id,
      description: basicForm.description,
      status: basicForm.status
    })
    
    // 2. 保存域名配置
    for (const config of domainConfigs.value) {
      const configData = {
        miniprogram_id: props.id,
        domain_type: config.domain_type,
        test_domain: config.test_domain,
        prod_domain: config.prod_domain,
        first_level: config.first_level,
        second_level: config.second_level,
        third_level: config.third_level,
        description: config.description,
        status: config.status || 1
      }
      
      if (config._isNew || !config.id) {
        await domainConfigAPI.createDomainConfig(configData)
      } else {
        await domainConfigAPI.updateDomainConfig(config.id, configData)
      }
    }
    
    // 3. 保存链接
    for (const link of links.value) {
      const linkData = {
        miniprogram_id: props.id,
        title: link.title,
        url: link.url,
        sort_order: link.sort_order,
        status: (link.status !== undefined && link.status !== null) ? link.status : 1
      }
      
      if (link._isNew || !link.id) {
        await linkAPI.createLink(linkData)
      } else {
        await linkAPI.updateLink(link.id, linkData)
      }
    }
    
    ElMessage.success('保存成功')
    
    // 重新加载数据以更新界面
    await loadData()
    
  } catch (error) {
    ElMessage.error('保存失败')
    console.error(error)
  } finally {
    saving.value = false
  }
}

const goBack = () => {
  router.back()
}

// 批量编辑相关方法
const parseBatchImport = () => {
  if (!batchImportText.value.trim()) {
    ElMessage.warning('请输入链接内容')
    return
  }

  const lines = batchImportText.value.trim().split('\n')
  const newLinks = []
  const errors = []

  lines.forEach((line, index) => {
    const trimmedLine = line.trim()
    if (!trimmedLine) return

    // 按一个或多个空格分割
    const parts = trimmedLine.split(/\s+/)
    if (parts.length < 2) {
      errors.push(`第 ${index + 1} 行格式错误，至少需要标题和URL：${trimmedLine}`)
      return
    }

    let title, url, sortOrder

    // 检查最后一个元素是否是数字（排序）
    const lastPart = parts[parts.length - 1]
    const isLastPartNumber = !isNaN(parseInt(lastPart)) && isFinite(lastPart)

    if (isLastPartNumber && parts.length >= 3) {
      // 格式：标题 URL 排序
      sortOrder = parseInt(lastPart)
      url = parts[parts.length - 2]
      title = parts.slice(0, -2).join(' ')
    } else {
      // 格式：标题 URL
      url = parts[parts.length - 1]
      title = parts.slice(0, -1).join(' ')
      sortOrder = links.value.length + newLinks.length
    }

    if (!title.trim() || !url.trim()) {
      errors.push(`第 ${index + 1} 行标题或URL为空`)
      return
    }

    newLinks.push({
      miniprogram_id: props.id,
      title: title.trim(),
      url: url.trim(),
      sort_order: isNaN(sortOrder) ? links.value.length + newLinks.length : sortOrder,
      status: 1,
      _isNew: true,
      _tempId: `temp_${++tempIdCounter}`
    })
  })

  if (errors.length > 0) {
    ElMessage.error(`解析出错：\n${errors.join('\n')}`)
    return
  }

  if (newLinks.length === 0) {
    ElMessage.warning('没有有效的链接数据')
    return
  }

  // 添加新链接到现有链接列表
  links.value.push(...newLinks)
  ElMessage.success(`成功导入 ${newLinks.length} 个链接`)
  
  // 清空导入文本
  batchImportText.value = ''
}

const clearBatchImport = () => {
  batchImportText.value = ''
  ElMessage.success('已清空导入内容')
}

const handleSelectionChange = (selection) => {
  selectedLinks.value = selection
}

const selectAllLinks = () => {
  // 由于 el-table 的限制，我们通过 ref 来触发全选
  // 这里我们可以模拟全选效果
  selectedLinks.value = [...links.value]
}

const selectNoneLinks = () => {
  selectedLinks.value = []
}

const batchUpdateStatus = (status) => {
  if (selectedLinks.value.length === 0) {
    ElMessage.warning('请先选择要操作的链接')
    return
  }

  selectedLinks.value.forEach(link => {
    link.status = status
  })

  ElMessage.success(`已${status === 1 ? '启用' : '禁用'} ${selectedLinks.value.length} 个链接`)
}

const batchDeleteLinks = async () => {
  if (selectedLinks.value.length === 0) {
    ElMessage.warning('请先选择要删除的链接')
    return
  }

  try {
    await ElMessageBox.confirm(
      `确定要删除选中的 ${selectedLinks.value.length} 个链接吗？此操作不可恢复。`,
      '确认批量删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )

    // 删除已存在的链接
    const existingLinks = selectedLinks.value.filter(link => link.id && !link._isNew)
    for (const link of existingLinks) {
      try {
        await linkAPI.deleteLink(link.id)
      } catch (error) {
        ElMessage.error(`删除链接 "${link.title}" 失败`)
        return
      }
    }

    // 从列表中移除所有选中的链接
    selectedLinks.value.forEach(selectedLink => {
      const index = links.value.findIndex(link => 
        link.id ? link.id === selectedLink.id : link._tempId === selectedLink._tempId
      )
      if (index !== -1) {
        links.value.splice(index, 1)
      }
    })

    ElMessage.success(`成功删除 ${selectedLinks.value.length} 个链接`)
    selectedLinks.value = []
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('批量删除失败')
    }
  }
}

// 生命周期
onMounted(() => {
  loadData()
})
</script>

<style scoped>
.edit-page {
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
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.section-card:last-child {
  margin-bottom: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  padding: 16px 20px;
  border-bottom: 2px solid #dee2e6;
}

.card-header h3 {
  margin: 0;
  color: #303133;
  font-weight: 600;
  font-size: 18px;
}

.domain-configs {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
}

.domain-config-item {
  border: 2px solid #f0f0f0;
  border-radius: 8px;
  overflow: hidden;
  transition: border-color 0.3s ease;
}

.domain-config-item:hover {
  border-color: #409eff;
}

.config-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f8f9fa;
  padding: 12px 16px;
  border-bottom: 1px solid #e9ecef;
}

.config-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.links-table {
  margin-top: 10px;
  padding: 0 20px 20px;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding: 12px 16px;
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 6px;
}

.table-title {
  font-size: 14px;
  font-weight: 600;
  color: #495057;
}

.batch-edit-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
}

.batch-mode-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 6px;
  margin-bottom: 20px;
}

.batch-mode-title {
  font-size: 14px;
  font-weight: 600;
  color: #495057;
}

.batch-import-card,
.batch-operations-card {
  border: 2px solid #e4e7ed;
  background: #f9f9f9;
  border-radius: 8px;
}

.batch-import-card .card-header h4,
.batch-operations-card .card-header h4 {
  margin: 0;
  color: #303133;
  font-weight: 600;
  font-size: 16px;
}

.import-help {
  margin-bottom: 20px;
}

.import-help pre {
  background: #f0f0f0;
  padding: 10px;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 12px;
  line-height: 1.5;
  margin: 8px 0;
}

.batch-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.batch-table {
  margin-top: 10px;
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

:deep(.el-button--primary) {
  background: #409eff;
  border-color: #409eff;
}

:deep(.el-button--success) {
  background: #67c23a;
  border-color: #67c23a;
}

:deep(.el-button--success.is-plain) {
  color: #67c23a;
  background: #f0f9ff;
  border-color: #67c23a;
}

:deep(.el-button--warning.is-plain) {
  color: #e6a23c;
  background: #fdf6ec;
  border-color: #e6a23c;
}

:deep(.el-button--danger.is-plain) {
  color: #f56c6c;
  background: #fef0f0;
  border-color: #f56c6c;
}

:deep(.el-table) {
  border: 1px solid #ebeef5;
}

:deep(.el-input-number.is-controls-right .el-input__inner) {
  text-align: left;
}

/* 批量编辑相关样式 */
.mode-switch {
  display: flex;
  align-items: center;
}

:deep(.batch-import-card .el-card__header) {
  background-color: #f0f9ff;
  border-bottom: 1px solid #e1f5fe;
}

:deep(.batch-operations-card .el-card__header) {
  background-color: #f3f4f6;
  border-bottom: 1px solid #e5e7eb;
}

:deep(.batch-import-card .el-card__body) {
  padding: 20px;
}

:deep(.batch-operations-card .el-card__body) {
  padding: 20px;
}
</style> 