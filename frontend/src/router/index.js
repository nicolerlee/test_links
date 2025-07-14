import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/manage'
  },
  {
    path: '/manage',
    name: 'Manage',
    component: () => import('../views/ManagePage.vue'),
    meta: {
      title: '小程序管理'
    }
  },
  {
    path: '/edit/:id',
    name: 'Edit',
    component: () => import('../views/EditPage.vue'),
    meta: {
      title: '编辑小程序'
    },
    props: true
  },
  {
    path: '/view/:id',
    name: 'View',
    component: () => import('../views/ViewPage.vue'),
    meta: {
      title: '查看小程序'
    },
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  if (to.meta.title) {
    document.title = `${to.meta.title} - 小程序管理系统`
  }
  next()
})

export default router 