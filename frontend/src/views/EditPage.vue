<template>
  <div class="edit-page">
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="8" animated />
    </div>

    <div v-else-if="miniprogram" class="content-area">
      <!-- 固定头部区域 -->
      <div class="fixed-header" :class="{ 'fixed': isHeaderFixed }">
        <div class="header-content">
          <div class="header-left">
            <el-button @click="goBack" :icon="ArrowLeft" size="small">返回</el-button>
            <h2>编辑 {{ miniprogram.name }}</h2>
          </div>
          <div class="header-right">
            <el-button @click="saveAll" type="default" :loading="saving">
              <el-icon><Check /></el-icon>
              保存所有修改
            </el-button>
          </div>
        </div>
      </div>

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
              <el-form-item label="H5网页名称" required>
                <el-input v-model="basicForm.name" placeholder="请输入H5网页名称" />
              </el-form-item>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="分类" required>
                <el-select v-model="basicForm.category_id" style="width: 100%" placeholder="请选择分类">
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
                  >
                    删除组
                  </el-button>
                </div>
              </template>

              <!-- 域名配置 -->
              <div class="domain-config-section">
                <h4 class="section-title">域名配置</h4>
                <el-form label-width="100px">
                  <el-row :gutter="20">
                    <el-col :span="12">
                      <el-form-item label="域名类型" required>
                        <el-select 
                          v-model="group.domain_type" 
                          style="width: 100%"
                          placeholder="请选择域名类型"
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
                      <el-form-item label="测试域名" required>
                        <el-input v-model="group.test_domain" placeholder="https://test.example.com" />
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item label="正式域名" required>
                        <el-input v-model="group.prod_domain" placeholder="https://prod.example.com" />
                      </el-form-item>
                    </el-col>
                  </el-row>
                  <el-row :gutter="20">
                    <el-col :span="8">
                      <el-form-item label="一级目录" required>
                        <el-input v-model="group.first_level" placeholder="一级目录" />
                      </el-form-item>
                    </el-col>
                    <el-col :span="8">
                      <el-form-item label="二级目录" required>
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
                  <div class="links-actions">
                    <el-button 
                      @click="addLinkToGroup(groupIndex)" 
                      type="primary" 
                      size="small"
                    >
                      <el-icon><Plus /></el-icon>
                      新增链接
                    </el-button>
                    <el-button 
                      @click="openBatchImportDialog(groupIndex)" 
                      type="warning" 
                      size="small"
                    >
                      <el-icon><Upload /></el-icon>
                      批量导入
                    </el-button>
                  </div>
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
                  <el-table-column label="标题 *" min-width="200">
                    <template #default="{ row }">
                      <el-input v-model="row.title" placeholder="请输入链接标题" />
                    </template>
                  </el-table-column>
                  <el-table-column label="URL *" min-width="300">
                    <template #default="{ row }">
                      <el-input 
                        v-model="row.url" 
                        placeholder="请输入页面路径，如：/pages/readerPage/readerPage?cartoon_id=123（不包含域名和目录）" 
                      />
                    </template>
                  </el-table-column>
                  <el-table-column label="域名类型 *" width="150">
                    <template #default="{ row, $index }">
                      <el-select 
                        v-model="row.domain_type" 
                        style="width: 100%"
                        placeholder="请选择域名类型"
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

    <!-- 批量导入对话框 -->
        <el-dialog
      v-model="showBatchImportDialog"
      title="批量导入链接"
      width="700px"
      :before-close="() => showBatchImportDialog = false"
      class="batch-import-dialog"
    >
      <div class="batch-import-content">
        <div class="import-instructions">
          <p><strong>格式：</strong>每行一个链接，<code>标题 页面路径</code> 或 <code>标题 完整URL</code></p>
          <p><small>支持页面路径或完整URL（系统自动提取页面路径）</small></p>
          <div class="examples-container">
            <div class="example-section">
              <p><strong>页面路径示例：</strong></p>
              <pre>退出登录 /pages/userInfo/userInfo
支付链接跳转 /pages/testJump/testJump
阅读页面 /pages/readerPage/readerPage?cartoon_id=123</pre>
            </div>
            <div class="example-section">
              <p><strong>完整URL示例：</strong></p>
              <pre>退出登录 https://noveltestqd.funshion.tv/tt/qudu/pages/userInfo/userInfo
