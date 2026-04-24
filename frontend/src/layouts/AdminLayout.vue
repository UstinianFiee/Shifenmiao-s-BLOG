<template>
  <div class="admin-layout">
    <header class="admin-header">
      <div class="header-left">
        <!-- 桌面端折叠按钮 / 移动端汉堡 -->
        <button class="collapse-btn" @click="toggleSidebar">
          <span class="hamburger-icon" :class="{ open: mobileMenuOpen }">
            <span></span><span></span><span></span>
          </span>
        </button>
        <span class="header-logo">时分渺<span class="logo-ovo">OvO</span></span>
      </div>
      <div class="header-right">
        <a href="/" target="_blank" class="front-link">🌐 前台</a>
        <button class="theme-btn" @click="themeStore.toggle()">{{ themeStore.theme === 'dark' ? '☀️' : '🌙' }}</button>
        <span class="admin-user">{{ auth.username }}</span>
        <button class="btn btn-danger" style="padding:4px 10px;font-size:12px" @click="logout">退出</button>
      </div>
    </header>

    <div class="admin-body">
      <!-- 移动端遮罩 -->
      <div class="sidebar-mask" v-if="mobileMenuOpen" @click="mobileMenuOpen = false"></div>

      <aside class="sidebar" :class="{ collapsed, 'mobile-open': mobileMenuOpen }">
        <nav class="sidebar-nav">
          <router-link to="/admin/articles" class="nav-item" @click="closeMobile">
            <span class="nav-icon">📝</span><span class="nav-text">文章管理</span>
          </router-link>
          <router-link to="/admin/categories" class="nav-item" @click="closeMobile">
            <span class="nav-icon">📁</span><span class="nav-text">分类管理</span>
          </router-link>
          <router-link to="/admin/tags" class="nav-item" @click="closeMobile">
            <span class="nav-icon">🏷️</span><span class="nav-text">标签管理</span>
          </router-link>
          <router-link to="/admin/media" class="nav-item" @click="closeMobile">
            <span class="nav-icon">🖼️</span><span class="nav-text">媒体库</span>
          </router-link>
          <router-link to="/admin/ai" class="nav-item" @click="closeMobile">
            <span class="nav-icon">🤖</span><span class="nav-text">AI 助手</span>
          </router-link>
          <router-link to="/admin/account" class="nav-item" @click="closeMobile">
            <span class="nav-icon">⚙️</span><span class="nav-text">账号设置</span>
          </router-link>
        </nav>
      </aside>

      <main class="admin-main" :class="{ collapsed }">
        <div class="breadcrumb">
          <span>首页</span><span class="sep">/</span><span class="current">{{ currentTitle }}</span>
        </div>
        <div class="main-content">
          <router-view />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useThemeStore } from '../stores/theme'

const auth = useAuthStore()
const themeStore = useThemeStore()
const router = useRouter()
const route = useRoute()
const collapsed = ref(false)
const mobileMenuOpen = ref(false)
const isMobile = () => window.innerWidth <= 768

function toggleSidebar() {
  if (isMobile()) {
    mobileMenuOpen.value = !mobileMenuOpen.value
  } else {
    collapsed.value = !collapsed.value
  }
}

function closeMobile() {
  if (isMobile()) mobileMenuOpen.value = false
}

const titleMap = { '/admin/articles': '文章管理', '/admin/articles/new': '新建文章', '/admin/categories': '分类管理', '/admin/tags': '标签管理', '/admin/media': '媒体库', '/admin/ai': 'AI 助手', '/admin/account': '账号设置' }
const currentTitle = computed(() => route.path.includes('/edit') ? '编辑文章' : (titleMap[route.path] || '管理后台'))

function logout() { auth.logout(); router.push('/admin/login') }
</script>

<style scoped>
.admin-layout { display: flex; flex-direction: column; min-height: 100vh; background: var(--bg-primary); }

