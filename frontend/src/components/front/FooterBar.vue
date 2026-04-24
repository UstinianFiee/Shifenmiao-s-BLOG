<template>
  <footer class="footer">
    <div class="footer-inner container">
      <RunningTime />
      <p class="copy">© {{ year }} 时分渺OvO · Powered by Flask &amp; Vue3</p>
    </div>
  </footer>
</template>

<script setup>
import RunningTime from './RunningTime.vue'
const year = new Date().getFullYear()
</script>

<style scoped>
.footer {
  position: fixed; bottom: 0; left: 0; right: 0; z-index: 90;
  background: var(--footer-bg);
  backdrop-filter: blur(12px);
  border-top: 1px solid var(--border);
  padding: 10px 0;
}
.footer-inner { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 4px; }
.copy { color: var(--text-muted); font-size: 12px; }
</style>