支付链接跳转 https://novelprodqd.funshion.tv/tt/qudu/pages/testJump/testJump</pre>
            </div>
          </div>
        </div>
        
        <div class="import-textarea">
          <el-input
            v-model="batchImportText"
            type="textarea"
            :rows="15"
            placeholder="请输入要导入的链接，每行一个，格式：标题 页面路径 或 标题 完整URL"
            resize="vertical"
          />
        </div>
        
        <div class="import-preview" v-if="parsedLinks.length > 0">
          <h4>预览 ({{ parsedLinks.length }} 个链接)：</h4>
          <div class="preview-list">
            <div 
              v-for="(link, index) in parsedLinks" 
              :key="index"
              class="preview-item"
              :class="{ 'preview-error': link.error }"
            >
              <span class="preview-index">{{ index + 1 }}</span>
              <span class="preview-title">{{ link.title }}</span>
              <span class="preview-url">{{ link.url }}</span>
              <span v-if="link.error" class="preview-error-msg">{{ link.error }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showBatchImportDialog = false">取消</el-button>
          <el-button 
            type="primary" 
            @click="confirmBatchImport"
            :disabled="parsedLinks.length === 0 || hasImportErrors"
          >
            确认导入
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  ArrowLeft,
  Check,
  Plus,
  Delete,
  Upload
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

// 批量导入对话框
const showBatchImportDialog = ref(false)
const batchImportText = ref('')
const currentImportGroupIndex = ref(-1)
const parsedLinks = ref([])
const hasImportErrors = ref(false)

// 页面滚动固定功能
const isHeaderFixed = ref(false)

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
    
    // 验证基本信息
    if (!basicForm.name.trim()) {
      ElMessage.error('H5网页名称不能为空')
      return
    }
    
    if (!basicForm.category_id) {
      ElMessage.error('请选择分类')
      return
    }
    
    // 验证域名配置
    for (let i = 0; i < domainLinkGroups.value.length; i++) {
      const group = domainLinkGroups.value[i]
      
      if (!group.domain_type?.trim()) {
        ElMessage.error(`第${i + 1}个域名配置的域名类型不能为空`)
        return
      }
      
      if (!group.test_domain?.trim()) {
        ElMessage.error(`第${i + 1}个域名配置的测试域名不能为空`)
        return
      }
      
      if (!group.prod_domain?.trim()) {
        ElMessage.error(`第${i + 1}个域名配置的正式域名不能为空`)
        return
      }
      
      if (!group.first_level?.trim()) {
        ElMessage.error(`第${i + 1}个域名配置的一级目录不能为空`)
        return
      }
      
      if (!group.second_level?.trim()) {
        ElMessage.error(`第${i + 1}个域名配置的二级目录不能为空`)
        return
      }
    }
    
    // 验证链接数据
    for (let i = 0; i < domainLinkGroups.value.length; i++) {
      const group = domainLinkGroups.value[i]
      
      for (let j = 0; j < group.links.length; j++) {
        const link = group.links[j]
        
        if (!link.title?.trim()) {
          ElMessage.error(`第${i + 1}个域名配置的第${j + 1}个链接标题不能为空`)
          return
        }
        
        if (!link.url?.trim()) {
          ElMessage.error(`第${i + 1}个域名配置的第${j + 1}个链接URL不能为空`)
          return
        }
        
        if (!link.domain_type?.trim()) {
          ElMessage.error(`第${i + 1}个域名配置的第${j + 1}个链接域名类型不能为空`)
          return
        }
      }
    }
    
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

// 处理页面滚动
const handlePageScroll = () => {
  const scrollTop = window.pageYOffset || document.documentElement.scrollTop
  isHeaderFixed.value = scrollTop > 100
}

// 批量导入相关方法
const openBatchImportDialog = (groupIndex) => {
  // 校验基本信息
  if (!basicForm.name?.trim()) {
    ElMessage.error('请先填写H5网页名称')
    return
  }
  
  if (!basicForm.category_id) {
    ElMessage.error('请先选择分类')
    return
  }
  
  // 校验当前组的域名配置
  const group = domainLinkGroups.value[groupIndex]
  if (!group) {
    ElMessage.error('未找到对应的域名配置组')
    return
  }
  
  if (!group.domain_type?.trim()) {
    ElMessage.error('请先填写域名类型')
    return
  }
  
  if (!group.test_domain?.trim()) {
    ElMessage.error('请先填写测试域名')
    return
  }
  
  if (!group.prod_domain?.trim()) {
    ElMessage.error('请先填写正式域名')
    return
  }
  
  if (!group.first_level?.trim()) {
    ElMessage.error('请先填写一级目录')
    return
  }
  
  if (!group.second_level?.trim()) {
    ElMessage.error('请先填写二级目录')
    return
  }
  
  // 所有校验通过，打开对话框
  currentImportGroupIndex.value = groupIndex
  batchImportText.value = ''
  parsedLinks.value = []
  hasImportErrors.value = false
  showBatchImportDialog.value = true
}

const parseBatchImportText = () => {
  const lines = batchImportText.value.trim().split('\n')
  const parsed = []
  let hasErrors = false
  
  // 获取当前组的域名配置
  const currentGroup = domainLinkGroups.value[currentImportGroupIndex.value]
  
  lines.forEach((line, index) => {
    const trimmedLine = line.trim()
    if (!trimmedLine) return
    
    // 查找第一个空格的位置
    const firstSpaceIndex = trimmedLine.indexOf(' ')
    if (firstSpaceIndex === -1) {
      parsed.push({
        title: '',
        url: trimmedLine,
        error: '格式错误：缺少标题和URL之间的空格'
      })
      hasErrors = true
      return
    }
    
    const title = trimmedLine.substring(0, firstSpaceIndex).trim()
    let url = trimmedLine.substring(firstSpaceIndex + 1).trim()
    
    if (!title) {
      parsed.push({
        title: '',
        url: url,
        error: '标题不能为空'
      })
      hasErrors = true
      return
    }
    
    if (!url) {
      parsed.push({
        title: title,
        url: '',
        error: 'URL不能为空'
      })
      hasErrors = true
      return
    }
    
    // 如果URL是完整URL（包含域名），尝试提取页面路径
    if (url.startsWith('http://') || url.startsWith('https://')) {
      const extractedPath = extractPagePath(url, currentGroup)
      if (extractedPath) {
        url = extractedPath
      } else {
        parsed.push({
          title: title,
          url: url,
          error: '无法从完整URL中提取页面路径，请检查域名配置'
        })
        hasErrors = true
        return
      }
    }
    
    // 简单的URL格式验证
    if (!url.startsWith('http://') && !url.startsWith('https://') && !url.startsWith('/')) {
      parsed.push({
        title: title,
        url: url,
        error: 'URL格式不正确，应以http://、https://或/开头'
      })
      hasErrors = true
      return
    }
    
    parsed.push({
      title: title,
      url: url,
      error: null
    })
  })
  
  parsedLinks.value = parsed
  hasImportErrors.value = hasErrors
}

// 从完整URL中提取页面路径
const extractPagePath = (fullUrl, group) => {
  if (!group) return null
  
  const testDomain = group.test_domain?.trim()
  const prodDomain = group.prod_domain?.trim()
  const firstLevel = group.first_level?.trim()
  const secondLevel = group.second_level?.trim()
  
  // 构建测试域名和正式域名的完整路径
  const testFullPath = testDomain ? `${testDomain}/${firstLevel}/${secondLevel}` : null
  const prodFullPath = prodDomain ? `${prodDomain}/${firstLevel}/${secondLevel}` : null
  
  // 尝试匹配测试域名
  if (testFullPath && fullUrl.startsWith(testFullPath)) {
    return fullUrl.substring(testFullPath.length)
  }
  
  // 尝试匹配正式域名
  if (prodFullPath && fullUrl.startsWith(prodFullPath)) {
    return fullUrl.substring(prodFullPath.length)
  }
  
  // 如果都不匹配，返回null
  return null
}

const confirmBatchImport = () => {
  if (currentImportGroupIndex.value === -1) {
    ElMessage.error('导入失败：未找到目标组')
    return
  }
  
  const group = domainLinkGroups.value[currentImportGroupIndex.value]
  const validLinks = parsedLinks.value.filter(link => !link.error)
  
  if (validLinks.length === 0) {
    ElMessage.error('没有有效的链接可以导入')
    return
  }
  
  // 添加链接到组
  validLinks.forEach((link, index) => {
    group.links.push({
      miniprogram_id: props.id,
      title: link.title,
      url: link.url,
      domain_type: group.domain_type || (domainTypes.value.length > 0 ? domainTypes.value[0].domain_type : 'default'),
      sort_order: group.links.length + index,
      status: 1,
      _isNew: true,
      _tempId: `temp_${++tempIdCounter}`
    })
  })
  
  ElMessage.success(`成功导入 ${validLinks.length} 个链接`)
  showBatchImportDialog.value = false
}

// 监听批量导入文本变化
watch(batchImportText, () => {
  parseBatchImportText()
})

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
  window.addEventListener('scroll', handlePageScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handlePageScroll)
})
</script>

