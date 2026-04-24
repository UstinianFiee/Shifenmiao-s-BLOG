import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  // 获取北京时间小时（UTC+8）
  function getBeijingHour() {
    const now = new Date()
    const utc = now.getTime() + now.getTimezoneOffset() * 60000
    const beijing = new Date(utc + 8 * 3600000)
    return beijing.getHours()
  }

  // 根据时间自动判断主题：8:00-20:00 日间，20:00-次日8:00 夜间
  function getAutoTheme() {
    const hour = getBeijingHour()
    return (hour >= 8 && hour < 20) ? 'light' : 'dark'
  }

  // 如果用户从未手动设置，用自动判断；否则用用户选择
  const stored = localStorage.getItem('theme')
  const userSet = localStorage.getItem('theme-user-set') === 'true'
  const theme = ref(userSet ? stored : getAutoTheme())

  function apply() {
    document.documentElement.setAttribute('data-theme', theme.value)
  }

  function toggle() {
    theme.value = theme.value === 'dark' ? 'light' : 'dark'
    localStorage.setItem('theme', theme.value)
    localStorage.setItem('theme-user-set', 'true')  // 标记用户手动设置过
    apply()
  }

  apply()

  return { theme, toggle, apply }
})
