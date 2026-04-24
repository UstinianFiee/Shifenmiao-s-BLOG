<template>
  <div class="login-page">
    <canvas id="particles-canvas" ref="canvas"></canvas>
    <div class="login-card card fade-in-up">
      <div class="login-logo">
        <span class="logo-bracket">[</span>BLOG<span class="logo-bracket">]</span>
      </div>
      <p class="login-sub">管理后台</p>
      <form @submit.prevent="submit">
        <div class="field">
          <label>用户名</label>
          <input v-model="form.username" type="text" autocomplete="username" required />
        </div>
        <div class="field">
          <label>密码</label>
          <div class="pwd-wrap">
            <input v-model="form.password" :type="showPwd ? 'text' : 'password'" autocomplete="current-password" required />
            <button type="button" class="pwd-toggle" @click="showPwd = !showPwd">
              <svg v-if="showPwd" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/>
                <path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/>
                <line x1="1" y1="1" x2="23" y2="23"/>
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                <circle cx="12" cy="12" r="3"/>
              </svg>
            </button>
          </div>
        </div>
        <p v-if="error" class="error-msg">{{ error }}</p>
        <button class="btn btn-primary" style="width:100%;justify-content:center" :disabled="loading">
          {{ loading ? '登录中...' : '登 录' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'

const auth = useAuthStore()
const router = useRouter()
const form = ref({ username: '', password: '' })
const error = ref('')
const loading = ref(false)
const showPwd = ref(false)
const canvas = ref(null)
let animId = null

async function submit() {
  error.value = ''
  loading.value = true
  try {
    await auth.login(form.value.username, form.value.password)
    router.push('/admin')
  } catch {
    error.value = '用户名或密码错误'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  const c = canvas.value
  const ctx = c.getContext('2d')
  let W = c.width = window.innerWidth
  let H = c.height = window.innerHeight
  const resize = () => { W = c.width = window.innerWidth; H = c.height = window.innerHeight }
  window.addEventListener('resize', resize)
  const particles = Array.from({ length: 60 }, () => ({
    x: Math.random() * W, y: Math.random() * H,
    r: Math.random() * 1.2 + 0.3,
    vx: (Math.random() - 0.5) * 0.3, vy: (Math.random() - 0.5) * 0.3,
    alpha: Math.random() * 0.4 + 0.1,
  }))
  const draw = () => {
    ctx.clearRect(0, 0, W, H)
    particles.forEach(p => {
      p.x += p.vx; p.y += p.vy
      if (p.x < 0) p.x = W; if (p.x > W) p.x = 0
      if (p.y < 0) p.y = H; if (p.y > H) p.y = 0
      ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2)
      ctx.fillStyle = `rgba(79,195,247,${p.alpha})`; ctx.fill()
    })
    animId = requestAnimationFrame(draw)
  }
  draw()
  onUnmounted(() => { cancelAnimationFrame(animId); window.removeEventListener('resize', resize) })
})
</script>

<style scoped>
.login-page {
  min-height: 100vh; display: flex; align-items: center; justify-content: center;
  background: var(--bg-primary); position: relative;
}
#particles-canvas { position: fixed; inset: 0; pointer-events: none; z-index: 0; }
.login-card { position: relative; z-index: 1; width: 360px; padding: 40px; }
.login-logo { font-size: 24px; font-weight: 700; letter-spacing: 4px; text-align: center; margin-bottom: 4px; }
.logo-bracket { color: var(--accent); }
.login-sub { text-align: center; color: var(--text-muted); font-size: 13px; margin-bottom: 32px; letter-spacing: 2px; }
.field { margin-bottom: 20px; }
.field label { display: block; font-size: 13px; color: var(--text-secondary); margin-bottom: 6px; }
.field input {
  width: 100%; padding: 10px 14px;
  background: var(--bg-primary); border: 1px solid var(--border);
  border-radius: var(--radius); color: var(--text-primary); font-size: 14px;
  outline: none; transition: border-color 0.3s;
}
.field input:focus { border-color: var(--accent); }
.pwd-wrap { position: relative; }
.pwd-wrap input { width: 100%; padding: 10px 56px 10px 14px; background: var(--bg-primary); border: 1px solid var(--border); border-radius: var(--radius); color: var(--text-primary); font-size: 14px; outline: none; transition: border-color 0.3s; }
.pwd-wrap input:focus { border-color: var(--accent); }
.pwd-toggle { position: absolute; right: 10px; top: 50%; transform: translateY(-50%); background: none; border: none; color: var(--text-muted); cursor: pointer; padding: 4px; border-radius: 4px; display: flex; align-items: center; transition: color 0.2s; }
.pwd-toggle:hover { color: var(--accent); }
.error-msg { color: #ff5252; font-size: 13px; margin-bottom: 12px; }
</style>
