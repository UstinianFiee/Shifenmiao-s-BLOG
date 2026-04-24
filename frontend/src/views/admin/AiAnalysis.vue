<template>
  <div class="ai-page">

    <!-- 配置卡片 -->
    <div class="section-card card">
      <div class="section-header">
        <h3 class="section-title">🤖 AI 助手配置</h3>
        <div class="header-actions">
          <button class="btn" @click="showConfig = !showConfig">{{ showConfig ? '收起' : '展开配置' }}</button>
          <span v-if="configMsg" class="config-saved-tip">{{ configMsg }}</span>
          <button class="btn btn-primary" v-if="showConfig" @click="saveConfig">保存配置</button>        </div>
      </div>
      <div v-if="showConfig" class="config-body">
        <div class="config-grid">
          <div class="field-group">
            <label>API Base URL</label>
            <input v-model="config.api_base" class="field-input" placeholder="https://api.openai.com/v1" />
            <p class="field-hint">兼容 OpenAI 格式，支持 DeepSeek、通义千问、Kimi 等</p>
          </div>
          <div class="field-group">
            <label>API Key</label>
            <div class="pwd-wrap">
              <input v-model="config.api_key" :type="showKey ? 'text' : 'password'" class="field-input" placeholder="sk-..." />
              <button type="button" class="eye-btn" @click="showKey = !showKey">
                <svg v-if="showKey" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/><path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
              </button>
            </div>
          </div>
          <div class="field-group">
            <label>模型名称</label>
            <input v-model="config.model" class="field-input" placeholder="gpt-3.5-turbo" />
            <p class="field-hint">如 deepseek-chat、qwen-turbo、moonshot-v1-8k</p>
          </div>
        </div>
        <div class="field-group" style="margin-top:16px">
          <label>近况分析 Prompt 模板 <span class="hint-tag">{articles} 代表文章内容</span></label>
          <textarea v-model="config.prompt_template" class="field-input" rows="4"></textarea>
        </div>
      </div>
      <div v-if="showConfig" class="presets">
        <p class="preset-label">快速填入服务商：</p>
        <div class="preset-btns">
          <button class="preset-btn" @click="setPreset('deepseek')">DeepSeek</button>
          <button class="preset-btn" @click="setPreset('qwen')">通义千问</button>
          <button class="preset-btn" @click="setPreset('kimi')">Kimi</button>
          <button class="preset-btn" @click="setPreset('openai')">OpenAI</button>
          <button class="preset-btn" @click="setPreset('zhipu')">智谱 GLM</button>
        </div>
      </div>
    </div>

    <!-- Tab 切换 -->
    <div class="tab-bar">
      <button :class="['tab', { active: activeTab === 'analyze' }]" @click="activeTab = 'analyze'">📊 近况分析</button>
      <button :class="['tab', { active: activeTab === 'generate' }]" @click="activeTab = 'generate'">💡 灵感一现</button>
    </div>

    <!-- 近况分析 -->
    <div v-if="activeTab === 'analyze'" class="section-card card">
      <div class="section-header">
        <h3 class="section-title">近况分析</h3>
        <button class="btn btn-primary" @click="analyze" :disabled="analyzing">
          {{ analyzing ? '分析中...' : '✨ 开始分析' }}
        </button>
      </div>
      <div v-if="!result && !analyzing" class="analyze-placeholder">
        <p>点击「开始分析」，AI 将读取你最近发布的文章，分析近况、关注话题和情绪倾向。</p>
      </div>
      <div v-if="result || analyzing" class="result-wrap">
        <textarea v-if="editing && !analyzing" v-model="result" class="result-editor" rows="6"></textarea>
        <template v-else>
          <div class="result-text" v-html="resultHtml"></div>
          <span v-if="analyzing" class="cursor-blink">▌</span>
        </template>
      </div>
      <p v-if="errMsg" class="tip error">{{ errMsg }}</p>
      <div v-if="result && !analyzing" class="result-actions">
        <button class="btn btn-primary" @click="saveToAbout" :disabled="saving">{{ saving ? '保存中...' : '📌 保存到关于页' }}</button>
        <button class="btn" @click="editing = !editing">{{ editing ? '预览' : '✏️ 编辑' }}</button>
        <button class="btn" @click="copyResult">复制</button>
        <button class="btn" @click="result = ''; editing = false; errMsg = ''">清空</button>
      </div>
    </div>

    <!-- AI 写文章 -->
    <div v-if="activeTab === 'generate'" class="section-card card">
      <div class="section-header">
        <h3 class="section-title">💡 灵感一现</h3>
        <button class="btn btn-primary" @click="generateArticle" :disabled="generating">
          {{ generating ? '生成中...' : '🚀 生成并保存' }}
        </button>
      </div>

      <div class="gen-form">
        <div class="field-group">
          <label>文章描述 <span class="required">*</span></label>
          <textarea v-model="genForm.description" class="field-input" rows="3"
            placeholder="例如：帮我写一篇关于 Flask 路由系统的入门教程，包含代码示例"></textarea>
        </div>

        <div class="gen-grid">
          <div class="field-group">
            <label>分类</label>
            <ComboBox v-model="genForm.category_name" :options="categoryNames" placeholder="选择或输入分类名，不存在自动创建" />
          </div>

          <div class="field-group">
            <label>标签 <span class="field-hint">（逗号分隔，不存在自动创建）</span></label>
            <ComboBox v-model="genTagInput" :options="tagNames" placeholder="Flask, Python, Web开发" />
          </div>

          <div class="field-group">
            <label>封面图 <span class="field-hint">（从媒体库选择或输入文件名）</span></label>
            <ComboBox v-model="genForm.cover_filename" :options="mediaNames" placeholder="选择或输入文件名" />
          </div>

          <div class="field-group">
            <label>发布状态</label>
            <select v-model="genForm.status" class="field-input">
              <option value="draft">草稿（生成后手动审核发布）</option>
              <option value="published">直接发布</option>
            </select>
          </div>
        </div>
      </div>

      <p v-if="genErr" class="tip error">{{ genErr }}</p>
      <div v-if="genResult" class="gen-result card">
        <p class="gen-result-title">✅ 文章已生成</p>
        <p class="gen-result-info">标题：<strong>{{ genResult.article.title }}</strong></p>
        <p class="gen-result-info" v-if="genResult.created_category">新建分类：{{ genResult.created_category }}</p>
        <p class="gen-result-info" v-if="genResult.created_tags?.length">新建标签：{{ genResult.created_tags.join('、') }}</p>
        <div class="gen-result-actions">
          <router-link :to="`/admin/articles/${genResult.article.id}/edit`" class="btn btn-primary">去编辑</router-link>
          <a v-if="genResult.article.status === 'published'" :href="`/article/${genResult.article.id}`" target="_blank" class="btn">查看文章</a>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../../api'
