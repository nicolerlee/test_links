<template>
  <div class="manage-page">
    <div class="page-header">
      <h2>小程序管理</h2>
      <div class="header-actions">
        <el-dropdown @command="handleCommand">
          <el-button type="info">
            <el-icon><Setting /></el-icon>
            设置
            <el-icon class="el-icon--right"><arrow-down /></el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="new">
                <el-icon><Plus /></el-icon>
                新建小程序
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>

    <div class="content-area">
      <el-tabs v-model="activeTab" type="card" class="category-tabs">
        <el-tab-pane
          v-for="category in categories"
          :key="category.id"
          :label="category.name"
          :name="category.id"
        >
          <template #label>
            <div class="tab-label" @mouseenter="showDeleteButton(category.id)" @mouseleave="hideDeleteButton(category.id)">
              <span>{{ category.name }}</span>
              <el-button
                v-if="hoveredCategory === category.id"
                @click.stop="deleteCategory(category)"
                type="danger"
                size="small"
                :icon="Delete"
                circle
                class="delete-category-btn"
              />
            </div>
          </template>
          
          <div class="miniprogram-grid">
            <el-card
              v-for="miniprogram in category.miniprograms"
              :key="miniprogram.id"
              class="miniprogram-card"
              shadow="hover"
            >
              <template #header>
                <div class="card-header">
                  <span class="miniprogram-name">{{ miniprogram.name }}</span>
                  <div class="card-actions">
                    <el-button
                      type="primary"
                      size="small"
                      @click="viewMiniprogram(miniprogram.id)"
                    >
                      <el-icon><View /></el-icon>
                      查看
                    </el-button>
                    <el-button
                      type="warning"
                      size="small"
                      @click="editMiniprogram(miniprogram.id)"
                    >
                      <el-icon><Edit /></el-icon>
                      编辑
                    </el-button>
                    <el-button
                      type="danger"
                      size="small"
                      @click="deleteMiniprogram(miniprogram)"
                    >
                      <el-icon><Delete /></el-icon>
                      删除
                    </el-button>
                  </div>
                </div>
              </template>
              
              <div class="miniprogram-info">
                <p class="description">{{ miniprogram.description || '暂无描述' }}</p>
                <div class="stats">
                  <el-tag size="small" type="info">
                    域名配置: {{ miniprogram.domain_configs?.length || 0 }}
                  </el-tag>
                  <el-tag size="small" type="success">
                    链接数量: {{ miniprogram.links?.length || 0 }}
                  </el-tag>
                </div>
              </div>
            </el-card>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>

    <!-- 新建小程序对话框 -->
    <el-dialog
      v-model="newMiniprogramVisible"
      title="新建小程序"
      width="500px"
      @close="resetNewForm"
    >
      <el-form
        ref="newFormRef"
        :model="newForm"
        :rules="formRules"
        label-width="100px"
      >
        <el-form-item label="小程序ID" prop="id">
          <el-input v-model="newForm.id" placeholder="请输入小程序ID" />
        </el-form-item>
        <el-form-item label="小程序名称" prop="name">
          <el-input v-model="newForm.name" placeholder="请输入小程序名称" />
        </el-form-item>
        <el-form-item label="分类" prop="category_id">
          <el-select
            v-model="newForm.category_id"
            placeholder="请选择分类"
            style="width: 100%"
            @change="handleCategoryChange"
          >
            <el-option
              label="-- 选择已有分类 --"
              value=""
              disabled
            />
            <el-option
              v-for="category in categories"
              :key="category.id"
              :label="category.name"
              :value="category.id"
            />
            <el-option
              label="+ 新建分类"
              value="__create_new__"
              style="color: #67c23a; font-weight: bold;"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="newForm.description"
            type="textarea"
            placeholder="请输入小程序描述"
            :rows="3"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="newMiniprogramVisible = false">取消</el-button>
        <el-button type="primary" @click="createMiniprogram" :loading="creating">
          确定
        </el-button>
      </template>
    </el-dialog>

    <!-- 新建分类对话框 -->
    <el-dialog
      v-model="newCategoryVisible"
      title="新建分类"
      width="400px"
      @close="resetCategoryForm"
    >
      <el-form
        ref="categoryFormRef"
        :model="categoryForm"
        :rules="categoryRules"
        label-width="80px"
      >
        <el-form-item label="分类ID" prop="id">
          <el-input v-model="categoryForm.id" placeholder="请输入分类ID" />
        </el-form-item>
        <el-form-item label="分类名称" prop="name">
          <el-input v-model="categoryForm.name" placeholder="请输入分类名称" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="categoryForm.description"
            type="textarea"
            placeholder="请输入分类描述"
            :rows="2"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="newCategoryVisible = false">取消</el-button>
        <el-button type="primary" @click="createCategory" :loading="creatingCategory">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Setting,
  Plus,
  ArrowDown,
  View,
  Edit,
  Delete
} from '@element-plus/icons-vue'
import { categoryAPI, miniprogramAPI } from '@/api'

