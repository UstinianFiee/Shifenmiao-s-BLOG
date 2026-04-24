<template>
  <div class="combo-wrap" ref="wrap">
    <div class="combo-input-row">
      <input
        v-model="inputVal"
        class="combo-input"
        :placeholder="placeholder"
        @focus="open = true; checkPosition()"
        @input="open = true; checkPosition()"
        @keydown.esc="open = false"
        @keydown.enter.prevent="selectHighlight"
        @keydown.down.prevent="moveHighlight(1)"
        @keydown.up.prevent="moveHighlight(-1)"
      />
      <button class="combo-arrow" @click.stop="toggle" tabindex="-1">
        <svg :class="['arrow-icon', { open }]" xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>
      </button>
    </div>

    <transition name="dropdown">
      <div v-if="open && filtered.length" class="combo-dropdown" :class="{ 'drop-up': dropUp }">
        <div
          v-for="(item, i) in filtered"
          :key="item"
          :class="['combo-option', { highlighted: i === highlightIdx }]"
          @mousedown.prevent="select(item)"
          @mouseover="highlightIdx = i"
        >{{ item }}</div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  modelValue: { type: String, default: '' },
  options: { type: Array, default: () => [] },
  placeholder: { type: String, default: '' },
})
const emit = defineEmits(['update:modelValue'])

const inputVal = ref(props.modelValue)
const open = ref(false)
const highlightIdx = ref(-1)
const wrap = ref(null)
const dropUp = ref(false)

function checkPosition() {
  if (!wrap.value) return
  const rect = wrap.value.getBoundingClientRect()
  const spaceBelow = window.innerHeight - rect.bottom
  dropUp.value = spaceBelow < 240 && rect.top > 240
}

watch(() => props.modelValue, v => { inputVal.value = v })
watch(inputVal, v => emit('update:modelValue', v))

const filtered = computed(() => {
  const q = inputVal.value.toLowerCase()
  return props.options.filter(o => o.toLowerCase().includes(q))
})

function select(item) {
  inputVal.value = item
  emit('update:modelValue', item)
  open.value = false
  highlightIdx.value = -1
}

function toggle() {
  open.value = !open.value
  if (open.value) checkPosition()
  highlightIdx.value = -1
}

function selectHighlight() {
  if (highlightIdx.value >= 0 && filtered.value[highlightIdx.value]) {
    select(filtered.value[highlightIdx.value])
  } else {
    open.value = false
  }
}

function moveHighlight(dir) {
  const len = filtered.value.length
  if (!len) return
  highlightIdx.value = (highlightIdx.value + dir + len) % len
}

function onClickOutside(e) {
  if (wrap.value && !wrap.value.contains(e.target)) open.value = false
}

onMounted(() => document.addEventListener('mousedown', onClickOutside))
onUnmounted(() => document.removeEventListener('mousedown', onClickOutside))
</script>

<style scoped>
.combo-wrap { position: relative; width: 100%; }

.combo-input-row {
  display: flex; align-items: center;
  background: var(--bg-primary); border: 1px solid var(--border);
  border-radius: var(--radius); transition: border-color 0.2s, box-shadow 0.2s;
  overflow: hidden;
}
.combo-input-row:focus-within {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-glow);
}
.combo-input {
  flex: 1; padding: 9px 12px;
  background: none; border: none; outline: none;
  color: var(--text-primary); font-size: 14px;
}
.combo-arrow {
  padding: 0 10px; background: none; border: none;
  cursor: pointer; color: var(--text-muted); display: flex; align-items: center;
  transition: color 0.2s;
}
.combo-arrow:hover { color: var(--accent); }
.arrow-icon { transition: transform 0.2s; }
.arrow-icon.open { transform: rotate(180deg); }

.combo-dropdown {
  position: absolute; top: calc(100% + 6px); left: 0; right: 0; z-index: 300;
  background: var(--bg-card); border: 1px solid var(--border-glow);
  border-radius: var(--radius); box-shadow: 0 8px 32px rgba(0,0,0,0.3);
  max-height: 220px; overflow-y: auto;
}
.combo-dropdown.drop-up {
  top: auto;
  bottom: calc(100% + 6px);
  box-shadow: 0 -8px 32px rgba(0,0,0,0.3);
}
[data-theme="light"] .combo-dropdown { box-shadow: 0 8px 24px rgba(37,99,235,0.12); }

/* 滚动条 */
.combo-dropdown::-webkit-scrollbar { width: 4px; }
.combo-dropdown::-webkit-scrollbar-track { background: transparent; }
.combo-dropdown::-webkit-scrollbar-thumb { background: var(--accent-2); border-radius: 2px; }

.combo-option {
  padding: 9px 14px; font-size: 13px; color: var(--text-secondary);
  cursor: pointer; transition: all 0.15s;
  border-bottom: 1px solid var(--border);
}
.combo-option:last-child { border-bottom: none; }
.combo-option:hover, .combo-option.highlighted {
  background: rgba(79,195,247,0.1); color: var(--accent);
}
[data-theme="light"] .combo-option:hover,
[data-theme="light"] .combo-option.highlighted {
  background: rgba(37,99,235,0.08); color: var(--accent);
}

/* 动画 */
.dropdown-enter-active { animation: dropIn 0.18s cubic-bezier(0.34,1.56,0.64,1); }
.dropdown-leave-active { animation: dropOut 0.14s ease forwards; }
@keyframes dropIn  { from { opacity:0; transform:translateY(-6px) scaleY(0.95); } to { opacity:1; transform:translateY(0) scaleY(1); } }
@keyframes dropOut { to   { opacity:0; transform:translateY(-4px) scaleY(0.97); } }
</style>