import { useToast } from '../../stores/toast'
import ComboBox from '../../components/ComboBox.vue'

const { show: toast } = useToast()

const showConfig = ref(false)
const showKey = ref(false)
const config = ref({ api_base: '', api_key: '', model: '', prompt_template: '' })
const configMsg = ref('')
const activeTab = ref('analyze')

// 近况分析
const analyzing = ref(false)
const result = ref('')
const errMsg = ref('')
const saving = ref(false)
const saveMsg = ref('')
const editing = ref(false)
const resultHtml = computed(() => result.value.replace(/\n/g, '<br>'))

// 文章生成
const generating = ref(false)
const genErr = ref('')
const genResult = ref(null)
const genTagInput = ref('')
const genForm = ref({ description: '', category_name: '', cover_filename: '', status: 'draft' })
const categories = ref([])
const tags = ref([])
const mediaList = ref([])

const categoryNames = computed(() => categories.value.map(c => c.name))
const tagNames = computed(() => tags.value.map(t => t.name))
const mediaNames = computed(() => mediaList.value.map(m => m.name))

const PRESETS = {
  deepseek: { api_base: 'https://api.deepseek.com/v1', model: 'deepseek-chat' },
  qwen:     { api_base: 'https://dashscope.aliyuncs.com/compatible-mode/v1', model: 'qwen-turbo' },
  kimi:     { api_base: 'https://api.moonshot.cn/v1', model: 'moonshot-v1-8k' },
  openai:   { api_base: 'https://api.openai.com/v1', model: 'gpt-3.5-turbo' },
  zhipu:    { api_base: 'https://open.bigmodel.cn/api/paas/v4', model: 'glm-4-flash' },
}

