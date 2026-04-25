<template>
  <div class="music-player" :class="{ expanded, minimized: !expanded }">
    <audio ref="audioEl" @timeupdate="onTimeUpdate" @ended="next" @loadedmetadata="onLoaded"></audio>

    <!-- 最小化状态：旋转唱片 -->
    <div v-if="!expanded" class="mini-disc" @click="expanded = true" :title="current?.title || '音乐播放器'">
      <div class="disc-ring" :class="{ spinning: playing }">
        <img v-if="current?.cover" :src="current.cover" class="disc-cover" />
        <span v-else class="disc-icon">♪</span>
      </div>
    </div>

    <!-- 展开状态 -->
    <div v-else class="player-panel">
      <!-- 头部 -->
      <div class="player-header">
        <span class="player-title">🎵 播放列表</span>
        <button class="icon-btn" @click="expanded = false" title="收起">╌</button>
      </div>

      <!-- 当前曲目信息 -->
      <div class="now-playing" v-if="current">
        <div class="np-cover">
          <img v-if="current.cover" :src="current.cover" />
          <span v-else class="np-icon">♪</span>
          <div class="np-spin-ring" :class="{ spinning: playing }"></div>
        </div>
        <div class="np-info">
          <p class="np-title">{{ current.title }}</p>
          <p class="np-artist">{{ current.artist || '未知艺术家' }}</p>
        </div>
      </div>
      <div class="now-playing empty" v-else>
        <p>暂无曲目，请在后台添加</p>
      </div>

      <!-- 进度条 -->
      <div class="progress-wrap" @click="seek">
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: progress + '%' }"></div>
        </div>
        <div class="time-row">
          <span>{{ formatTime(currentTime) }}</span>
          <span>{{ formatTime(duration) }}</span>
        </div>
      </div>

      <!-- 控制按钮 -->
      <div class="controls">
        <button class="ctrl-btn" @click="toggleMode" :title="modeLabel">{{ modeIcon }}</button>
        <button class="ctrl-btn" @click="prev">⏮</button>
        <button class="ctrl-btn play-btn" @click="togglePlay">
          {{ playing ? '⏸' : '▶' }}
        </button>
        <button class="ctrl-btn" @click="next">⏭</button>
        <div class="volume-wrap">
          <span class="ctrl-btn" @click="toggleMute">{{ muted ? '🔇' : '🔊' }}</span>
          <input type="range" min="0" max="1" step="0.05" v-model="volume" class="volume-slider" @input="setVolume" />
        </div>
      </div>

      <!-- 播放列表 -->
      <div class="playlist">
        <div
          v-for="(item, i) in playlist"
          :key="item.id"
          :class="['pl-item', { active: currentIdx === i }]"
          @click="playAt(i)"
        >
          <span class="pl-num">{{ currentIdx === i && playing ? '▶' : i + 1 }}</span>
          <div class="pl-info">
            <span class="pl-title">{{ item.title }}</span>
            <span class="pl-artist">{{ item.artist }}</span>
          </div>
        </div>
        <div v-if="!playlist.length" class="pl-empty">暂无曲目</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import api from '../api'

const audioEl = ref(null)
const playlist = ref([])
const currentIdx = ref(0)
const playing = ref(false)
const expanded = ref(false)
const currentTime = ref(0)
const duration = ref(0)
const volume = ref(0.7)
const muted = ref(false)
const mode = ref('list') // list | random | single

const current = computed(() => playlist.value[currentIdx.value] || null)
const progress = computed(() => duration.value ? (currentTime.value / duration.value) * 100 : 0)
const modeIcon = computed(() => ({ list: '🔁', random: '🔀', single: '🔂' }[mode.value]))
const modeLabel = computed(() => ({ list: '列表循环', random: '随机播放', single: '单曲循环' }[mode.value]))

function toggleMode() {
  mode.value = { list: 'random', random: 'single', single: 'list' }[mode.value]
}

async function loadPlaylist() {
  const res = await api.get('/playlist')
  playlist.value = res.data
}

function playAt(i) {
  currentIdx.value = i
  playing.value = true
}

watch(current, (song) => {
  if (!song || !audioEl.value) return
  audioEl.value.src = song.url
  if (playing.value) audioEl.value.play().catch(() => {})
})

watch(playing, (v) => {
  if (!audioEl.value) return
  v ? audioEl.value.play().catch(() => {}) : audioEl.value.pause()
})

function togglePlay() { playing.value = !playing.value }

function prev() {
  if (!playlist.value.length) return
  currentIdx.value = (currentIdx.value - 1 + playlist.value.length) % playlist.value.length
  playing.value = true
}

function next() {
  if (!playlist.value.length) return
  if (mode.value === 'single') {
    audioEl.value.currentTime = 0
    audioEl.value.play().catch(() => {})
    return
  }
  if (mode.value === 'random') {
    currentIdx.value = Math.floor(Math.random() * playlist.value.length)
  } else {
    currentIdx.value = (currentIdx.value + 1) % playlist.value.length
  }
  playing.value = true
}

function onTimeUpdate() { currentTime.value = audioEl.value?.currentTime || 0 }
function onLoaded() { duration.value = audioEl.value?.duration || 0 }

function seek(e) {
  if (!audioEl.value || !duration.value) return
  const rect = e.currentTarget.querySelector('.progress-bar').getBoundingClientRect()
  const ratio = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width))
  audioEl.value.currentTime = ratio * duration.value
}

function setVolume() {
  if (audioEl.value) { audioEl.value.volume = volume.value; muted.value = false }
}
function toggleMute() {
  muted.value = !muted.value
  if (audioEl.value) audioEl.value.muted = muted.value
}

