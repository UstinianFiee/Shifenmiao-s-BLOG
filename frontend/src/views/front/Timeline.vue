<template>
  <div class="timeline-page container">
    <div class="page-header fade-in-up">
      <p class="page-sub">TIMELINE</p>
      <h1 class="page-title">时间轴</h1>
    </div>
    <div class="glow-divider"></div>

    <div v-if="loading" class="loading">加载中...</div>
    <div v-else class="timeline">
      <div v-for="(items, year) in data" :key="year" class="year-group fade-in-up">
        <div class="year-label">{{ year }}</div>
        <div class="year-items">
          <router-link
            v-for="a in items" :key="a.id"
            :to="`/article/${a.id}`"
            class="timeline-item"
          >
            <span class="dot"></span>
            <span class="item-date">{{ formatDate(a.created_at) }}</span>
            <span class="item-title">{{ a.title }}</span>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api'

const data = ref({})
const loading = ref(true)

function formatDate(iso) {
  const d = new Date(iso)
  return `${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`
}

onMounted(async () => {
  const res = await api.get('/articles/timeline')
  data.value = res.data
  loading.value = false
})
</script>

<style scoped>
.timeline-page { padding: 120px 24px 80px; max-width: 800px; }
.page-header { text-align: center; margin-bottom: 40px; }
.page-sub { font-size: 12px; letter-spacing: 6px; color: var(--accent); margin-bottom: 8px; }
.page-title { font-size: 36px; font-weight: 700; }

.year-group { margin-bottom: 48px; }
.year-label {
  font-size: 28px; font-weight: 700; color: var(--accent);
  margin-bottom: 20px; opacity: 0.7;
}
.year-items { border-left: 1px solid var(--border); padding-left: 24px; display: flex; flex-direction: column; gap: 16px; }
.timeline-item {
  display: flex; align-items: center; gap: 16px;
  position: relative; color: var(--text-secondary);
  transition: color 0.3s;
}
.timeline-item:hover { color: var(--accent); }
.dot {
  position: absolute; left: -29px;
  width: 8px; height: 8px; border-radius: 50%;
  background: var(--accent); border: 2px solid var(--bg-primary);
  transition: box-shadow 0.3s;
}
.timeline-item:hover .dot { box-shadow: 0 0 8px var(--accent); }
.item-date { font-size: 13px; color: var(--text-muted); flex-shrink: 0; font-variant-numeric: tabular-nums; }
.item-title { font-size: 15px; }
.loading { text-align: center; color: var(--text-muted); padding: 80px 0; }

@media (max-width: 768px) {
  .timeline-page { padding: 90px 16px 80px; }
  .page-title { font-size: 28px; }
  .year-label { font-size: 22px; }
  .item-title { font-size: 14px; }
}
</style>
