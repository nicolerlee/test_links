<template>
  <div class="edit-page">
    <div class="page-header">
      <div class="header-left">
        <el-button @click="goBack" :icon="ArrowLeft">返回</el-button>
        <h2>编辑 {{ miniprogram?.name || 'H5网页' }}</h2>
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
            <h3>基本信息</h3>
            <el-tag :type="miniprogram.status === 1 ? 'success' : 'danger'">
              {{ miniprogram.status === 1 ? '启用' : '禁用' }}
            </el-tag>
          </div>
        </template>
        
        <el-form ref="basicFormRef" :model="basicForm" label-width="120px">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="H5网页ID">
                <el-input v-model="basicForm.id" disabled />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="H5网页名称">
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
              placeholder="请输入H5网页描述"
            />
          </el-form-item>
        </el-form>
      </el-card>

      <!-- 域名和链接配置组合 -->
      <el-card class="section-card" shadow="never">
        <template #header>
          <div class="card-header">
            <h3>域名和链接配置</h3>
            <el-button @click="addDomainLinkGroup" type="success" size="small">
              <el-icon><Plus /></el-icon>
              新建域名链接组
            </el-button>
          </div>
        </template>

        <div class="domain-link-groups">
          <div
            v-for="(group, groupIndex) in domainLinkGroups"
            :key="group.id || `new-group-${groupIndex}`"
            class="domain-link-group"
          >
            <el-card shadow="hover" class="group-card">
              <template #header>
                <div class="group-header">
                  <div class="group-title">
                    <el-tag>{{ group.domain_type }}</el-tag>
                    <span>{{ group.description || `域名链接组 ${groupIndex + 1}` }}</span>
                  </div>
                  <el-button
                    @click="removeDomainLinkGroup(groupIndex)"
                    type="danger"
                    size="small"
                    :icon="Delete"
                    plain
                  />
                </div>
              </template>

              <!-- 域名配置 -->
              <div class="domain-config-section">
                <h4 class="section-title">域名配置</h4>
                <el-form label-width="100px">
                  <el-row :gutter="20">
                    <el-col :span="12">
                      <el-form-item label="域名类型">
                        <el-select 
                          v-model="group.domain_type" 
                          style="width: 100%"
                          @change="handleDomainTypeChange($event, 'group', groupIndex)"
                        >
                          <el-option 
                            v-for="domainType in domainTypes" 
                            :key="domainType.id"
                            :label="domainType.domain_type" 
                            :value="domainType.domain_type" 
                          />
                          <el-option 
                            label="+ 新增域名类型"
                            value="__ADD_NEW__"
                            style="color: #409eff; font-weight: 600;"
                          />
                        </el-select>
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item label="描述">
                        <el-input v-model="group.description" placeholder="域名用途描述" />
                      </el-form-item>
                    </el-col>
                  </el-row>
                  <el-row :gutter="20">
                    <el-col :span="12">
                      <el-form-item label="测试域名">
                        <el-input v-model="group.test_domain" placeholder="https://test.example.com" />
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item label="正式域名">
                        <el-input v-model="group.prod_domain" placeholder="https://prod.example.com" />
                      </el-form-item>
                    </el-col>
                  </el-row>
                  <el-row :gutter="20">
                    <el-col :span="8">
                      <el-form-item label="一级目录">
                        <el-input v-model="group.first_level" placeholder="一级目录" />
                      </el-form-item>
                    </el-col>
                    <el-col :span="8">
                      <el-form-item label="二级目录">
                        <el-input v-model="group.second_level" placeholder="二级目录" />
                      </el-form-item>
                    </el-col>
                    <el-col :span="8">
                      <el-form-item label="三级目录">
                        <el-input v-model="group.third_level" placeholder="三级目录" />
                      </el-form-item>
                    </el-col>
                  </el-row>
                </el-form>
              </div>

              <!-- 链接管理 -->
              <div class="links-section">
                <div class="links-header">
                  <h4 class="section-title">链接管理</h4>
                  <el-button 
                    @click="addLinkToGroup(groupIndex)" 
                    type="primary" 
                    size="small"
                  >
                    <el-icon><Plus /></el-icon>
                    新增链接
                  </el-button>
                </div>
                
                <el-table :data="group.links" stripe>
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
                  <el-table-column label="域名类型" width="150">
                    <template #default="{ row, $index }">
                      <el-select 
                        v-model="row.domain_type" 
                        style="width: 100%"
                        @change="handleDomainTypeChange($event, 'link', groupIndex, $index)"
                      >
                        <el-option 
                          v-for="domainType in domainTypes" 
                          :key="domainType.id"
                          :label="domainType.domain_type" 
                          :value="domainType.domain_type" 
                        />
                        <el-option 
                          label="+ 新增域名类型"
                          value="__ADD_NEW__"
                          style="color: #409eff; font-weight: 600;"
                        />
                      </el-select>
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
                        @click="removeLinkFromGroup(groupIndex, $index)"
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
        </div>
      </el-card>
    </div>

    <div v-else class="error-container">
      <el-result icon="warning" title="H5网页不存在" sub-title="请检查H5网页ID是否正确">
        <template #extra>
          <el-button @click="goBack">返回</el-button>
        </template>
      </el-result>
    </div>

    <!-- 新增域名类型对话框 -->
    <el-dialog 
      v-model="showAddDomainTypeDialog" 
      title="新增域名类型" 
      width="500px"
      :before-close="() => showAddDomainTypeDialog = false"
    >
      <el-form 
        ref="domainTypeFormRef" 
        :model="newDomainTypeForm" 
        label-width="100px"
        :rules="{
          domain_type: [
            { required: true, message: '请输入域名类型', trigger: 'blur' },
            { min: 1, max: 50, message: '域名类型长度应在1到50个字符', trigger: 'blur' }
          ]
        }"
      >
        <el-form-item label="域名类型" prop="domain_type">
          <el-input 
            v-model="newDomainTypeForm.domain_type" 
            placeholder="请输入域名类型，如：default、order、claim"
            maxlength="50"
            show-word-limit
          />
        </el-form-item>
        <el-form-item label="描述">
          <el-input 
            v-model="newDomainTypeForm.description" 
            placeholder="请输入域名类型的描述（可选）"
            maxlength="200"
            show-word-limit
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAddDomainTypeDialog = false">取消</el-button>
          <el-button type="primary" @click="addNewDomainType">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  ArrowLeft,
  Check,
  Plus,
  Delete
} from '@element-plus/icons-vue'
import { miniprogramAPI, categoryAPI, domainConfigAPI, domainTypeAPI, linkAPI } from '@/api'

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
const saving = ref(false)
const miniprogram = ref(null)
const categories = ref([])
const domainTypes = ref([])

