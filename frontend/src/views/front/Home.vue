<template>
  <div class="home">
    <!-- Hero -->
    <section class="hero">
      <div class="hero-content fade-in-up">
        <p class="hero-sub">TECH · LIFE · THOUGHTS</p>
        <h1 class="hero-title hero-gradient-text">时分渺OvO的小窝</h1>
        <p class="hero-desc">记录技术与生活的点滴，分享思考与感悟</p>
      </div>
      <div class="hero-scroll-hint">↓</div>
    </section>

    <!-- 文章列表 -->
    <section class="articles-section container">
      <div v-if="loading" class="loading">加载中...</div>
      <div v-else-if="articles.length === 0" class="empty">暂无文章</div>
      <div v-else class="articles-grid">
        <ArticleCard v-for="a in articles" :key="a.id" :article="a" class="fade-in-up" />
      </div>
      <div v-if="totalPages > 1" class="pagination">
        <button class="btn" :disabled="page <= 1" @click="fetchArticles(page - 1)">上一页</button>
        <span class="page-info">{{ page }} / {{ totalPages }}</span>
        <button class="btn" :disabled="page >= totalPages" @click="fetchArticles(page + 1)">下一页</button>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import api from '../../api'
import ArticleCard from '../../components/front/ArticleCard.vue'

const route = useRoute()
const articles = ref([])
const loading = ref(false)
const page = ref(1)
const totalPages = ref(1)

async function fetchArticles(p = 1) {
  loading.value = true
  page.value = p
  try {
    const res = await api.get('/articles', {
      params: {
        page: p,
        per_page: 9,
        keyword: route.query.keyword || '',
        category_id: route.query.category_id || null,
      }
    })
    articles.value = res.data.items
    totalPages.value = res.data.pages
  } finally {
    loading.value = false
  }
}

// 路由参数变化时重新加载
watch(() => route.query, () => fetchArticles(1), { immediate: true })
</script>

<style scoped>
.hero {
  min-height: 100vh;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  text-align: center; padding: 0 24px;
  position: relative;
}
.hero-sub { font-size: 12px; letter-spacing: 6px; color: var(--accent); margin-bottom: 16px; }
.hero-title { font-size: clamp(36px, 6vw, 72px); font-weight: 700; line-height: 1.2; margin-bottom: 16px; }
.hero-desc { font-size: 16px; color: var(--text-secondary); }
.hero-scroll-hint { position: absolute; bottom: 32px; font-size: 20px; color: var(--text-muted); animation: bounce 2s infinite; }
@keyframes bounce { 0%,100%{transform:translateY(0)} 50%{transform:translateY(8px)} }
.articles-section { padding: 80px 24px 80px; }
.articles-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 24px; }
.loading, .empty { text-align: center; color: var(--text-muted); padding: 60px 0; }
.pagination { display: flex; align-items: center; justify-content: center; gap: 16px; margin-top: 48px; }
.page-info { color: var(--text-secondary); font-size: 14px; }
</style>
