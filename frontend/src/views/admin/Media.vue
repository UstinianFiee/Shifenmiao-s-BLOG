<template>
  <div class="media-page">
    <!-- 工具栏 -->
    <div class="toolbar card">
      <div class="toolbar-left">
        <h2 class="page-title">媒体库</h2>
        <div class="filter-tabs">
          <button :class="['tab', { active: filter === '' }]" @click="filter = ''; load(1)">全部</button>
          <button :class="['tab', { active: filter === 'image' }]" @click="filter = 'image'; load(1)">图片</button>
          <button :class="['tab', { active: filter === 'video' }]" @click="filter = 'video'; load(1)">视频</button>
        </div>
      </div>
      <label class="btn btn-primary upload-label">
        + 上传文件
        <input type="file" multiple accept="image/*,video/*" @change="uploadFiles" class="hidden-input" />
      </label>
    </div>

    <!-- 上传进度 -->
    <div v-if="uploading" class="upload-progress card">
      <div class="progress-bar"><div class="progress-fill" :style="{ width: uploadPct + '%' }"></div></div>
      <span>上传中 {{ uploadPct }}%</span>
    </div>

    <!-- 媒体网格 -->
    <div v-if="items.length === 0 && !loading" class="empty card">暂无媒体文件，点击上传按钮添加</div>
    <div v-else class="media-grid">
      <div v-for="m in items" :key="m.id" class="media-item card" @click="select(m)">
        <div class="media-thumb">
          <img v-if="m.file_type === 'image'" :src="m.url" :alt="m.name" loading="lazy" />
          <div v-else class="video-thumb">
            <canvas :ref="el => registerCanvas(el, m)" class="video-canvas"></canvas>
            <span class="video-badge">▶ VIDEO</span>
          </div>
        </div>
        <div class="media-info">
          <p class="media-name">{{ m.name }}</p>
          <p class="media-date">{{ formatDate(m.created_at) }}</p>
        </div>
      </div>
    </div>

    <!-- 分页 -->
    <div v-if="totalPages > 1" class="pagination">
      <button class="btn" :disabled="page <= 1" @click="load(page - 1)">上一页</button>
      <span class="page-info">{{ page }} / {{ totalPages }}</span>
      <button class="btn" :disabled="page >= totalPages" @click="load(page + 1)">下一页</button>
    </div>

    <!-- 详情弹窗 -->
    <div v-if="selected" class="modal-mask" @click.self="selected = null">
      <div class="modal card">
        <button class="modal-close" @click="selected = null">✕</button>
        <div class="modal-preview">
          <img v-if="selected.file_type === 'image'" :src="selected.url" />
          <video v-else :src="selected.url" controls class="modal-video"></video>
        </div>
        <div class="modal-meta">
          <p class="modal-name">{{ selected.name }}</p>
          <p class="modal-date">{{ formatDate(selected.created_at) }}</p>
          <div class="modal-caption">
            <label>说明</label>
            <input v-model="selected.caption" class="field-input" placeholder="添加说明..." @blur="saveCaption" />
          </div>
          <div class="modal-url">
            <label>链接</label>
            <div class="url-row">
              <input :value="selected.url" class="field-input" readonly />
              <button class="btn" @click="copyUrl">复制</button>
            </div>
          </div>
          <div class="modal-md">
            <label>MD 插入代码</label>
            <div class="url-row">
              <input :value="mdCode" class="field-input" readonly />
              <button class="btn" @click="copyMd">复制</button>
            </div>
          </div>
          <button class="btn btn-danger" style="margin-top:16px;width:100%;justify-content:center" @click="del">删除</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../../api'

const items = ref([])
const loading = ref(false)
const page = ref(1)
const totalPages = ref(1)
const filter = ref('')
const selected = ref(null)
const uploading = ref(false)
const uploadPct = ref(0)

// 视频封面：用 canvas 截取第一帧
function registerCanvas(canvas, media) {
  if (!canvas || media.file_type !== 'video') return
  const video = document.createElement('video')
  video.src = media.url
  video.crossOrigin = 'anonymous'
  video.muted = true
  video.preload = 'metadata'
  video.onloadeddata = () => {
    video.currentTime = 1
  }
  video.onseeked = () => {
    const ctx = canvas.getContext('2d')
    canvas.width = video.videoWidth || 320
    canvas.height = video.videoHeight || 180
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height)
    video.src = ''
  }
  video.load()
}

const mdCode = computed(() => {
  if (!selected.value) return ''
  if (selected.value.file_type === 'image') {
    return `![${selected.value.caption || selected.value.name}](${selected.value.url})`
  }
  return `<video src="${selected.value.url}" controls style="max-width:100%"></video>`
})

async function load(p = 1) {
  loading.value = true
  page.value = p
  const res = await api.get('/media', { params: { page: p, per_page: 24, type: filter.value || undefined } })
  items.value = res.data.items
  totalPages.value = res.data.pages
  loading.value = false
}

async function uploadFiles(e) {
  const files = Array.from(e.target.files)
  if (!files.length) return
  uploading.value = true
  uploadPct.value = 0
  for (let i = 0; i < files.length; i++) {
    const fd = new FormData()
    fd.append('file', files[i])
    await api.post('/media', fd)
    uploadPct.value = Math.round((i + 1) / files.length * 100)
  }
  uploading.value = false
  e.target.value = ''
  load(1)
}

