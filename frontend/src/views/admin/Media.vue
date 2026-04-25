<template>
  <div class="media-page">
    <div class="toolbar card">
      <div class="toolbar-left">
        <h2 class="page-title">媒体库</h2>
        <div class="filter-tabs">
          <button :class="['tab', { active: filter === '' }]" @click="setFilter('')">全部</button>
          <button :class="['tab', { active: filter === 'image' }]" @click="setFilter('image')">图片</button>
          <button :class="['tab', { active: filter === 'video' }]" @click="setFilter('video')">视频</button>
        </div>
      </div>
      <label class="btn btn-primary upload-label">
        + 上传文件
        <input type="file" multiple accept="image/*,video/*" @change="uploadFiles" class="hidden-input" ref="fileInput" />
      </label>
    </div>

    <div v-if="uploading" class="upload-progress card">
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: pct + '%' }"></div>
      </div>
      <span>上传中 {{ pct }}%</span>
    </div>

    <div v-if="loading" class="status-card card">加载中...</div>
    <div v-else-if="items.length === 0" class="status-card card">暂无媒体文件，点击上传按钮添加</div>
    <div v-else class="media-grid">
      <div v-for="m in items" :key="m.id" class="media-item card" @click="openDetail(m)">
        <div class="media-thumb">
          <img v-if="m.file_type === 'image'" :src="m.url" :alt="m.name" loading="lazy" />
          <div v-else class="video-thumb">
            <canvas :ref="el => drawVideoThumb(el, m.url)" class="video-canvas"></canvas>
            <span class="video-badge">VIDEO</span>
          </div>
        </div>
        <div class="media-info">
          <p class="media-name">{{ m.name }}</p>
          <p class="media-date">{{ fmtDate(m.created_at) }}</p>
        </div>
      </div>
    </div>

    <div v-if="totalPages > 1" class="pagination">
      <button class="btn" :disabled="page <= 1" @click="load(page - 1)">上一页</button>
      <span class="page-info">{{ page }} / {{ totalPages }}</span>
      <button class="btn" :disabled="page >= totalPages" @click="load(page + 1)">下一页</button>
    </div>

    <div v-if="detail" class="modal-mask" @click.self="detail = null">
      <div class="modal card">
        <button class="modal-close" @click="detail = null">✕</button>
        <div class="modal-preview">
          <img v-if="detail.file_type === 'image'" :src="detail.url" />
          <video v-else :src="detail.url" controls class="modal-video"></video>
        </div>
        <div class="modal-meta">
          <p class="modal-name">{{ detail.name }}</p>
          <p class="modal-date">{{ fmtDate(detail.created_at) }}</p>
          <div class="meta-row">
            <label>说明</label>
            <input v-model="detail.caption" class="field-input" placeholder="添加说明..." @blur="saveCaption" />
          </div>
          <div class="meta-row">
            <label>链接</label>
            <div class="copy-row">
              <input :value="detail.url" class="field-input" readonly />
              <button class="btn" @click="copy(detail.url)">复制</button>
            </div>
          </div>
          <div class="meta-row">
            <label>MD 代码</label>
            <div class="copy-row">
              <input :value="mdCode" class="field-input" readonly />
              <button class="btn" @click="copy(mdCode)">复制</button>
            </div>
          </div>
          <button class="btn btn-danger del-btn" @click="delItem">删除</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../../api'
import { useToast } from '../../stores/toast'

const { show: toast } = useToast()

const items = ref([])
const loading = ref(false)
const page = ref(1)
const totalPages = ref(1)
const filter = ref('')
const detail = ref(null)
const uploading = ref(false)
const pct = ref(0)
const fileInput = ref(null)

const mdCode = computed(() => {
  if (!detail.value) return ''
  if (detail.value.file_type === 'image') {
    return '![' + (detail.value.caption || detail.value.name) + '](' + detail.value.url + ')'
  }
  return '<video src="' + detail.value.url + '" controls style="max-width:100%"></video>'
})

function setFilter(val) {
  filter.value = val
  load(1)
}

async function load(p) {
  loading.value = true
  page.value = p || 1
  try {
    const params = { page: page.value, per_page: 24 }
    if (filter.value) params.type = filter.value
    const res = await api.get('/media', { params })
    items.value = Array.isArray(res.data.items) ? res.data.items : []
    totalPages.value = res.data.pages || 1
  } catch (e) {
    toast('加载失败', 'error')
    items.value = []
  } finally {
    loading.value = false
  }
}

async function uploadFiles(e) {
  const files = Array.from(e.target.files || [])
  if (!files.length) return
  uploading.value = true
  pct.value = 0
  let ok = 0
  for (let i = 0; i < files.length; i++) {
    try {
      const fd = new FormData()
      fd.append('file', files[i])
      await api.post('/media', fd)
      ok++
    } catch (err) {
      toast((err.response && err.response.data && err.response.data.msg) || (files[i].name + ' 上传失败'), 'error')
    }
    pct.value = Math.round((i + 1) / files.length * 100)
  }
  uploading.value = false
  if (fileInput.value) fileInput.value.value = ''
  if (ok > 0) {
    toast('上传成功 ' + ok + ' 个文件')
    load(1)
  }
}

