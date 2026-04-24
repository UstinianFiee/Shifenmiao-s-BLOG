<template>
  <nav class="navbar" :class="{ scrolled }">
    <div class="container nav-inner">
      <router-link to="/" class="logo">时分渺<span class="logo-ovo">OvO</span></router-link>

      <!-- 桌面端导航 -->
      <ul class="nav-links">
        <li><router-link to="/">首页</router-link></li>
        <li><router-link to="/timeline">时间轴</router-link></li>
        <li><router-link to="/about">关于</router-link></li>
      </ul>

      <!-- 桌面端右侧工具栏 -->
      <div class="nav-right">
        <div class="search-wrap">
          <input v-model="keyword" class="search-input" placeholder="搜索文章..." @keyup.enter="doSearch" />
          <span class="search-icon">&#128269;</span>
        </div>
        <div class="cat-wrap">
          <button class="cat-btn" @click="catOpen = !catOpen">
            {{ activeCatName }}<span class="arrow" :class="{ open: catOpen }">&#9662;</span>
          </button>
          <div class="cat-dropdown" v-show="catOpen">
            <div class="cat-item" :class="{ active: !activeCategory }" @click="selectCat(null)">全部</div>
            <div v-for="c in categories" :key="c.id" class="cat-item" :class="{ active: activeCategory === c.id }" @click="selectCat(c.id)">{{ c.name }}</div>
          </div>
        </div>
        <button class="theme-btn" @click="themeStore.toggle()">
          <span class="theme-icon">{{ isDark ? '◑' : '◐' }}</span>
        </button>
        <router-link to="/admin" class="admin-btn" title="管理后台">
          <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/>
          </svg>
        </router-link>
      </div>

      <!-- 移动端右侧 -->
      <div class="mobile-right">
        <button class="theme-btn" @click="themeStore.toggle()">
          <span class="theme-icon">{{ isDark ? '◑' : '◐' }}</span>
        </button>
        <button class="hamburger" @click="mobileOpen = !mobileOpen" :class="{ open: mobileOpen }">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>

    <!-- 移动端抽屉菜单 -->
    <div class="mobile-menu" :class="{ open: mobileOpen }" @click.self="mobileOpen = false">
      <div class="mobile-menu-inner">
        <div class="mobile-search">
          <input v-model="keyword" class="search-input" placeholder="搜索文章..." @keyup.enter="doSearchMobile" />
        </div>
        <ul class="mobile-nav-links">
          <li><router-link to="/" @click="mobileOpen = false">首页</router-link></li>
          <li><router-link to="/timeline" @click="mobileOpen = false">时间轴</router-link></li>
          <li><router-link to="/about" @click="mobileOpen = false">关于</router-link></li>
          <li><router-link to="/admin" @click="mobileOpen = false">管理后台</router-link></li>
        </ul>
        <div class="mobile-cats">
          <p class="mobile-cat-title">分类筛选</p>
          <div class="mobile-cat-list">
            <span class="cat-tag" :class="{ active: !activeCategory }" @click="selectCatMobile(null)">全部</span>
            <span v-for="c in categories" :key="c.id" class="cat-tag" :class="{ active: activeCategory === c.id }" @click="selectCatMobile(c.id)">{{ c.name }}</span>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useThemeStore } from '../../stores/theme'
import api from '../../api'

const themeStore = useThemeStore()
const router = useRouter()
const isDark = computed(() => themeStore.theme === 'dark')
const scrolled = ref(false)
const mobileOpen = ref(false)
const onScroll = () => { scrolled.value = window.scrollY > 40 }

const keyword = ref('')
function doSearch() {
  if (!keyword.value.trim()) return
  router.push({ path: '/', query: { keyword: keyword.value.trim() } })
  keyword.value = ''
}
function doSearchMobile() {
  doSearch()
  mobileOpen.value = false
}

const categories = ref([])
const activeCategory = ref(null)
const catOpen = ref(false)
const activeCatName = computed(() => {
  if (!activeCategory.value) return '分类'
  return categories.value.find(c => c.id === activeCategory.value)?.name || '分类'
})
function selectCat(id) {
  activeCategory.value = id
  catOpen.value = false
  router.push({ path: '/', query: id ? { category_id: id } : {} })
}
function selectCatMobile(id) {
  activeCategory.value = id
  mobileOpen.value = false
  router.push({ path: '/', query: id ? { category_id: id } : {} })
}
function onClickOutside(e) {
  if (!e.target.closest('.cat-wrap')) catOpen.value = false
}

onMounted(() => {
  window.addEventListener('scroll', onScroll)
  document.addEventListener('click', onClickOutside)
  api.get('/categories').then(r => { categories.value = r.data })
})
onUnmounted(() => {
  window.removeEventListener('scroll', onScroll)
  document.removeEventListener('click', onClickOutside)
})
</script>

<style scoped>
.navbar { position: fixed; top: 0; left: 0; right: 0; z-index: 100; padding: 12px 0; transition: background 0.3s, backdrop-filter 0.3s, box-shadow 0.3s; }
.navbar.scrolled { background: var(--navbar-bg); backdrop-filter: blur(12px); border-bottom: 1px solid var(--border); box-shadow: var(--shadow); }
.nav-inner { display: flex; align-items: center; position: relative; }
.logo { font-size: 18px; font-weight: 700; color: var(--text-primary); transition: color 0.3s; flex-shrink: 0; margin-right: 32px; }
.logo:hover { color: var(--accent); }
.logo-ovo { color: var(--accent); }