function setPreset(name) {
  const p = PRESETS[name]
  config.value.api_base = p.api_base
  config.value.model = p.model
}

function addTag(name) {
  const cur = genTagInput.value.split(',').map(s => s.trim()).filter(Boolean)
  if (!cur.includes(name)) cur.push(name)
  genTagInput.value = cur.join(', ')
}

async function loadConfig() {
  const res = await api.get('/ai/config')
  config.value = res.data
}

async function saveConfig() {
  await api.put('/ai/config', config.value)
  toast('配置保存成功')
}

async function analyze() {
  errMsg.value = ''
  result.value = ''
  analyzing.value = true
  const token = localStorage.getItem('token')
  const res = await fetch('/api/ai/analyze', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
  })
  if (!res.ok) {
    const d = await res.json()
    errMsg.value = d.msg || '请求失败'
    analyzing.value = false
    return
  }
  const reader = res.body.getReader()
  const decoder = new TextDecoder()
  let buf = ''
  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    buf += decoder.decode(value, { stream: true })
    const lines = buf.split('\n')
    buf = lines.pop()
    for (const line of lines) {
      if (!line.startsWith('data: ')) continue
      const d = line.slice(6)
      if (d === '[DONE]') { analyzing.value = false; return }
      try {
        const obj = JSON.parse(d)
        if (obj.error) { errMsg.value = obj.error; analyzing.value = false; return }
        if (obj.text) result.value += obj.text
      } catch {}
    }
  }
  analyzing.value = false
}

async function saveToAbout() {
  saving.value = true
  await api.post('/ai/save-analysis', { content: result.value })
  toast('已保存到关于页')
  saving.value = false
}

function copyResult() { navigator.clipboard.writeText(result.value) }

async function generateArticle() {
  genErr.value = ''
  genResult.value = null
  if (!genForm.value.description.trim()) { genErr.value = '请输入文章描述'; return }
  generating.value = true
  try {
    const tag_names = genTagInput.value.split(',').map(s => s.trim()).filter(Boolean)
    const res = await api.post('/ai/generate-article', { ...genForm.value, tag_names })
    genResult.value = res.data
    toast('文章生成成功 🎉')
  } catch (e) {
    genErr.value = e.response?.data?.msg || '生成失败，请检查 API 配置'
    toast(genErr.value, 'error')
  } finally {
    generating.value = false
  }
}

onMounted(async () => {
  loadConfig()
  const [cats, tgs, media] = await Promise.all([
    api.get('/categories'),
    api.get('/tags'),
    api.get('/media?per_page=50&type=image'),
  ])
  categories.value = cats.data
  tags.value = tgs.data
  mediaList.value = media.data.items
})
</script>

<style scoped>
.ai-page { display: flex; flex-direction: column; gap: 20px; }
.section-card { padding: 24px; }
.section-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; }
.section-title { font-size: 16px; font-weight: 600; color: var(--text-primary); }
.header-actions { display: flex; gap: 10px; align-items: center; }
.config-saved-tip { font-size: 13px; color: var(--accent); animation: fadeIn 0.3s ease; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(-4px); } to { opacity: 1; transform: translateY(0); } }

