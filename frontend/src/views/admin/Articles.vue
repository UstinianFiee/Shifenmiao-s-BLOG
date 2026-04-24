<template>
  <div class="admin-articles">
    <div class="toolbar card">
      <h2 class="page-title">文章管理</h2>
      <router-link to="/admin/articles/new" class="btn btn-primary">+ 新建文章</router-link>
    </div>

    <div class="table-wrap card">
      <table class="table">
        <thead>
          <tr>
            <th>标题</th>
            <th>分类</th>
            <th>状态</th>
            <th>阅读</th>
            <th>发布时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="a in articles" :key="a.id">
            <td class="title-cell">{{ a.title }}</td>
            <td>{{ a.category?.name || '-' }}</td>
            <td>
              <span class="status-badge" :class="a.status">
                {{ a.status === 'published' ? '已发布' : '草稿' }}
              </span>
            </td>
            <td>{{ a.views }}</td>
            <td>{{ formatDate(a.created_at) }}</td>
            <td class="actions">
              <router-link :to="`/admin/articles/${a.id}/edit`" class="btn" style="padding:4px 12px;font-size:12px">编辑</router-link>
              <button class="btn btn-danger" style="padding:4px 12px;font-size:12px" @click="del(a.id)">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
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
.table-wrap { overflow-x: auto; }
.table { width: 100%; border-collapse: collapse; font-size: 14px; }
.table th { padding: 12px 16px; text-align: left; color: var(--accent); font-weight: 500; border-bottom: 1px solid var(--border); }
.table td { padding: 12px 16px; border-bottom: 1px solid var(--border); color: var(--text-secondary); }
.table tr:last-child td { border-bottom: none; }
.table tr:hover td { background: var(--bg-card-hover); }
.title-cell { color: var(--text-primary); max-width: 280px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.status-badge { padding: 2px 8px; border-radius: 4px; font-size: 12px; }
.status-badge.published { background: rgba(79,195,247,0.15); color: var(--accent); }
.status-badge.draft { background: rgba(255,213,79,0.15); color: var(--gold); }
.actions { display: flex; gap: 8px; }
.empty { text-align: center; color: var(--text-muted); padding: 40px; }
.pagination { display: flex; align-items: center; gap: 16px; margin-top: 24px; }
.page-info { color: var(--text-secondary); font-size: 14px; }
</style>
