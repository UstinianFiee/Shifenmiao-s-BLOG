<template>
  <div class="running-time">
    <span class="label">博客已运行</span>
    <span class="time">{{ display }}</span>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import api from '../../api'

const display = ref('--')
let startDate = null
let timer = null

function calc() {
  if (!startDate) return
  const diff = Date.now() - startDate.getTime()
  const d = Math.floor(diff / 86400000)
  const h = Math.floor((diff % 86400000) / 3600000)
  const m = Math.floor((diff % 3600000) / 60000)
  const s = Math.floor((diff % 60000) / 1000)
  display.value = `${d} 天 ✦ ${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`
}

onMounted(async () => {
  try {
    const res = await api.get('/site/info')
    // 明确按北京时间 UTC+8 解析，避免浏览器当 UTC 处理偏差8小时
    const [y, m, d] = res.data.blog_start_date.split('-').map(Number)
    startDate = new Date(y, m - 1, d, 0, 0, 0)  // 本地时间午夜
  } catch {
    startDate = new Date(2025, 0, 1)
  }
  calc()
  timer = setInterval(calc, 1000)
})
onUnmounted(() => clearInterval(timer))
</script>

<style scoped>
.running-time { display: flex; align-items: center; gap: 10px; font-size: 13px; }
.label { color: var(--text-muted); }
.time { color: var(--accent); font-variant-numeric: tabular-nums; letter-spacing: 1px; }
</style>
