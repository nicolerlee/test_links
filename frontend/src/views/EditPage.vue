<template>
  <div class="edit-page">
    <div class="page-header">
      <div class="header-left">
        <el-button @click="goBack" :icon="ArrowLeft">返回</el-button>
        <h2>编辑小程序</h2>
      </div>
      <div class="header-actions">
        <el-button @click="saveAll" type="primary" :loading="saving">
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
            <el-button @click="addDomainConfig" type="primary" size="small">
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
            <el-button @click="addLink" type="primary" size="small">
              <el-icon><Plus /></el-icon>
              新增链接
            </el-button>
          </div>
        </template>

        <div class="links-table">
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
                />
              </template>
            </el-table-column>
          </el-table>
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
  Delete
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
    links.value = miniprogramData.links || []
    
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
    _isNew: true
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
        status: link.status || 1
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

.links-table {
  margin-top: 10px;
}

:deep(.el-card__header) {
  background-color: #fafafa;
  border-bottom: 1px solid #ebeef5;
}

:deep(.el-table) {
  border: 1px solid #ebeef5;
}

:deep(.el-input-number.is-controls-right .el-input__inner) {
  text-align: left;
}
</style> 