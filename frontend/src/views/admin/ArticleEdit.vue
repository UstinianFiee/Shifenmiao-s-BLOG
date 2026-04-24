<template>
  <div class="article-edit">
    <div class="page-header">
      <h2 class="page-title">{{ isEdit ? '编辑文章' : '新建文章' }}</h2>
      <div class="header-actions">
        <button class="btn" @click="save('draft')">保存草稿</button>
        <button class="btn btn-primary" @click="save('published')">发布</button>
      </div>
    </div>

    <div class="edit-layout">
      <!-- 左侧主编辑区 -->
      <div class="edit-main">
        <input v-model="form.title" class="title-input" placeholder="文章标题..." />
        <input v-model="form.summary" class="summary-input" placeholder="摘要（可选）..." />
        <!-- Vditor MD 编辑器 -->
        <div id="vditor" class="editor-wrap"></div>
      </div>

      <!-- 右侧配置 -->
      <aside class="edit-sidebar">
        <div class="sidebar-section card">
          <p class="section-title">封面图</p>
          <input v-model="form.cover" class="field-input" placeholder="图片URL" />
          <div class="upload-area" @click="$refs.coverInput.click()" @dragover.prevent @drop.prevent="onDrop">
            <input ref="coverInput" type="file" accept="image/*" @change="uploadCover" class="hidden-input" />
            <div v-if="form.cover" class="cover-preview-wrap">
              <img :src="form.cover" class="cover-preview" />
              <div class="cover-overlay">点击更换</div>
            </div>
            <div v-else class="upload-placeholder">
              <span class="upload-icon">&#128247;</span>
              <span class="upload-text">点击或拖拽上传封面</span>
              <span class="upload-hint">支持 JPG / PNG / WebP</span>
            </div>
          </div>
        </div>

        <div class="sidebar-section card">
          <p class="section-title">分类</p>
          <select v-model="form.category_id" class="field-input">
            <option :value="null">无分类</option>
            <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
          </select>
        </div>

        <div class="sidebar-section card">
          <p class="section-title">标签</p>
          <div class="tags-select">
            <label v-for="t in tags" :key="t.id" class="tag-check">
              <input type="checkbox" :value="t.id" v-model="form.tag_ids" />
              {{ t.name }}
            </label>
          </div>
        </div>
      </aside>
    </div>

    <p v-if="msg" class="save-msg">{{ msg }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../../api'
import Vditor from 'vditor'
import 'vditor/dist/index.css'

const route = useRoute()
const router = useRouter()
const isEdit = !!route.params.id
const msg = ref('')

const form = ref({
  title: '', summary: '', cover: '', content: '',
  status: 'draft', category_id: null, tag_ids: [],
})

const categories = ref([])
const tags = ref([])
let vd = null

onMounted(async () => {
  const [cats, tgs] = await Promise.all([api.get('/categories'), api.get('/tags')])
  categories.value = cats.data
  tags.value = tgs.data

  const isDark = document.documentElement.getAttribute('data-theme') !== 'light'
  vd = new Vditor('vditor', {
    height: 600,
    theme: isDark ? 'dark' : 'classic',
    contentTheme: isDark ? 'dark' : 'light',
    toolbar: [
      'emoji','headings','bold','italic','strike','|','line','quote','list','ordered-list',
      'check','outdent','indent','|','code','inline-code','insert-after','insert-before','|',
      'upload','link','table','|','undo','redo','|','fullscreen','preview',
    ],
    upload: {
      url: '/api/upload',
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      fieldName: 'file',
      success: (_, msg) => {
        const url = JSON.parse(msg).url
        return url
      },
    },
    after: async () => {
      if (isEdit) {
        const res = await api.get(`/articles/admin/all?page=1&per_page=999`)
        // fetch single article via public endpoint (full content)
        const art = await api.get(`/articles/${route.params.id}`)
        // if draft, use admin endpoint workaround - just load content
        const a = art.data
        form.value = {
          title: a.title, summary: a.summary, cover: a.cover,
          status: a.status, category_id: a.category?.id || null,
          tag_ids: a.tags.map(t => t.id), content: a.content,
        }
        vd.setValue(a.content)
      }
    },
  })
})

onUnmounted(() => vd?.destroy())

async function save(status) {
  form.value.content = vd.getValue()
  form.value.status = status
  if (!form.value.title.trim()) { msg.value = '请填写标题'; return }
  try {
    if (isEdit) {
      await api.put(`/articles/admin/${route.params.id}`, form.value)
    } else {
      await api.post('/articles/admin', form.value)
    }
    msg.value = status === 'published' ? '发布成功' : '草稿已保存'
    setTimeout(() => router.push('/admin/articles'), 800)
  } catch {
    msg.value = '保存失败，请重试'
  }
}

async function uploadCover(e) {
  const file = e.target.files[0]
  if (!file) return
  const fd = new FormData()
  fd.append('file', file)
  const res = await api.post('/upload', fd)
  form.value.cover = res.data.url
}

async function onDrop(e) {
  const file = e.dataTransfer.files[0]
  if (!file || !file.type.startsWith('image/')) return
  const fd = new FormData()
  fd.append('file', file)
  const res = await api.post('/upload', fd)
  form.value.cover = res.data.url
}
</script>

<style scoped>
.article-edit { max-width: 1400px; margin: 0 auto; }
.page-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px; }
.page-title { font-size: 22px; font-weight: 600; }
.header-actions { display: flex; gap: 12px; }

