<template>
  <teleport to="body">
    <transition-group name="toast" tag="div" class="toast-container">
      <div v-for="t in toasts" :key="t.id" :class="['toast', t.type]">
        <span class="toast-icon">{{ icons[t.type] }}</span>
        <span class="toast-msg">{{ t.msg }}</span>
      </div>
    </transition-group>
  </teleport>
</template>

<script setup>
import { ref } from 'vue'

const toasts = ref([])
const icons = { success: '✓', error: '✕', info: '◎' }
let seq = 0

function show(msg, type = 'success', duration = 2500) {
  const id = ++seq
  toasts.value.push({ id, msg, type })
  setTimeout(() => {
    toasts.value = toasts.value.filter(t => t.id !== id)
  }, duration)
}

defineExpose({ show })
</script>

<style scoped>
.toast-container {
  position: fixed; top: 72px; left: 50%; transform: translateX(-50%);
  z-index: 9999; display: flex; flex-direction: column; align-items: center; gap: 10px;
  pointer-events: none;
}
.toast {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 20px; border-radius: 24px;
  font-size: 14px; font-weight: 500;
  backdrop-filter: blur(12px);
  box-shadow: 0 4px 20px rgba(0,0,0,0.25);
  pointer-events: auto;
}
.toast.success { background: rgba(79,195,247,0.15); border: 1px solid rgba(79,195,247,0.4); color: #4fc3f7; }
.toast.error   { background: rgba(239,68,68,0.15);  border: 1px solid rgba(239,68,68,0.4);  color: #ef4444; }
.toast.info    { background: rgba(124,77,255,0.15); border: 1px solid rgba(124,77,255,0.4); color: #a78bfa; }
[data-theme="light"] .toast.success { background: rgba(37,99,235,0.1); border-color: rgba(37,99,235,0.3); color: #2563eb; }
[data-theme="light"] .toast.error   { background: rgba(239,68,68,0.1); border-color: rgba(239,68,68,0.3); }
[data-theme="light"] .toast.info    { background: rgba(124,77,255,0.1); border-color: rgba(124,77,255,0.3); color: #7c3aed; }
.toast-icon { font-size: 15px; }

/* 动画 */
.toast-enter-active { animation: toastIn 0.3s cubic-bezier(0.34,1.56,0.64,1); }
.toast-leave-active { animation: toastOut 0.25s ease forwards; }
@keyframes toastIn  { from { opacity:0; transform:translateY(-12px) scale(0.9); } to { opacity:1; transform:translateY(0) scale(1); } }
@keyframes toastOut { to   { opacity:0; transform:translateY(-8px) scale(0.95); } }
</style>
