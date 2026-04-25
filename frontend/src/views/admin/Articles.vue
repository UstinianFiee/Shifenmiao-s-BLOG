<template>
  <div class="admin-articles">
    <div class="toolbar card">
      <h2 class="page-title">文章管理</h2>
      <router-link to="/admin/articles/new" class="btn btn-primary">+ 新建文章</router-link>
    </div>

    <div class="list-wrap card">
      <div v-for="a in articles" :key="a.id" class="article-row">
        <div class="row-main">
          <div class="row-title">{{ a.title }}</div>
          <div class="row-meta">
            <span v-if="a.category" class="meta-cat">{{ a.category.name }}</span>
            <span class="status-badge" :class="a.status">
              {{ a.status === 'published' ? '已发布' : '草稿' }}
            </span>
            <span class="meta-info">👁 {{ a.views }}</span>
            <span class="meta-info">{{ formatDate(a.created_at) }}</span>
          </div>
        </div>
        <div class="row-actions">
          <router-link :to="`/admin/articles/${a.id}/edit`" class="action-btn">编辑</router-link>
          <button class="action-btn danger" @click="del(a.id)">删除</button>
        </div>
      </div>
      <div v-if="articles.length === 0" class="empty">暂无文章</div>
    </div>

    <div v-if="totalPages > 1" class="pagination">
      <button class="btn" :disabled="page <= 1" @click="fetch(page - 1)">上一页</button>
      <span class="page-info">{{ page }} / {{ totalPages }}</span>
      <button class="btn" :disabled="page >= totalPages" @click="fetch(page + 1)">下一页</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api'

const articles = ref([])
const page = ref(1)
const totalPages = ref(1)

async function fetch(p = 1) {
  page.value = p
  const res = await api.get('/articles/admin/all', { params: { page: p, per_page: 15 } })
  articles.value = res.data.items
  totalPages.value = res.data.pages
}

async function del(id) {
  if (!confirm('确认删除？')) return
  await api.delete(`/articles/admin/${id}`)
  fetch(page.value)
}

function formatDate(iso) {
  return new Date(iso).toLocaleDateString('zh-CN')
}

onMounted(() => fetch())
</script>

<style scoped>
.admin-articles { display: flex; flex-direction: column; gap: 16px; }
.toolbar { display: flex; align-items: center; justify-content: space-between; padding: 16px 20px; }
.page-title { font-size: 18px; font-weight: 600; }

.list-wrap { overflow: hidden; }
.article-row {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 20px; border-bottom: 1px solid var(--border); gap: 12px;
}
.article-row:last-child { border-bottom: none; }
.article-row:hover { background: var(--bg-card-hover); }

.row-main { flex: 1; min-width: 0; }
.row-title { font-size: 14px; font-weight: 500; color: var(--text-primary); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; margin-bottom: 6px; }
.row-meta { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; }
.meta-cat { font-size: 12px; color: var(--accent); border: 1px solid var(--accent); padding: 1px 7px; border-radius: 4px; }
.meta-info { font-size: 12px; color: var(--text-muted); }
.status-badge { padding: 2px 8px; border-radius: 4px; font-size: 12px; }
.status-badge.published { background: rgba(79,195,247,0.15); color: var(--accent); }
.status-badge.draft { background: rgba(255,213,79,0.15); color: var(--gold); }

.row-actions { display: flex; gap: 8px; flex-shrink: 0; }
.action-btn {
  display: inline-flex; align-items: center; justify-content: center;
  padding: 5px 14px; border-radius: var(--radius);
  font-size: 13px; cursor: pointer; transition: all 0.2s;
  border: 1px solid var(--border-glow); color: var(--accent); background: none;
  white-space: nowrap; text-decoration: none;
}
.action-btn:hover { background: var(--accent); color: #fff; }
.action-btn.danger { border-color: rgba(239,68,68,0.4); color: #ef4444; }
.action-btn.danger:hover { background: #ef4444; color: #fff; }

.empty { text-align: center; color: var(--text-muted); padding: 40px; }
.pagination { display: flex; align-items: center; justify-content: center; gap: 16px; }
.page-info { color: var(--text-secondary); font-size: 14px; }

@media (max-width: 768px) {
  .article-row { flex-wrap: wrap; }
  .row-title { white-space: normal; }
  .row-actions { width: 100%; }
}
</style>
