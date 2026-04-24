import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './styles/global.css'

const app = createApp(App)
const pinia = createPinia()
app.use(pinia)
app.use(router)

// 初始化主题（mount 前执行，避免闪烁）
import { useThemeStore } from './stores/theme'
useThemeStore(pinia).apply()

app.mount('#app')
