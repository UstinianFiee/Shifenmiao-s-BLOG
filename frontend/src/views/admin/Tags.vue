<template>
  <div class="admin-page">
    <div class="toolbar card">
      <h2 class="page-title">标签管理</h2>
      <div class="add-form">
        <input v-model="newName" class="field-input" placeholder="新标签名称" @keyup.enter="add" />
        <button class="btn btn-primary" @click="add">添加</button>
      </div>
    </div>
    <div class="tags-cloud card" style="padding:20px">
      <span v-for="t in tags" :key="t.id" class="tag-item">
        {{ t.name }} ({{ t.count }})
        <button class="del-btn" @click="del(t.id)">×</button>
      </span>
      <div v-if="tags.length === 0" class="empty">暂无标签</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api'

const tags = ref([])
const newName = ref('')

async function fetch() {
  const res = await api.get('/tags')
  tags.value = res.data
}
async function add() {
  if (!newName.value.trim()) return
  await api.post('/tags', { name: newName.value.trim() })
  newName.value = ''
  fetch()
}
async function del(id) {
  if (!confirm('确认删除？')) return
  await api.delete(`/tags/${id}`)
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
.tags-cloud { display: flex; flex-wrap: wrap; gap: 10px; }
.tag-item {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 4px 12px; border-radius: 20px;
  border: 1px solid var(--border); color: var(--text-secondary); font-size: 13px;
}
.del-btn {
  background: none; border: none; color: var(--text-muted);
  cursor: pointer; font-size: 16px; line-height: 1; padding: 0;
  transition: color 0.2s;
}
.del-btn:hover { color: #ff5252; }
.empty { color: var(--text-muted); }
</style>
