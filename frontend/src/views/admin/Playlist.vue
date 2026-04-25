<template>
  <div class="playlist-page">
    <!-- 工具栏 -->
    <div class="toolbar card">
      <h2 class="page-title">🎵 播放列表</h2>
      <button class="btn btn-primary" @click="showAdd = true">+ 添加曲目</button>
    </div>

    <!-- 列表 -->
    <div class="list-wrap card">
      <div v-for="item in list" :key="item.id" class="pl-row">
        <div class="pl-cover">
          <img v-if="item.cover" :src="item.cover" />
          <span v-else>♪</span>
        </div>
        <div class="pl-info">
          <p class="pl-title">{{ item.title }}</p>
          <p class="pl-artist">{{ item.artist || '未知艺术家' }}</p>
          <p class="pl-url">{{ item.url }}</p>
        </div>
        <div class="pl-actions">
          <button class="btn" style="padding:4px 10px;font-size:12px" @click="startEdit(item)">编辑</button>
          <button class="btn btn-danger" style="padding:4px 10px;font-size:12px" @click="del(item.id)">删除</button>
        </div>
      </div>
      <div v-if="!list.length" class="empty">暂无曲目，点击「添加曲目」上传音乐</div>
    </div>

    <!-- 添加/编辑弹窗 -->
    <div v-if="showAdd || editItem" class="modal-mask" @click.self="closeForm">
      <div class="modal card">
        <h3 class="modal-title">{{ editItem ? '编辑曲目' : '添加曲目' }}</h3>

        <div class="form-fields">
          <div class="field-group">
            <label>曲目名称 *</label>
            <input v-model="form.title" class="field-input" placeholder="歌曲名" />
          </div>
          <div class="field-group">
            <label>艺术家</label>
            <input v-model="form.artist" class="field-input" placeholder="歌手/乐队" />
          </div>
          <div class="field-group">
            <label>音频文件 *</label>
            <div class="upload-row">
              <input v-model="form.url" class="field-input" placeholder="上传后自动填入，或手动输入路径" readonly />
              <label class="btn upload-btn">
                {{ audioUploading ? '上传中...' : '上传音频' }}
                <input type="file" accept="audio/*" @change="uploadAudio" class="hidden-input" :disabled="audioUploading" />
              </label>
            </div>
            <audio v-if="form.url" :src="form.url" controls class="audio-preview"></audio>
          </div>
          <div class="field-group">
            <label>封面图（可选）</label>
            <div class="upload-row">
              <input v-model="form.cover" class="field-input" placeholder="上传后自动填入，或手动输入路径" readonly />
              <label class="btn upload-btn">
                上传封面
                <input type="file" accept="image/*" @change="uploadCover" class="hidden-input" />
              </label>
            </div>
            <img v-if="form.cover" :src="form.cover" class="cover-preview" />
          </div>
        </div>

        <div class="modal-actions">
          <button class="btn btn-primary" @click="save">保存</button>
          <button class="btn" @click="closeForm">取消</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api'
import { useToast } from '../../stores/toast'

const { show: toast } = useToast()
const list = ref([])
const showAdd = ref(false)
const editItem = ref(null)
const audioUploading = ref(false)

const form = ref({ title: '', artist: '', url: '', cover: '' })

async function load() {
  const res = await api.get('/playlist')
  list.value = res.data
}

function startEdit(item) {
  editItem.value = item
  form.value = { title: item.title, artist: item.artist, url: item.url, cover: item.cover }
}

function closeForm() {
  showAdd.value = false
  editItem.value = null
  form.value = { title: '', artist: '', url: '', cover: '' }
}

async function uploadAudio(e) {
  const file = e.target.files[0]
  if (!file) return
  audioUploading.value = true
  const fd = new FormData()
  fd.append('file', file)
  const res = await api.post('/upload', fd)
  form.value.url = res.data.url
  if (!form.value.title) form.value.title = file.name.replace(/\.[^.]+$/, '')
  audioUploading.value = false
}

async function uploadCover(e) {
  const file = e.target.files[0]
  if (!file) return
  const fd = new FormData()
  fd.append('file', file)
  const res = await api.post('/upload', fd)
  form.value.cover = res.data.url
}

async function save() {
  if (!form.value.title || !form.value.url) { toast('请填写曲目名称和音频文件', 'error'); return }
  if (editItem.value) {
    await api.put(`/playlist/${editItem.value.id}`, form.value)
    toast('修改成功')
  } else {
    await api.post('/playlist', form.value)
    toast('添加成功')
  }
  closeForm()
  load()
}

async function del(id) {
  if (!confirm('确认删除？')) return
  await api.delete(`/playlist/${id}`)
  toast('已删除')
  load()
}

onMounted(load)
</script>

<style scoped>
.playlist-page { display: flex; flex-direction: column; gap: 16px; }
.toolbar { display: flex; align-items: center; justify-content: space-between; padding: 16px 20px; }
.page-title { font-size: 18px; font-weight: 600; }
.list-wrap { overflow: hidden; }
.pl-row { display: flex; align-items: center; gap: 14px; padding: 14px 20px; border-bottom: 1px solid var(--border); flex-wrap: wrap; }
.pl-row:last-child { border-bottom: none; }
.pl-cover { width: 44px; height: 44px; border-radius: 50%; background: linear-gradient(135deg, var(--accent), var(--accent-2)); display: flex; align-items: center; justify-content: center; overflow: hidden; flex-shrink: 0; font-size: 18px; color: #fff; }
.pl-cover img { width: 100%; height: 100%; object-fit: cover; }
.pl-info { flex: 1; min-width: 0; }
.pl-title { font-size: 14px; font-weight: 500; color: var(--text-primary); }
.pl-artist { font-size: 12px; color: var(--text-muted); }
.pl-url { font-size: 11px; color: var(--text-muted); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.pl-actions { display: flex; gap: 8px; flex-shrink: 0; }
.empty { padding: 40px; text-align: center; color: var(--text-muted); }

@media (max-width: 768px) {
  .pl-row { align-items: flex-start; }
  .pl-actions { width: 100%; padding-left: 58px; }
}

/* 弹窗 */
.modal-mask { position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 400; display: flex; align-items: center; justify-content: center; padding: 20px; }
.modal { width: 100%; max-width: 480px; padding: 24px; }
.modal-title { font-size: 16px; font-weight: 600; margin-bottom: 20px; }
.form-fields { display: flex; flex-direction: column; gap: 16px; }
.field-group { display: flex; flex-direction: column; gap: 6px; }
.field-group label { font-size: 13px; color: var(--text-secondary); }
.field-input { width: 100%; padding: 9px 12px; background: var(--bg-primary); border: 1px solid var(--border); border-radius: var(--radius); color: var(--text-primary); font-size: 14px; outline: none; transition: border-color 0.2s; }
.field-input:focus { border-color: var(--accent); }
.upload-row { display: flex; gap: 8px; }
.upload-row .field-input { flex: 1; }
.upload-btn { cursor: pointer; white-space: nowrap; flex-shrink: 0; }
.hidden-input { display: none; }
.audio-preview { width: 100%; margin-top: 8px; height: 36px; }
.cover-preview { width: 80px; height: 80px; border-radius: 50%; object-fit: cover; margin-top: 8px; }
.modal-actions { display: flex; gap: 10px; margin-top: 20px; justify-content: flex-end; }
</style>
