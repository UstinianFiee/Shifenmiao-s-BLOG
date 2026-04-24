import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  // 前台
  {
    path: '/',
    component: () => import('../layouts/FrontLayout.vue'),
    children: [
      { path: '', name: 'Home', component: () => import('../views/front/Home.vue') },
      { path: 'article/:id', name: 'Article', component: () => import('../views/front/Article.vue') },
      { path: 'category/:id', name: 'Category', component: () => import('../views/front/CategoryPage.vue') },
      { path: 'tag/:id', name: 'Tag', component: () => import('../views/front/TagPage.vue') },
      { path: 'timeline', name: 'Timeline', component: () => import('../views/front/Timeline.vue') },
      { path: 'about', name: 'About', component: () => import('../views/front/About.vue') },
    ]
  },
  // 后台
  { path: '/admin/login', name: 'Login', component: () => import('../views/admin/Login.vue') },
  {
    path: '/admin',
    component: () => import('../layouts/AdminLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: '', redirect: '/admin/articles' },
      { path: 'articles', name: 'AdminArticles', component: () => import('../views/admin/Articles.vue') },
      { path: 'articles/new', name: 'ArticleNew', component: () => import('../views/admin/ArticleEdit.vue') },
      { path: 'articles/:id/edit', name: 'ArticleEdit', component: () => import('../views/admin/ArticleEdit.vue') },
      { path: 'categories', name: 'AdminCategories', component: () => import('../views/admin/Categories.vue') },
      { path: 'tags', name: 'AdminTags', component: () => import('../views/admin/Tags.vue') },
      { path: 'media', name: 'AdminMedia', component: () => import('../views/admin/Media.vue') },
      { path: 'ai', name: 'AdminAi', component: () => import('../views/admin/AiAnalysis.vue') },
      { path: 'account', name: 'AdminAccount', component: () => import('../views/admin/Account.vue') },
    ]
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.token) {
    return '/admin/login'
  }
})

export default router