const router = useRouter()

// 响应式数据
const categories = ref([])
const activeTab = ref('')
const loading = ref(false)

// 新建小程序相关
const newMiniprogramVisible = ref(false)
const creating = ref(false)
const newFormRef = ref()
const newForm = reactive({
  id: '',
  name: '',
  category_id: '',
  description: ''
})

// 新建分类相关
const newCategoryVisible = ref(false)
const creatingCategory = ref(false)
const categoryFormRef = ref()
const categoryForm = reactive({
  id: '',
  name: '',
  description: ''
})

// 删除分类相关
const hoveredCategory = ref('')

// 表单验证规则
const formRules = {
  id: [
    { required: true, message: '请输入小程序ID', trigger: 'blur' },
    { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' }
  ],
  name: [
    { required: true, message: '请输入小程序名称', trigger: 'blur' },
    { min: 2, max: 200, message: '长度在 2 到 200 个字符', trigger: 'blur' }
  ],
  category_id: [
    { required: true, message: '请选择分类', trigger: 'change' }
  ]
}

const categoryRules = {
  id: [
    { required: true, message: '请输入分类ID', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  name: [
    { required: true, message: '请输入分类名称', trigger: 'blur' },
    { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' }
  ]
}

// 方法
const loadCategories = async () => {
  try {
    loading.value = true
    const data = await categoryAPI.getCategories()
    
    // 加载每个分类的小程序
    for (const category of data) {
      const categoryDetail = await categoryAPI.getCategory(category.id)
      category.miniprograms = categoryDetail.miniprograms || []
    }
    
    categories.value = data
    if (data.length > 0) {
      // 尝试从 sessionStorage 恢复 activeTab
      const savedTab = sessionStorage.getItem('managePageActiveTab');
      if (savedTab && data.some(cat => cat.id === savedTab)) {
        activeTab.value = savedTab;
      } else {
        activeTab.value = data[0].id
      }
    }
  } catch (error) {
    ElMessage.error('加载分类失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

// 监听 activeTab 的变化并保存到 sessionStorage
watch(activeTab, (newTab) => {
  if (newTab) {
    sessionStorage.setItem('managePageActiveTab', newTab);
  }
});

const handleCommand = (command) => {
  if (command === 'new') {
    newMiniprogramVisible.value = true
  }
}

const handleCategoryChange = async (value) => {
  // 如果选择的是"新建分类"选项
  if (value === '__create_new__') {
    // 重置分类表单
    categoryForm.id = ''
    categoryForm.name = ''
    categoryForm.description = ''
    
    // 显示新建分类对话框
    newCategoryVisible.value = true
    
    // 清空当前选择，等待用户创建完成
    newForm.category_id = ''
  }
}

const createCategory = async () => {
  try {
    await categoryFormRef.value.validate()
    creatingCategory.value = true
    
    await categoryAPI.createCategory(categoryForm)
    ElMessage.success('分类创建成功')
    
    newCategoryVisible.value = false
    await loadCategories()
    
    // 设置新创建的分类为选中分类
    newForm.category_id = categoryForm.id
  } catch (error) {
    if (error.response?.status === 400) {
      ElMessage.error('分类ID已存在')
    } else {
      ElMessage.error('创建分类失败')
    }
    console.error(error)
  } finally {
    creatingCategory.value = false
  }
}

const createMiniprogram = async () => {
  try {
    await newFormRef.value.validate()
    creating.value = true
    
    await miniprogramAPI.createMiniprogram(newForm)
    ElMessage.success('小程序创建成功')
    
    newMiniprogramVisible.value = false
    await loadCategories()
  } catch (error) {
    if (error.response?.status === 400) {
      ElMessage.error(error.response.data.detail || '小程序创建失败')
    } else {
      ElMessage.error('创建小程序失败')
    }
    console.error(error)
  } finally {
    creating.value = false
  }
}

const viewMiniprogram = (id) => {
  router.push(`/view/${id}`)
}

const editMiniprogram = (id) => {
  router.push(`/edit/${id}`)
}

const deleteMiniprogram = async (miniprogram) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除小程序 "${miniprogram.name}" 吗？此操作不可恢复。`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    await miniprogramAPI.deleteMiniprogram(miniprogram.id)
    ElMessage.success('删除成功')
    await loadCategories()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
      console.error(error)
    }
  }
}

const deleteCategory = async (category) => {
  try {
    const miniprogramCount = category.miniprograms?.length || 0
    
    let confirmMessage = ''
    let confirmTitle = '确认删除'
    
    if (miniprogramCount > 0) {
      confirmMessage = `分类 "${category.name}" 下还有 ${miniprogramCount} 个小程序。删除分类后，这些小程序也将被删除。\n\n确定要删除吗？此操作不可恢复。`
      confirmTitle = '警告：分类下有小程序'
    } else {
      confirmMessage = `确定要删除分类 "${category.name}" 吗？\n\n删除分类后，该分类下的所有小程序也会一并删除。此操作不可恢复。`
    }
    
    await ElMessageBox.confirm(
      confirmMessage,
      confirmTitle,
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning',
        dangerouslyUseHTMLString: false,
      }
    )

    await categoryAPI.deleteCategory(category.id)
    ElMessage.success('分类删除成功')
    await loadCategories()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
      console.error(error)
    }
  }
}

const showDeleteButton = (categoryId) => {
  hoveredCategory.value = categoryId
}

const hideDeleteButton = (categoryId) => {
  hoveredCategory.value = ''
}

const resetNewForm = () => {
  Object.assign(newForm, {
    id: '',
    name: '',
    category_id: '',
    description: ''
  })
  newFormRef.value?.resetFields()
}

const resetCategoryForm = () => {
  Object.assign(categoryForm, {
    id: '',
    name: '',
    description: ''
  })
  categoryFormRef.value?.resetFields()
}

// 生命周期
onMounted(() => {
  loadCategories()
})
</script>

<style scoped>
.manage-page {
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

.page-header h2 {
  margin: 0;
  color: #303133;
  font-weight: 600;
}

.content-area {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.08);
}

.category-tabs {
  min-height: 400px;
}

.miniprogram-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.miniprogram-card {
  transition: transform 0.2s;
}

.miniprogram-card:hover {
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.miniprogram-name {
  font-weight: 600;
  color: #303133;
  font-size: 16px;
}

.card-actions {
  display: flex;
  gap: 5px;
}

.miniprogram-info {
  padding: 10px 0;
}

.description {
  color: #606266;
  margin: 0 0 15px 0;
  line-height: 1.5;
  min-height: 24px;
}

.stats {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
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

:deep(.el-tabs__header) {
  margin-bottom: 0;
}

:deep(.el-tabs__content) {
  padding-top: 0;
}

.tab-label {
  display: flex;
  align-items: center;
  gap: 8px;
  position: relative;
}

.delete-category-btn {
  margin-left: 8px;
  width: 20px;
  height: 20px;
  padding: 0;
  opacity: 0.8;
  transition: opacity 0.2s;
}

.delete-category-btn:hover {
  opacity: 1;
}

.tab-label:hover .delete-category-btn {
  opacity: 1;
}

/* 确保标签内容不会因为删除按钮而换行 */
:deep(.el-tabs__item) {
  white-space: nowrap;
}

:deep(.el-tabs__nav-wrap) {
  overflow: visible;
}
</style> 