// 表单数据
const basicForm = reactive({
  id: '',
  name: '',
  category_id: '',
  description: '',
  status: 1
})

// 新增域名类型对话框
const showAddDomainTypeDialog = ref(false)
const domainTypeFormRef = ref(null)
const newDomainTypeForm = reactive({
  domain_type: '',
  description: ''
})

// 域名链接组合数据
const domainLinkGroups = ref([])
let tempIdCounter = 0

// 方法
const loadData = async () => {
  try {
    loading.value = true
    
    // 并行加载数据
    const [miniprogramData, categoriesData, domainTypesData] = await Promise.all([
      miniprogramAPI.getMiniprogram(props.id),
      categoryAPI.getCategories(),
      domainTypeAPI.getDomainTypesByMiniprogram(props.id)
    ])
    
    if (!miniprogramData) {
      return
    }
    
    miniprogram.value = miniprogramData
    categories.value = categoriesData
    domainTypes.value = domainTypesData
    
    // 填充基本信息表单
    Object.assign(basicForm, {
      id: miniprogramData.id,
      name: miniprogramData.name,
      category_id: miniprogramData.category_id,
      description: miniprogramData.description || '',
      status: miniprogramData.status
    })
    
    // 组织域名链接组合数据
    const domainConfigs = miniprogramData.domain_configs || []
    const links = miniprogramData.links || []
    
    // 如果有域名配置，按域名配置组织
    if (domainConfigs.length > 0) {
      domainLinkGroups.value = domainConfigs.map(config => ({
        ...config,
        links: links.filter(link => link.domain_type === config.domain_type).map(link => ({
          ...link,
          _tempId: link.id || `temp_${++tempIdCounter}`
        })) || []
      }))
    } else {
      // 如果没有域名配置，创建一个默认组
      domainLinkGroups.value = [{
        miniprogram_id: props.id,
        domain_type: 'default',
        test_domain: '',
        prod_domain: '',
        first_level: '',
        second_level: '',
        third_level: '',
        description: '默认域名配置',
        status: 1,
        _isNew: true,
        links: links.map(link => ({
          ...link,
          _tempId: link.id || `temp_${++tempIdCounter}`
        }))
      }]
    }
    
  } catch (error) {
    ElMessage.error('加载数据失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

const addDomainLinkGroup = () => {
  domainLinkGroups.value.push({
    miniprogram_id: props.id,
    domain_type: 'default',
    test_domain: '',
    prod_domain: '',
    first_level: '',
    second_level: '',
    third_level: '',
    description: '',
    status: 1,
    _isNew: true,
    links: []
  })
}

const removeDomainLinkGroup = async (groupIndex) => {
  const group = domainLinkGroups.value[groupIndex]
  
  if (group.id && !group._isNew) {
    try {
      await ElMessageBox.confirm('确定要删除这个域名链接组吗？这将同时删除其下的所有链接。', '确认删除', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      })
      
      // 删除域名配置
      await domainConfigAPI.deleteDomainConfig(group.id)
      
      // 删除相关链接
      for (const link of group.links) {
        if (link.id && !link._isNew) {
          await linkAPI.deleteLink(link.id)
        }
      }
      
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
  
  domainLinkGroups.value.splice(groupIndex, 1)
}

const addLinkToGroup = (groupIndex) => {
  const group = domainLinkGroups.value[groupIndex]
  group.links.push({
    miniprogram_id: props.id,
    title: '',
    url: '',
    domain_type: group.domain_type || (domainTypes.value.length > 0 ? domainTypes.value[0].domain_type : 'default'),
    sort_order: group.links.length,
    status: 1,
    _isNew: true,
    _tempId: `temp_${++tempIdCounter}`
  })
}

const removeLinkFromGroup = async (groupIndex, linkIndex) => {
  const group = domainLinkGroups.value[groupIndex]
  const link = group.links[linkIndex]
  
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
  
  group.links.splice(linkIndex, 1)
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
    
    // 2. 保存域名链接组合
    for (const group of domainLinkGroups.value) {
      const configData = {
        miniprogram_id: props.id,
        domain_type: group.domain_type,
        test_domain: group.test_domain,
        prod_domain: group.prod_domain,
        first_level: group.first_level,
        second_level: group.second_level,
        third_level: group.third_level,
        description: group.description,
        status: group.status || 1
      }
      
      let domainConfigId = group.id
      
      // 保存域名配置
      if (group._isNew || !group.id) {
        const result = await domainConfigAPI.createDomainConfig(configData)
        domainConfigId = result.id
        group.id = domainConfigId
      } else {
        await domainConfigAPI.updateDomainConfig(group.id, configData)
      }
      
      // 保存该组的链接
      for (const link of group.links) {
        const linkData = {
          miniprogram_id: props.id,
          title: link.title,
          url: link.url,
          domain_type: link.domain_type,
          sort_order: link.sort_order,
          status: (link.status !== undefined && link.status !== null) ? link.status : 1
        }
        
        if (link._isNew || !link.id) {
          const result = await linkAPI.createLink(linkData)
          link.id = result.id
          link._isNew = false // 清除新建标记
        } else {
          await linkAPI.updateLink(link.id, linkData)
        }
      }
      
      // 清除组的新建标记
      group._isNew = false
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

// 新增域名类型相关方法
const openAddDomainTypeDialog = () => {
  newDomainTypeForm.domain_type = ''
  newDomainTypeForm.description = ''
  showAddDomainTypeDialog.value = true
}

const addNewDomainType = async () => {
  try {
    // 表单验证
    if (!domainTypeFormRef.value) {
      return
    }
    
    const valid = await domainTypeFormRef.value.validate()
    if (!valid) {
      return
    }
    
    // 检查是否已存在相同的域名类型
    const existingType = domainTypes.value.find(type => 
      type.domain_type === newDomainTypeForm.domain_type.trim()
    )
    
    if (existingType) {
      ElMessage.error('该域名类型已存在')
      return
    }
    
    // 保存新的域名类型
    const result = await domainTypeAPI.createDomainType({
      miniprogram_id: props.id,
      domain_type: newDomainTypeForm.domain_type.trim(),
      description: newDomainTypeForm.description.trim()
    })
    
    // 添加到本地数组
    domainTypes.value.push(result)
    
    ElMessage.success('新增域名类型成功')
    showAddDomainTypeDialog.value = false
    
    return result.domain_type
    
  } catch (error) {
    ElMessage.error('新增域名类型失败')
    console.error(error)
  }
}

// 处理域名类型选择变化
const handleDomainTypeChange = async (value, type, groupIndex, linkIndex) => {
  if (value === '__ADD_NEW__') {
    // 记录当前选择的位置和原始值
    const currentSelection = { type, groupIndex, linkIndex }
    let originalValue = ''
    
    // 获取原始值并暂时恢复
    if (type === 'group') {
      originalValue = domainLinkGroups.value[groupIndex].domain_type
      domainLinkGroups.value[groupIndex].domain_type = originalValue || (domainTypes.value.length > 0 ? domainTypes.value[0].domain_type : '')
    } else if (type === 'link') {
      originalValue = domainLinkGroups.value[groupIndex].links[linkIndex].domain_type
      domainLinkGroups.value[groupIndex].links[linkIndex].domain_type = originalValue || (domainTypes.value.length > 0 ? domainTypes.value[0].domain_type : '')
    }
    
    // 保存当前domainTypes数量，用于判断是否新增了域名类型
    const originalDomainTypesCount = domainTypes.value.length
    
    // 打开新增对话框
    openAddDomainTypeDialog()
    
    // 监听对话框关闭事件
    const unwatch = watch(showAddDomainTypeDialog, (newVal) => {
      if (!newVal) {
        // 对话框关闭时检查是否新增了域名类型
        if (domainTypes.value.length > originalDomainTypesCount) {
          // 有新增的域名类型，设置为新增的域名类型
          const newDomainType = domainTypes.value[domainTypes.value.length - 1]
          
          if (currentSelection.type === 'group') {
            domainLinkGroups.value[currentSelection.groupIndex].domain_type = newDomainType.domain_type
          } else if (currentSelection.type === 'link') {
            domainLinkGroups.value[currentSelection.groupIndex].links[currentSelection.linkIndex].domain_type = newDomainType.domain_type
          }
        }
        
        unwatch()
      }
    })
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

.domain-link-groups {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
}

.domain-link-group {
  border: 2px solid #f0f0f0;
  border-radius: 8px;
  overflow: hidden;
  transition: border-color 0.3s ease;
}

.domain-link-group:hover {
  border-color: #409eff;
}

.group-card {
  border: none;
  box-shadow: none;
}

.group-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f8f9fa;
  padding: 12px 16px;
  border-bottom: 1px solid #e9ecef;
}

.group-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.domain-config-section {
  padding: 20px;
  border-bottom: 1px solid #ebeef5;
}

.links-section {
  padding: 20px;
}

.section-title {
  margin: 0 0 15px 0;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.links-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
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

/* 新增域名类型对话框样式 */
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

/* 新增域名类型选项样式 */
:deep(.el-select-dropdown__item) {
  transition: all 0.3s ease;
}

:deep(.el-select-dropdown__item:hover) {
  background-color: #f5f7fa;
}
</style> 