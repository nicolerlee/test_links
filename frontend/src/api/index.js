import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

// 分类API
export const categoryAPI = {
  // 获取所有分类
  getCategories: () => api.get('/categories'),
  
  // 获取单个分类及其小程序
  getCategory: (categoryId) => api.get(`/categories/${categoryId}`),
  
  // 创建分类
  createCategory: (data) => api.post('/categories', data),
  
  // 更新分类
  updateCategory: (categoryId, data) => api.put(`/categories/${categoryId}`, data),
  
  // 删除分类
  deleteCategory: (categoryId) => api.delete(`/categories/${categoryId}`),
}

// 小程序API
export const miniprogramAPI = {
  // 获取所有小程序
  getMiniprograms: () => api.get('/miniprograms'),
  
  // 获取单个小程序
  getMiniprogram: (miniprogramId) => api.get(`/miniprograms/${miniprogramId}`),
  
  // 根据分类获取小程序
  getMiniprogramsByCategory: (categoryId) => api.get(`/miniprograms/category/${categoryId}`),
  
  // 创建小程序
  createMiniprogram: (data) => api.post('/miniprograms', data),
  
  // 更新小程序
  updateMiniprogram: (miniprogramId, data) => api.put(`/miniprograms/${miniprogramId}`, data),
  
  // 删除小程序
  deleteMiniprogram: (miniprogramId) => api.delete(`/miniprograms/${miniprogramId}`),
}

// 域名配置API
export const domainConfigAPI = {
  // 获取小程序的所有域名配置
  getDomainConfigsByMiniprogram: (miniprogramId) => 
    api.get(`/domain-configs/miniprogram/${miniprogramId}`),
  
  // 获取单个域名配置
  getDomainConfig: (configId) => api.get(`/domain-configs/${configId}`),
  
  // 创建域名配置
  createDomainConfig: (data) => api.post('/domain-configs', data),
  
  // 更新域名配置
  updateDomainConfig: (configId, data) => api.put(`/domain-configs/${configId}`, data),
  
  // 删除域名配置
  deleteDomainConfig: (configId) => api.delete(`/domain-configs/${configId}`),
}

// 链接API
export const linkAPI = {
  // 获取小程序的所有链接
  getLinksByMiniprogram: (miniprogramId) => 
    api.get(`/links/miniprogram/${miniprogramId}`),
  
  // 获取单个链接
  getLink: (linkId) => api.get(`/links/${linkId}`),
  
  // 创建链接
  createLink: (data) => api.post('/links', data),
  
  // 更新链接
  updateLink: (linkId, data) => api.put(`/links/${linkId}`, data),
  
  // 删除链接
  deleteLink: (linkId) => api.delete(`/links/${linkId}`),
}

export default api 