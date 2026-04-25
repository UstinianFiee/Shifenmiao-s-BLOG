<template>
  <div class="front-layout" @contextmenu.prevent @selectstart="onSelectStart">
    <canvas id="particles-canvas" ref="canvas"></canvas>
    <NavBar />
    <main class="main-content">
      <router-view />
    </main>
    <FooterBar />
    <MusicPlayer />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useThemeStore } from '../stores/theme'
import NavBar from '../components/front/NavBar.vue'
import FooterBar from '../components/front/FooterBar.vue'
import MusicPlayer from '../components/MusicPlayer.vue'

const themeStore = useThemeStore()
const canvas = ref(null)
let animId = null

// 允许输入框选中，禁止其他区域选中文字
function onSelectStart(e) {
  const tag = e.target.tagName.toLowerCase()
  if (['input', 'textarea'].includes(tag)) return true
  e.preventDefault()
}

onMounted(() => {
  const c = canvas.value
  const ctx = c.getContext('2d')
  let W = c.width = window.innerWidth
  let H = c.height = window.innerHeight
  const resize = () => { W = c.width = window.innerWidth; H = c.height = window.innerHeight }
  window.addEventListener('resize', resize)

  const particles = Array.from({ length: 80 }, () => ({
    x: Math.random() * W, y: Math.random() * H,
    r: Math.random() * 1.5 + 0.3,
    vx: (Math.random() - 0.5) * 0.3,
    vy: (Math.random() - 0.5) * 0.3,
    alpha: Math.random() * 0.5 + 0.1,
  }))

  const getColor = () => themeStore.theme === 'dark' ? '79,195,247' : '37,99,235'

  const draw = () => {
    ctx.clearRect(0, 0, W, H)
    const rgb = getColor()
    particles.forEach(p => {
      p.x += p.vx; p.y += p.vy
      if (p.x < 0) p.x = W; if (p.x > W) p.x = 0
      if (p.y < 0) p.y = H; if (p.y > H) p.y = 0
      ctx.beginPath()
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2)
      ctx.fillStyle = `rgba(${rgb},${p.alpha})`
      ctx.fill()
    })
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x
        const dy = particles[i].y - particles[j].y
        const dist = Math.sqrt(dx * dx + dy * dy)
        if (dist < 120) {
          ctx.beginPath()
          ctx.moveTo(particles[i].x, particles[i].y)
          ctx.lineTo(particles[j].x, particles[j].y)
          ctx.strokeStyle = `rgba(${rgb},${0.08 * (1 - dist / 120)})`
          ctx.stroke()
        }
      }
    }
    animId = requestAnimationFrame(draw)
  }
  draw()

  onUnmounted(() => {
    cancelAnimationFrame(animId)
    window.removeEventListener('resize', resize)
  })
})
</script>

<style scoped>
.front-layout { position: relative; min-height: 100vh; }
.main-content { position: relative; z-index: 1; padding-bottom: 56px; }
</style>
