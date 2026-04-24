<template>
  <router-link :to="`/article/${article.id}`" class="article-card card">
    <div v-if="article.cover" class="cover">
      <img :src="article.cover" :alt="article.title" />
    </div>
    <div class="body">
      <div class="meta">
        <span v-if="article.category" class="category">{{ article.category.name }}</span>
        <span class="date">{{ formatDate(article.created_at) }}</span>
        <span class="views">👁 {{ article.views }}</span>
      </div>
      <h2 class="title">{{ article.title }}</h2>
      <p class="summary">{{ article.summary }}</p>
      <div class="tags">
        <span v-for="t in article.tags" :key="t.id" class="tag">{{ t.name }}</span>
      </div>
    </div>
  </router-link>
</template>

<script setup>
defineProps({ article: Object })
function formatDate(iso) {
  return new Date(iso).toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' })
}
</script>

<style scoped>
.article-card { display: block; overflow: hidden; }
.cover { height: 180px; overflow: hidden; }
.cover img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.4s; }
.article-card:hover .cover img { transform: scale(1.05); }
.body { padding: 20px; }
.meta { display: flex; gap: 12px; align-items: center; font-size: 12px; color: var(--text-muted); margin-bottom: 10px; }
.category { color: var(--accent); border: 1px solid var(--accent); padding: 1px 8px; border-radius: 4px; }
.title { font-size: 18px; font-weight: 500; margin-bottom: 8px; color: var(--text-primary); line-height: 1.4; }
.summary { font-size: 14px; color: var(--text-secondary); display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.tags { margin-top: 12px; display: flex; flex-wrap: wrap; gap: 6px; }
</style>
