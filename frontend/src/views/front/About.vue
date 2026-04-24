<template>
  <div class="about-page container">
    <div class="about-card card fade-in-up">
      <div class="avatar-wrap">
        <div class="avatar-ring"></div>
        <img v-if="profile.avatar" :src="profile.avatar" class="avatar-img" />
        <div v-else class="avatar">{{ profile.nickname?.charAt(0) || 'A' }}</div>
      </div>
      <h1 class="name">{{ profile.nickname || '时分渺OvO' }}</h1>
      <p class="bio">{{ profile.bio || '热爱技术，热爱生活。' }}</p>
      <div class="glow-divider"></div>
      <div class="stats">
        <div class="stat">
          <span class="stat-num">{{ stats.articles }}</span>
          <span class="stat-label">文章</span>
        </div>
        <div class="stat">
          <span class="stat-num">{{ stats.categories }}</span>
          <span class="stat-label">分类</span>
        </div>
        <div class="stat">
          <span class="stat-num">{{ stats.tags }}</span>
          <span class="stat-label">标签</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api'

const profile = ref({ nickname: '', bio: '', avatar: '' })
const stats = ref({ articles: 0, categories: 0, tags: 0 })

onMounted(async () => {
  const [prof, arts, cats, tags] = await Promise.all([
    api.get('/account/profile'),
    api.get('/articles?per_page=1'),
    api.get('/categories'),
    api.get('/tags'),
  ])
  profile.value = prof.data
  stats.value = {
    articles: arts.data.total,
    categories: cats.data.length,
    tags: tags.data.length,
  }
})
</script>

<style scoped>
.about-page { padding: 120px 24px 80px; display: flex; justify-content: center; }
.about-card { max-width: 480px; width: 100%; padding: 48px; text-align: center; }

@media (max-width: 768px) {
  .about-page { padding: 90px 16px 80px; }
  .about-card { padding: 32px 20px; }
  .stats { gap: 24px; }
}
.avatar-wrap { position: relative; width: 100px; height: 100px; margin: 0 auto 24px; }
.avatar-ring {
  position: absolute; inset: -4px; border-radius: 50%;
  background: conic-gradient(var(--accent), var(--accent-2), var(--accent));
  animation: spin 4s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
.avatar-img { width: 100px; height: 100px; border-radius: 50%; object-fit: cover; position: relative; z-index: 1; }
.avatar {
  width: 100px; height: 100px; border-radius: 50%;
  background: linear-gradient(135deg, var(--accent), var(--accent-2));
  position: relative; z-index: 1;
  display: flex; align-items: center; justify-content: center;
  font-size: 40px; font-weight: 700; color: #fff;
}
.name { font-size: 24px; font-weight: 700; margin-bottom: 8px; }
.bio { color: var(--text-secondary); font-size: 15px; }
.stats { display: flex; justify-content: center; gap: 48px; }
.stat { display: flex; flex-direction: column; align-items: center; gap: 4px; }
.stat-num { font-size: 28px; font-weight: 700; color: var(--accent); }
.stat-label { font-size: 13px; color: var(--text-muted); }
</style>