<style scoped>
.edit-page {
  max-width: 1200px;
  margin: 0 auto;
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
  font-size: 18px;
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
  transition: margin-top 0.3s ease;
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

.links-actions {
  display: flex;
  gap: 10px;
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

/* 必填字段样式 */
:deep(.el-form-item.is-required .el-form-item__label::before) {
  content: '*';
  color: #f56c6c;
  margin-right: 4px;
}

/* 表格必填字段标题样式 */
.el-table .el-table__header th {
  position: relative;
}

.el-table .el-table__header th[data-required="true"]::after {
  content: ' *';
  color: #f56c6c;
  font-weight: bold;
}

/* 批量导入对话框样式 */
.batch-import-content {
  display: flex;
  flex-direction: column;
  gap: 15px;
  max-height: 70vh;
  overflow: hidden;
}

.import-instructions {
  background: #f8f9fa;
  padding: 12px;
  border-radius: 6px;
  border-left: 4px solid #409eff;
  flex-shrink: 0;
  overflow-x: auto;
}

.import-instructions p {
  margin: 3px 0;
  color: #606266;
  font-size: 13px;
}

.examples-container {
  display: flex;
  gap: 20px;
  margin-top: 8px;
  overflow-x: auto;
  padding-bottom: 5px;
}

.example-section {
  flex: 1;
  min-width: 300px;
  flex-shrink: 0;
}

.example-section p {
  margin: 0 0 5px 0;
  font-size: 12px;
  color: #303133;
}

.example-section pre {
  white-space: pre-wrap;
  word-break: break-all;
  overflow-x: auto;
}

.import-textarea {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.import-textarea .el-textarea {
  flex: 1;
  overflow: hidden;
}

.import-textarea .el-textarea__inner {
  height: 100% !important;
  resize: vertical;
}

/* 批量导入对话框样式 */
:deep(.batch-import-dialog .el-dialog__body) {
  max-height: 70vh;
  overflow: hidden;
}

/* 固定头部样式 */
.fixed-header {
  background: #fff;
  border-bottom: 1px solid #e4e7ed;
  padding: 12px 0;
  margin-bottom: 20px;
  transition: all 0.3s ease;
}

.fixed-header.fixed {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 8px 20px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

.header-left h2 {
  margin: 0;
  font-size: 18px;
  color: #303133;
}

.header-subtitle {
  margin: 5px 0 0 0;
  font-size: 14px;
  color: #909399;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

/* 当头部固定时，给内容区域添加顶部边距 */
.fixed-header.fixed + .content-area {
  margin-top: 80px;
}

.import-instructions code {
  background: #e1f5fe;
  padding: 2px 4px;
  border-radius: 3px;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 12px;
}

.import-instructions pre {
  background: #f5f5f5;
  padding: 8px;
  margin: 5px 0;
  font-size: 12px;
  border-radius: 4px;
  border-radius: 4px;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 12px;
  line-height: 1.4;
  margin: 10px 0 0 0;
  overflow-x: auto;
}

.import-textarea {
  margin-bottom: 10px;
}

.import-preview {
  border-top: 1px solid #ebeef5;
  padding-top: 15px;
}

.import-preview h4 {
  margin: 0 0 10px 0;
  color: #303133;
  font-size: 14px;
}

.preview-list {
  max-height: 200px;
  overflow-y: auto;
  border: 1px solid #ebeef5;
  border-radius: 4px;
}

.preview-item {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  border-bottom: 1px solid #f0f0f0;
  font-size: 12px;
}

.preview-item:last-child {
  border-bottom: none;
}

.preview-item.preview-error {
  background: #fef0f0;
  color: #f56c6c;
}

.preview-index {
  width: 30px;
  color: #909399;
  font-weight: 500;
}

.preview-title {
  width: 120px;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.preview-url {
  flex: 1;
  color: #606266;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
}

.preview-error-msg {
  color: #f56c6c;
  font-size: 11px;
  margin-left: 10px;
}
</style> 