.edit-layout { display: flex; gap: 24px; align-items: flex-start; }
.edit-main { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 12px; }

.title-input, .summary-input {
  width: 100%; padding: 12px 16px;
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: var(--radius); color: var(--text-primary);
  font-size: 16px; outline: none; transition: border-color 0.3s;
}
.title-input { font-size: 20px; font-weight: 600; }
.title-input:focus, .summary-input:focus { border-color: var(--accent); }

.editor-wrap { border-radius: var(--radius); overflow: hidden; }

.edit-sidebar { width: 300px; flex-shrink: 0; display: flex; flex-direction: column; gap: 16px; }
.sidebar-section { padding: 20px; }
.section-title { font-size: 14px; color: var(--accent); margin-bottom: 12px; font-weight: 600; }
.field-input {
  width: 100%; padding: 10px 14px;
  background: var(--bg-primary); border: 1px solid var(--border);
  border-radius: var(--radius); color: var(--text-primary); font-size: 14px;
  outline: none; transition: border-color 0.3s; margin-bottom: 10px;
}
.field-input:focus { border-color: var(--accent); }
.file-input { font-size: 12px; color: var(--text-muted); margin-top: 4px; }
.hidden-input { display: none; }
.upload-area {
  margin-top: 10px; border: 1.5px dashed var(--border);
  border-radius: var(--radius); cursor: pointer;
  transition: border-color 0.3s, background 0.3s; overflow: hidden;
}
.upload-area:hover { border-color: var(--accent); background: rgba(79,195,247,0.04); }
[data-theme="light"] .upload-area:hover { background: rgba(37,99,235,0.04); }
.upload-placeholder { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 6px; padding: 24px 16px; }
.upload-icon { font-size: 28px; }
.upload-text { font-size: 13px; color: var(--text-secondary); }
.upload-hint { font-size: 11px; color: var(--text-muted); }
.cover-preview-wrap { position: relative; }
.cover-preview { width: 100%; display: block; max-height: 160px; object-fit: cover; }
.cover-overlay { position: absolute; inset: 0; background: rgba(0,0,0,0.45); color: #fff; display: flex; align-items: center; justify-content: center; font-size: 13px; opacity: 0; transition: opacity 0.2s; }
.cover-preview-wrap:hover .cover-overlay { opacity: 1; }

.tags-select { display: flex; flex-wrap: wrap; gap: 10px; }
.tag-check { display: flex; align-items: center; gap: 6px; font-size: 13px; color: var(--text-secondary); cursor: pointer; }
.tag-check input { accent-color: var(--accent); cursor: pointer; }

.save-msg { margin-top: 16px; color: var(--accent); font-size: 14px; text-align: center; }
</style>