/* 桌面端 */
.nav-links { display: flex; gap: 28px; list-style: none; position: absolute; left: 50%; transform: translateX(-50%); }
.nav-links a { color: var(--text-secondary); font-size: 14px; transition: color 0.3s; position: relative; padding-bottom: 2px; white-space: nowrap; }
.nav-links a::after { content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 1px; background: var(--accent); transform: scaleX(0); transition: transform 0.3s; }
.nav-links a:hover::after, .nav-links a.router-link-active::after { transform: scaleX(1); }
.nav-links a:hover, .nav-links a.router-link-active { color: var(--accent); }
.nav-right { display: flex; align-items: center; gap: 10px; margin-left: auto; flex-shrink: 0; }
.search-wrap { position: relative; }
.search-input { width: 150px; padding: 6px 28px 6px 12px; background: var(--bg-card); border: 1px solid var(--border); border-radius: 20px; color: var(--text-primary); font-size: 13px; outline: none; transition: all 0.3s; }
.search-input:focus { border-color: var(--accent); width: 190px; box-shadow: 0 0 8px var(--accent-glow); }
.search-icon { position: absolute; right: 10px; top: 50%; transform: translateY(-50%); font-size: 12px; pointer-events: none; color: var(--text-muted); }
.cat-wrap { position: relative; }
.cat-btn { display: flex; align-items: center; gap: 4px; padding: 6px 12px; border-radius: 20px; background: var(--bg-card); border: 1px solid var(--border); color: var(--text-secondary); font-size: 13px; cursor: pointer; transition: all 0.3s; white-space: nowrap; }
.cat-btn:hover { border-color: var(--accent); color: var(--accent); }
.arrow { font-size: 10px; transition: transform 0.3s; display: inline-block; }
.arrow.open { transform: rotate(180deg); }
.cat-dropdown { position: absolute; top: calc(100% + 8px); right: 0; min-width: 130px; background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius); box-shadow: var(--shadow); overflow: hidden; z-index: 200; }
.cat-item { padding: 8px 16px; font-size: 13px; color: var(--text-secondary); cursor: pointer; transition: all 0.2s; }
.cat-item:hover { background: var(--bg-card-hover); color: var(--text-primary); }
.cat-item.active { color: var(--accent); background: rgba(79,195,247,0.08); }
[data-theme="light"] .cat-item.active { background: rgba(37,99,235,0.08); }
.theme-btn { background: var(--bg-card); border: 1px solid var(--border); border-radius: 50%; width: 34px; height: 34px; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.3s; flex-shrink: 0; }
.theme-btn:hover { border-color: var(--accent); box-shadow: 0 0 10px var(--accent-glow); }
.theme-icon { font-size: 18px; color: var(--accent); line-height: 1; }
.admin-btn { display: flex; align-items: center; justify-content: center; width: 34px; height: 34px; border-radius: 50%; background: var(--bg-card); border: 1px solid var(--border); color: var(--text-muted); transition: all 0.3s; flex-shrink: 0; }
.admin-btn:hover { border-color: var(--accent); color: var(--accent); box-shadow: 0 0 10px var(--accent-glow); }

/* 移动端隐藏 */
.mobile-right { display: none; align-items: center; gap: 8px; margin-left: auto; }
.hamburger { background: none; border: none; cursor: pointer; padding: 4px; display: flex; flex-direction: column; gap: 5px; }
.hamburger span { display: block; width: 22px; height: 2px; background: var(--text-primary); border-radius: 2px; transition: all 0.3s; }
.hamburger.open span:nth-child(1) { transform: translateY(7px) rotate(45deg); }
.hamburger.open span:nth-child(2) { opacity: 0; }
.hamburger.open span:nth-child(3) { transform: translateY(-7px) rotate(-45deg); }

/* 移动端抽屉 */
.mobile-menu {
  display: none;
  position: fixed; top: 56px; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.4); z-index: 99;
}
.mobile-menu.open { display: block; }
.mobile-menu-inner {
  background: var(--bg-card); padding: 20px 16px;
  border-bottom: 1px solid var(--border);
  display: flex; flex-direction: column; gap: 20px;
}
.mobile-search .search-input { width: 100%; }
.mobile-nav-links { list-style: none; display: flex; flex-direction: column; gap: 0; }
.mobile-nav-links li a {
  display: block; padding: 12px 0;
  color: var(--text-secondary); font-size: 15px;
  border-bottom: 1px solid var(--border); transition: color 0.2s;
}
.mobile-nav-links li:last-child a { border-bottom: none; }
.mobile-nav-links li a:hover, .mobile-nav-links li a.router-link-active { color: var(--accent); }
.mobile-cat-title { font-size: 12px; color: var(--text-muted); margin-bottom: 10px; }
.mobile-cat-list { display: flex; flex-wrap: wrap; gap: 8px; }
.cat-tag { padding: 4px 12px; border-radius: 20px; font-size: 13px; border: 1px solid var(--border); color: var(--text-secondary); cursor: pointer; transition: all 0.2s; }
.cat-tag:hover, .cat-tag.active { border-color: var(--accent); color: var(--accent); background: rgba(79,195,247,0.08); }
[data-theme="light"] .cat-tag.active { background: rgba(37,99,235,0.08); }

@media (max-width: 768px) {
  .nav-links { display: none; }
  .nav-right { display: none; }
  .mobile-right { display: flex; }
  .logo { margin-right: 0; }
}
</style>