function openDetail(m) {
  detail.value = Object.assign({}, m)
}

async function saveCaption() {
  if (!detail.value) return
  await api.put('/media/' + detail.value.id, { caption: detail.value.caption })
  const idx = items.value.findIndex(function(m) { return m.id === detail.value.id })
  if (idx !== -1) items.value[idx].caption = detail.value.caption
}

async function delItem() {
  if (!confirm('确认删除？')) return
  await api.delete('/media/' + detail.value.id)
  items.value = items.value.filter(function(m) { return m.id !== detail.value.id })
  detail.value = null
  toast('已删除')
}

function copy(text) {
  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(text).then(function() { toast('已复制') }).catch(function() { fallbackCopy(text) })
  } else {
    fallbackCopy(text)
  }
}

function fallbackCopy(text) {
  var ta = document.createElement('textarea')
  ta.value = text
  ta.style.cssText = 'position:fixed;top:-9999px;left:-9999px;opacity:0'
  document.body.appendChild(ta)
  ta.focus()
  ta.select()
  try { document.execCommand('copy'); toast('已复制') }
  catch (e) { toast('复制失败，请手动复制', 'error') }
  document.body.removeChild(ta)
}

function drawVideoThumb(el, url) {
  if (!el || !url) return
  var video = document.createElement('video')
  video.src = url
  video.muted = true
  video.preload = 'metadata'
  video.onloadeddata = function() { video.currentTime = 1 }
  video.onseeked = function() {
    try {
      var ctx = el.getContext('2d')
      el.width = video.videoWidth || 320
      el.height = video.videoHeight || 180
      ctx.drawImage(video, 0, 0, el.width, el.height)
    } catch (e) { /* ignore */ }
    video.src = ''
  }
  video.onerror = function() { video.src = '' }
  video.load()
}

function fmtDate(iso) {
  return new Date(iso).toLocaleDateString('zh-CN')
}

onMounted(function() { load(1) })
</script>

<style scoped>
.media-page { display: flex; flex-direction: column; gap: 16px; }
.toolbar { display: flex; align-items: center; justify-content: space-between; padding: 14px 20px; flex-wrap: wrap; gap: 12px; }
.toolbar-left { display: flex; align-items: center; gap: 16px; flex-wrap: wrap; }
.page-title { font-size: 18px; font-weight: 600; }
.filter-tabs { display: flex; gap: 4px; }
.tab { padding: 5px 14px; border-radius: 20px; border: 1px solid var(--border); background: none; color: var(--text-secondary); font-size: 13px; cursor: pointer; transition: all 0.2s; }
.tab.active, .tab:hover { border-color: var(--accent); color: var(--accent); background: rgba(79,195,247,0.08); }
.upload-label { cursor: pointer; }
.hidden-input { display: none; }
.upload-progress { padding: 12px 20px; display: flex; align-items: center; gap: 12px; }
.progress-bar { flex: 1; height: 6px; background: var(--border); border-radius: 3px; overflow: hidden; }
.progress-fill { height: 100%; background: linear-gradient(90deg, var(--accent), var(--accent-2)); transition: width 0.3s; }
.status-card { padding: 60px; text-align: center; color: var(--text-muted); }
.media-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 12px; }
.media-item { cursor: pointer; overflow: hidden; transition: all 0.2s; }
.media-item:hover { border-color: var(--accent); transform: translateY(-2px); }
.media-thumb { height: 120px; overflow: hidden; background: var(--bg-secondary); }
.media-thumb img { width: 100%; height: 100%; object-fit: cover; }
.video-thumb { position: relative; width: 100%; height: 100%; background: #0a0c14; display: flex; align-items: center; justify-content: center; }
.video-canvas { width: 100%; height: 100%; object-fit: cover; display: block; }
.video-badge { position: absolute; bottom: 6px; right: 6px; background: rgba(0,0,0,0.65); color: #fff; font-size: 10px; padding: 2px 7px; border-radius: 4px; }
.media-info { padding: 8px 10px; }
.media-name { font-size: 12px; color: var(--text-secondary); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.media-date { font-size: 11px; color: var(--text-muted); margin-top: 2px; }
.pagination { display: flex; align-items: center; justify-content: center; gap: 16px; }
.page-info { font-size: 14px; color: var(--text-secondary); }
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
.meta-row { display: flex; flex-direction: column; gap: 6px; }
.meta-row label { font-size: 12px; color: var(--text-muted); }
.field-input { width: 100%; padding: 8px 12px; background: var(--bg-primary); border: 1px solid var(--border); border-radius: var(--radius); color: var(--text-primary); font-size: 13px; outline: none; transition: border-color 0.2s; }
.field-input:focus { border-color: var(--accent); }
.copy-row { display: flex; gap: 8px; }
.copy-row .field-input { flex: 1; min-width: 0; }
.del-btn { width: 100%; justify-content: center; margin-top: 4px; }
@media (max-width: 768px) {
  .modal { flex-direction: column; }
  .modal-meta { width: 100%; }
  .media-grid { grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); }
}
</style>