function formatTime(s) {
  if (!s || isNaN(s)) return '0:00'
  const m = Math.floor(s / 60)
  const sec = Math.floor(s % 60)
  return `${m}:${String(sec).padStart(2, '0')}`
}

onMounted(() => {
  loadPlaylist()
  if (audioEl.value) audioEl.value.volume = volume.value
})
</script>

<style scoped>
.music-player {
  position: fixed; bottom: 80px; right: 20px; z-index: 500;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 最小化唱片 */
.mini-disc {
  width: 52px; height: 52px; cursor: pointer;
  filter: drop-shadow(0 4px 12px var(--accent-glow));
  transition: transform 0.3s;
}
.mini-disc:hover { transform: scale(1.1); }
.disc-ring {
  width: 52px; height: 52px; border-radius: 50%;
  background: linear-gradient(135deg, var(--accent), var(--accent-2));
  display: flex; align-items: center; justify-content: center;
  border: 2px solid rgba(255,255,255,0.2);
  overflow: hidden;
}
.disc-ring.spinning { animation: spin 4s linear infinite; }
.disc-cover { width: 100%; height: 100%; object-fit: cover; border-radius: 50%; }
.disc-icon { font-size: 22px; color: #fff; }
@keyframes spin { to { transform: rotate(360deg); } }

/* 展开面板 */
.player-panel {
  width: 300px;
  background: var(--bg-card);
  border: 1px solid var(--border-glow);
  border-radius: 16px;
  box-shadow: 0 8px 40px rgba(0,0,0,0.4);
  overflow: hidden;
  backdrop-filter: blur(16px);
}
[data-theme="light"] .player-panel { box-shadow: 0 8px 32px rgba(37,99,235,0.15); }

.player-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 12px 16px 8px;
  border-bottom: 1px solid var(--border);
}
.player-title { font-size: 13px; font-weight: 600; color: var(--text-secondary); }
.icon-btn { background: none; border: none; color: var(--text-muted); cursor: pointer; font-size: 18px; line-height: 1; transition: color 0.2s; }
.icon-btn:hover { color: var(--accent); }

/* 当前曲目 */
.now-playing { display: flex; align-items: center; gap: 12px; padding: 14px 16px; }
.now-playing.empty { justify-content: center; color: var(--text-muted); font-size: 13px; }
.np-cover {
  width: 48px; height: 48px; border-radius: 50%; flex-shrink: 0;
  background: linear-gradient(135deg, var(--accent), var(--accent-2));
  display: flex; align-items: center; justify-content: center;
  overflow: hidden; position: relative;
}
.np-cover img { width: 100%; height: 100%; object-fit: cover; }
.np-icon { font-size: 20px; color: #fff; }
.np-spin-ring {
  position: absolute; inset: -2px; border-radius: 50%;
  border: 2px solid transparent;
  border-top-color: var(--accent);
}
.np-spin-ring.spinning { animation: spin 2s linear infinite; }
.np-info { flex: 1; min-width: 0; }
.np-title { font-size: 14px; font-weight: 500; color: var(--text-primary); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.np-artist { font-size: 12px; color: var(--text-muted); margin-top: 2px; }

/* 进度条 */
.progress-wrap { padding: 0 16px 4px; cursor: pointer; }
.progress-bar { height: 3px; background: var(--border); border-radius: 2px; overflow: hidden; }
.progress-fill { height: 100%; background: linear-gradient(90deg, var(--accent), var(--accent-2)); border-radius: 2px; transition: width 0.3s linear; }
.time-row { display: flex; justify-content: space-between; font-size: 11px; color: var(--text-muted); margin-top: 4px; }

/* 控制 */
.controls { display: flex; align-items: center; justify-content: center; gap: 8px; padding: 8px 16px 10px; }
.ctrl-btn { background: none; border: none; cursor: pointer; font-size: 18px; color: var(--text-secondary); transition: all 0.2s; padding: 4px; border-radius: 50%; }
.ctrl-btn:hover { color: var(--accent); transform: scale(1.15); }
.play-btn { font-size: 22px; color: var(--accent); }
.volume-wrap { display: flex; align-items: center; gap: 4px; margin-left: 4px; }
.volume-slider { width: 60px; height: 3px; accent-color: var(--accent); cursor: pointer; }

/* 播放列表 */
.playlist { max-height: 180px; overflow-y: auto; border-top: 1px solid var(--border); }
.playlist::-webkit-scrollbar { width: 3px; }
.playlist::-webkit-scrollbar-thumb { background: var(--accent-2); border-radius: 2px; }
.pl-item { display: flex; align-items: center; gap: 10px; padding: 8px 16px; cursor: pointer; transition: background 0.2s; }
.pl-item:hover { background: var(--bg-card-hover); }
.pl-item.active { background: rgba(79,195,247,0.1); }
[data-theme="light"] .pl-item.active { background: rgba(37,99,235,0.08); }
.pl-num { font-size: 12px; color: var(--text-muted); width: 18px; text-align: center; flex-shrink: 0; }
.pl-item.active .pl-num { color: var(--accent); }
.pl-info { flex: 1; min-width: 0; }
.pl-title { font-size: 13px; color: var(--text-primary); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; display: block; }
.pl-item.active .pl-title { color: var(--accent); }
.pl-artist { font-size: 11px; color: var(--text-muted); }
.pl-empty { padding: 20px; text-align: center; color: var(--text-muted); font-size: 13px; }

@media (max-width: 768px) {
  .music-player { bottom: 70px; right: 12px; }
  .player-panel { width: 280px; }
}
</style>
