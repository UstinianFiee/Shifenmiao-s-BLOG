import { ref } from 'vue'

const toasts = ref([])
let seq = 0

export function useToast() {
  function show(msg, type = 'success', duration = 2500) {
    const id = ++seq
    toasts.value.push({ id, msg, type })
    setTimeout(() => {
      toasts.value = toasts.value.filter(t => t.id !== id)
    }, duration)
  }
  return { toasts, show }
}
