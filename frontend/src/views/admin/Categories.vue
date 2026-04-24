<template>
  <div class="admin-page">
    <div class="toolbar card">
      <h2 class="page-title">分类管理</h2>
      <div class="add-form">
        <input v-model="newName" class="field-input" placeholder="新分类名称" @keyup.enter="add" />
        <button class="btn btn-primary" @click="add">添加</button>
      </div>
    </div>
    <div class="list card">
      <div v-for="c in categories" :key="c.id" class="list-item">
        <span class="item-name">{{ c.name }}</span>
        <span class="item-count">{{ c.count }} 篇</span>
        <button class="btn btn-danger" style="padding:4px 12px;font-size:12px" @click="del(c.id)">删除</button>
      </div>
      <div v-if="categories.length === 0" class="empty">暂无分类</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api'

const categories = ref([])
const newName = ref('')

async function fetch() {
  const res = await api.get('/categories')
  categories.value = res.data
}
async function add() {
  if (!newName.value.trim()) return
  await api.post('/categories', { name: newName.value.trim() })
  newName.value = ''
  fetch()
}
async function del(id) {
  if (!confirm('确认删除？')) return
  await api.delete(`/categories/${id}`)
  fetch()
}
onMounted(fetch)
</script>

<style scoped>
.admin-page { display: flex; flex-direction: column; gap: 16px; }
.toolbar { display: flex; align-items: center; justify-content: space-between; padding: 16px 20px; flex-wrap: wrap; gap: 12px; }
.page-title { font-size: 18px; font-weight: 600; }
.add-form { display: flex; gap: 10px; }
.field-input {
  flex: 1; padding: 8px 14px;
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: var(--radius); color: var(--text-primary); font-size: 14px; outline: none;
}
.field-input:focus { border-color: var(--accent); }
.list { overflow: hidden; }
.list-item {
  display: flex; align-items: center; gap: 12px;
  padding: 12px 16px; border-bottom: 1px solid var(--border);
}
.list-item:last-child { border-bottom: none; }
.item-name { flex: 1; color: var(--text-primary); font-size: 14px; }
.item-count { color: var(--text-muted); font-size: 13px; }
.empty { text-align: center; color: var(--text-muted); padding: 32px; }
</style>