.config-body { display: flex; flex-direction: column; gap: 0; }
.config-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; }
.field-group { display: flex; flex-direction: column; gap: 6px; }
.field-group label { font-size: 13px; color: var(--text-secondary); }
.field-hint { font-size: 11px; color: var(--text-muted); margin-top: 2px; }
.hint-tag { font-size: 11px; color: var(--accent); background: rgba(79,195,247,0.1); padding: 1px 6px; border-radius: 4px; margin-left: 6px; }
[data-theme="light"] .hint-tag { background: rgba(37,99,235,0.1); }
.field-input { width: 100%; padding: 9px 14px; background: var(--bg-primary); border: 1px solid var(--border); border-radius: var(--radius); color: var(--text-primary); font-size: 14px; outline: none; transition: border-color 0.2s; resize: vertical; }
.field-input:focus { border-color: var(--accent); }
.pwd-wrap { position: relative; }
.pwd-wrap .field-input { padding-right: 38px; }
.eye-btn { position: absolute; right: 10px; top: 50%; transform: translateY(-50%); background: none; border: none; color: var(--text-muted); cursor: pointer; display: flex; align-items: center; transition: color 0.2s; }
.eye-btn:hover { color: var(--accent); }

.presets { margin-top: 16px; padding-top: 16px; border-top: 1px solid var(--border); }
.preset-label { font-size: 12px; color: var(--text-muted); margin-bottom: 10px; }
.preset-btns { display: flex; flex-wrap: wrap; gap: 8px; }
.preset-btn { padding: 5px 14px; border-radius: 20px; border: 1px solid var(--border); background: none; color: var(--text-secondary); font-size: 12px; cursor: pointer; transition: all 0.2s; }
.preset-btn:hover { border-color: var(--accent); color: var(--accent); }

.analyze-placeholder { padding: 40px 0; text-align: center; color: var(--text-muted); font-size: 14px; }
.result-wrap { background: var(--bg-secondary); border-radius: var(--radius); padding: 20px; min-height: 80px; line-height: 1.9; font-size: 15px; color: var(--text-primary); }
.result-editor { width: 100%; background: var(--bg-secondary); border: 1px solid var(--accent); border-radius: var(--radius); padding: 16px; color: var(--text-primary); font-size: 15px; line-height: 1.9; outline: none; resize: vertical; min-height: 120px; }

@media (max-width: 768px) {
  .config-grid { grid-template-columns: 1fr; }
  .section-header { flex-wrap: wrap; gap: 10px; }
  .result-actions { flex-wrap: wrap; }
}
.cursor-blink { display: inline-block; animation: blink 0.8s infinite; color: var(--accent); }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }
.result-actions { display: flex; gap: 10px; margin-top: 16px; }
.tip { font-size: 13px; margin-top: 12px; }
.tip.success { color: var(--accent); }
.tip.error { color: #ef4444; }

/* Tab 切换 */
.tab-bar { display: flex; gap: 4px; background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius); padding: 4px; }
.tab { flex: 1; padding: 8px 16px; border-radius: calc(var(--radius) - 2px); border: none; background: none; color: var(--text-secondary); font-size: 14px; cursor: pointer; transition: all 0.2s; }
.tab:hover { color: var(--text-primary); }
.tab.active { background: var(--accent); color: #fff; font-weight: 500; }

/* 文章生成表单 */
.gen-form { display: flex; flex-direction: column; gap: 16px; }
.gen-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; }
.input-with-hint { display: flex; flex-direction: column; gap: 6px; }
.existing-list { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 4px; }
.quick-tag { padding: 2px 10px; border-radius: 20px; font-size: 12px; border: 1px solid var(--border); color: var(--text-muted); cursor: pointer; transition: all 0.2s; }
.quick-tag:hover { border-color: var(--accent); color: var(--accent); }
.required { color: #ef4444; }

/* 生成结果 */
.gen-result { padding: 20px; margin-top: 16px; border-left: 3px solid var(--accent); }
.gen-result-title { font-size: 15px; font-weight: 600; color: var(--accent); margin-bottom: 12px; }
.gen-result-info { font-size: 14px; color: var(--text-secondary); margin-bottom: 6px; }
.gen-result-info strong { color: var(--text-primary); }
.gen-result-actions { display: flex; gap: 10px; margin-top: 16px; }

@media (max-width: 768px) {
  .gen-grid { grid-template-columns: 1fr; }
  .tab-bar { flex-direction: column; }
}
</style>