function select(m) { selected.value = { ...m } }

async function saveCaption() {
  await api.put(`/media/${selected.value.id}`, { caption: selected.value.caption })
  const idx = items.value.findIndex(m => m.id === selected.value.id)
  if (idx !== -1) items.value[idx].caption = selected.value.caption
}

async function del() {
  if (!confirm('确认删除？此操作不可恢复')) return
  await api.delete(`/media/${selected.value.id}`)
  items.value = items.value.filter(m => m.id !== selected.value.id)
  selected.value = null
}

function copyUrl() { navigator.clipboard.writeText(selected.value.url) }
function copyMd() { navigator.clipboard.writeText(mdCode.value) }
function formatDate(iso) { return new Date(iso).toLocaleDateString('zh-CN') }

onMounted(() => load())
</script>

<style scoped>
.media-page { display: flex; flex-direction: column; gap: 16px; }
.toolbar { display: flex; align-items: center; justify-content: space-between; padding: 14px 20px; flex-wrap: wrap; gap: 12px; }
.toolbar-left { display: flex; align-items: center; gap: 16px; flex-wrap: wrap; }
.page-title { font-size: 18px; font-weight: 600; }
.filter-tabs { display: flex; gap: 4px; }
.tab { padding: 5px 14px; border-radius: 20px; border: 1px solid var(--border); background: none; color: var(--text-secondary); font-size: 13px; cursor: pointer; transition: all 0.2s; }
.tab.active, .tab:hover { border-color: var(--accent); color: var(--accent); background: rgba(79,195,247,0.08); }
[data-theme="light"] .tab.active { background: rgba(37,99,235,0.08); }
.upload-label { cursor: pointer; }
.hidden-input { display: none; }

.upload-progress { padding: 12px 20px; display: flex; align-items: center; gap: 12px; }
.progress-bar { flex: 1; height: 6px; background: var(--border); border-radius: 3px; overflow: hidden; }
.progress-fill { height: 100%; background: linear-gradient(90deg, var(--accent), var(--accent-2)); transition: width 0.3s; }

.media-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 12px; }
.media-item { cursor: pointer; overflow: hidden; transition: all 0.2s; }
.media-item:hover { border-color: var(--accent); transform: translateY(-2px); }
.media-thumb { height: 120px; overflow: hidden; background: var(--bg-secondary); }
.media-thumb img { width: 100%; height: 100%; object-fit: cover; }
.video-thumb { position: relative; width: 100%; height: 100%; background: #0a0c14; display: flex; align-items: center; justify-content: center; }
.video-canvas { width: 100%; height: 100%; object-fit: cover; display: block; }
.video-badge { position: absolute; bottom: 6px; right: 6px; background: rgba(0,0,0,0.65); color: #fff; font-size: 10px; padding: 2px 7px; border-radius: 4px; letter-spacing: 0.5px; }
.media-info { padding: 8px 10px; }
.media-name { font-size: 12px; color: var(--text-secondary); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.media-date { font-size: 11px; color: var(--text-muted); margin-top: 2px; }

.empty { padding: 60px; text-align: center; color: var(--text-muted); }
.pagination { display: flex; align-items: center; justify-content: center; gap: 16px; }
.page-info { font-size: 14px; color: var(--text-secondary); }

/* 弹窗 */
.modal-mask { position: fixed; inset: 0; background: rgba(0,0,0,0.6); z-index: 300; display: flex; align-items: center; justify-content: center; padding: 20px; }
.modal { position: relative; width: 100%; max-width: 800px; max-height: 90vh; overflow-y: auto; display: flex; gap: 24px; padding: 24px; }
.modal-close { position: absolute; top: 12px; right: 12px; background: none; border: none; color: var(--text-muted); font-size: 18px; cursor: pointer; transition: color 0.2s; }
.modal-close:hover { color: var(--text-primary); }
.modal-preview { flex: 1; min-width: 0; display: flex; align-items: center; justify-content: center; background: var(--bg-secondary); border-radius: var(--radius); overflow: hidden; min-height: 200px; }
.modal-preview img { max-width: 100%; max-height: 60vh; object-fit: contain; }
.modal-video { max-width: 100%; max-height: 60vh; }
.modal-meta { width: 240px; flex-shrink: 0; display: flex; flex-direction: column; gap: 14px; }
.modal-name { font-size: 14px; font-weight: 500; color: var(--text-primary); word-break: break-all; }
.modal-date { font-size: 12px; color: var(--text-muted); }
.modal-caption label, .modal-url label, .modal-md label { font-size: 12px; color: var(--text-muted); display: block; margin-bottom: 6px; }
.field-input { width: 100%; padding: 8px 12px; background: var(--bg-primary); border: 1px solid var(--border); border-radius: var(--radius); color: var(--text-primary); font-size: 13px; outline: none; transition: border-color 0.2s; }
.field-input:focus { border-color: var(--accent); }
.url-row { display: flex; gap: 8px; }
.url-row .field-input { flex: 1; min-width: 0; }

@media (max-width: 768px) {
  .modal { flex-direction: column; }
  .modal-meta { width: 100%; }
  .media-grid { grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); }
}
</style>
