<template>
  <teleport to="body">
    <transition-group name="toast" tag="div" class="toast-container">
      <div v-for="t in toasts" :key="t.id" :class="['toast', t.type]">
        <span class="toast-icon">{{ { success: '✓', error: '✕', info: '◎' }[t.type] }}</span>
        <span>{{ t.msg }}</span>
      </div>
    </transition-group>
  </teleport>
</template>

<script setup>
import { useToast } from '../stores/toast'
const { toasts } = useToast()
</script>

<style scoped>
.toast-container {
  position: fixed; top: 72px; left: 50%; transform: translateX(-50%);
  z-index: 9999; display: flex; flex-direction: column; align-items: center; gap: 10px;
  pointer-events: none; min-width: 200px;
}
.toast {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 22px; border-radius: 24px;
  font-size: 14px; font-weight: 500; white-space: nowrap;
  backdrop-filter: blur(16px);
  box-shadow: 0 4px 24px rgba(0,0,0,0.2);
}
.toast.success { background: rgba(79,195,247,0.15); border: 1px solid rgba(79,195,247,0.45); color: #4fc3f7; }
.toast.error   { background: rgba(239,68,68,0.15);  border: 1px solid rgba(239,68,68,0.45);  color: #ef4444; }
.toast.info    { background: rgba(124,77,255,0.15); border: 1px solid rgba(124,77,255,0.45); color: #a78bfa; }
[data-theme="light"] .toast.success { background: rgba(37,99,235,0.1); border-color: rgba(37,99,235,0.35); color: #2563eb; }
[data-theme="light"] .toast.error   { background: rgba(239,68,68,0.1); border-color: rgba(239,68,68,0.35); }
[data-theme="light"] .toast.info    { background: rgba(124,77,255,0.1); border-color: rgba(124,77,255,0.35); color: #7c3aed; }
.toast-icon { font-size: 14px; }
.toast-enter-active { animation: toastIn 0.3s cubic-bezier(0.34,1.56,0.64,1); }
.toast-leave-active { animation: toastOut 0.25s ease forwards; }
@keyframes toastIn  { from { opacity:0; transform:translateY(-14px) scale(0.88); } to { opacity:1; transform:translateY(0) scale(1); } }
@keyframes toastOut { to   { opacity:0; transform:translateY(-8px) scale(0.94); } }
</style>