.admin-header {
  height: 56px; flex-shrink: 0;
  background: var(--bg-card); border-bottom: 1px solid var(--border);
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 16px;
  position: fixed; top: 0; left: 0; right: 0; z-index: 200;
  box-shadow: var(--shadow);
}
.header-left { display: flex; align-items: center; gap: 12px; }
.header-logo { font-size: 15px; font-weight: 700; color: var(--text-primary); }
.logo-ovo { color: var(--accent); }

/* 汉堡按钮 */
.collapse-btn { background: none; border: none; cursor: pointer; padding: 6px; display: flex; align-items: center; }
.hamburger-icon { display: flex; flex-direction: column; gap: 5px; }
.hamburger-icon span { display: block; width: 20px; height: 2px; background: var(--text-secondary); border-radius: 2px; transition: all 0.3s; }
.hamburger-icon.open span:nth-child(1) { transform: translateY(7px) rotate(45deg); }
.hamburger-icon.open span:nth-child(2) { opacity: 0; }
.hamburger-icon.open span:nth-child(3) { transform: translateY(-7px) rotate(-45deg); }

.header-right { display: flex; align-items: center; gap: 8px; }
.admin-user { font-size: 13px; color: var(--text-secondary); }
.theme-btn { background: none; border: 1px solid var(--border); border-radius: 50%; width: 30px; height: 30px; cursor: pointer; font-size: 13px; display: flex; align-items: center; justify-content: center; transition: all 0.2s; }
.theme-btn:hover { border-color: var(--accent); }
.front-link { display: flex; align-items: center; gap: 4px; font-size: 12px; color: var(--text-secondary); padding: 4px 10px; border-radius: 20px; border: 1px solid var(--border); transition: all 0.2s; white-space: nowrap; }
.front-link:hover { border-color: var(--accent); color: var(--accent); }

.admin-body { display: flex; margin-top: 56px; min-height: calc(100vh - 56px); }

/* 遮罩 */
.sidebar-mask { display: none; position: fixed; inset: 56px 0 0 0; background: rgba(0,0,0,0.5); z-index: 99; }

.sidebar {
  width: 200px; flex-shrink: 0;
  background: var(--bg-secondary); border-right: 1px solid var(--border);
  position: fixed; top: 56px; left: 0; bottom: 0;
  overflow: hidden; transition: width 0.25s ease, transform 0.25s ease; z-index: 100;
}
.sidebar.collapsed { width: 52px; }
.sidebar-nav { padding: 12px 8px; display: flex; flex-direction: column; gap: 4px; }
.nav-item { display: flex; align-items: center; gap: 10px; padding: 10px 12px; border-radius: var(--radius); color: var(--text-secondary); font-size: 14px; white-space: nowrap; overflow: hidden; transition: all 0.2s; }
.nav-item:hover { background: var(--bg-card-hover); color: var(--text-primary); }
.nav-item.router-link-active { background: rgba(37,99,235,0.12); color: var(--accent); border-left: 3px solid var(--accent); }
[data-theme="dark"] .nav-item.router-link-active { background: rgba(79,195,247,0.1); }
.nav-icon { font-size: 16px; flex-shrink: 0; }
.nav-text { transition: opacity 0.2s; }
.collapsed .nav-text { opacity: 0; pointer-events: none; }

.admin-main { margin-left: 200px; flex: 1; padding: 20px; transition: margin-left 0.25s ease; }
.admin-main.collapsed { margin-left: 52px; }
.breadcrumb { font-size: 13px; color: var(--text-muted); margin-bottom: 16px; display: flex; align-items: center; gap: 6px; }
.sep { color: var(--border-glow); }
.current { color: var(--text-secondary); }
.main-content { background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius); padding: 24px; min-height: calc(100vh - 56px - 80px); max-width: 1200px; margin: 0 auto; }

/* 移动端 */
@media (max-width: 768px) {
  .admin-user { display: none; }
  .front-link { display: none; }

  /* 侧边栏默认隐藏，滑入显示 */
  .sidebar { transform: translateX(-100%); width: 200px !important; }
  .sidebar.mobile-open { transform: translateX(0); }
  .sidebar-mask { display: block; }

  .admin-main { margin-left: 0 !important; padding: 12px; }
  .main-content { padding: 16px; }
}
</style>
