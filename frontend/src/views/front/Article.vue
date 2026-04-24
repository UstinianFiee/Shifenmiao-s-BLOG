<template>
  <div class="article-page container" v-if="article">
    <div class="article-header fade-in-up">
      <div class="meta">
        <span v-if="article.category" class="category">{{ article.category.name }}</span>
        <span class="date">{{ formatDate(article.created_at) }}</span>
        <span class="views">👁 {{ article.views }}</span>
      </div>
      <h1 class="title">{{ article.title }}</h1>
      <div class="tags">
        <span v-for="t in article.tags" :key="t.id" class="tag">{{ t.name }}</span>
      </div>
    </div>

    <div class="glow-divider"></div>

    <div class="article-body">
      <!-- 目录 -->
      <aside class="toc" v-if="toc.length">
        <p class="toc-title">目录</p>
        <ul>
          <li v-for="h in toc" :key="h.id" :class="`toc-h${h.level}`">
            <a :href="`#${h.id}`">{{ h.text }}</a>
          </li>
        </ul>
      </aside>
      <!-- 正文 -->
      <article class="md-content" v-html="rendered"></article>
    </div>
  </div>
  <div v-else class="loading container">加载中...</div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../../api'
import { marked } from 'marked'
import hljs from 'highlight.js'
import 'highlight.js/styles/github-dark.css'

marked.setOptions({
  highlight: (code, lang) => {
    if (lang && hljs.getLanguage(lang)) return hljs.highlight(code, { language: lang }).value
    return hljs.highlightAuto(code).value
  },
  breaks: true,
})

const route = useRoute()
const article = ref(null)
const rendered = ref('')
const toc = ref([])

function buildToc(html) {
  const items = []
  const re = /<h([1-3])[^>]*id="([^"]*)"[^>]*>(.*?)<\/h[1-3]>/gi
  let m
  while ((m = re.exec(html)) !== null) {
    items.push({ level: m[1], id: m[2], text: m[3].replace(/<[^>]+>/g, '') })
  }
  return items
}

function formatDate(iso) {
  return new Date(iso).toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })
}

onMounted(async () => {
  const res = await api.get(`/articles/${route.params.id}`)
  article.value = res.data
  // add ids to headings
  const renderer = new marked.Renderer()
  renderer.heading = (text, level) => {
    const id = text.toLowerCase().replace(/\s+/g, '-').replace(/[^\w-]/g, '')
    return `<h${level} id="${id}">${text}</h${level}>`
  }
  rendered.value = marked(res.data.content, { renderer })
  toc.value = buildToc(rendered.value)
})
</script>

<style scoped>
.article-page { padding: 120px 24px 80px; max-width: 1100px; }
.article-header { margin-bottom: 32px; }
.meta { display: flex; gap: 12px; align-items: center; font-size: 13px; color: var(--text-muted); margin-bottom: 16px; }
.category { color: var(--accent); border: 1px solid var(--accent); padding: 1px 8px; border-radius: 4px; }
.title { font-size: clamp(24px, 4vw, 40px); font-weight: 700; line-height: 1.3; }
.tags { margin-top: 12px; display: flex; flex-wrap: wrap; gap: 6px; }

.article-body { display: flex; gap: 40px; align-items: flex-start; }

.toc {
  position: sticky; top: 80px;
  width: 220px; flex-shrink: 0;
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 16px;
  font-size: 13px;
}
.toc-title { color: var(--accent); font-weight: 600; margin-bottom: 12px; letter-spacing: 1px; }
.toc ul { list-style: none; }
.toc li { margin: 6px 0; }
.toc li a { color: var(--text-secondary); transition: color 0.2s; }
.toc li a:hover { color: var(--accent); }
.toc-h2 { padding-left: 12px; }
.toc-h3 { padding-left: 24px; }

.md-content { flex: 1; min-width: 0; }

@media (max-width: 768px) {
  .article-page { padding: 90px 16px 80px; }
  .article-body { flex-direction: column; gap: 20px; }
  .toc { position: static; width: 100%; }
}
</style>

<style>
/* markdown 渲染样式（全局） */
.md-content h1,.md-content h2,.md-content h3 { color: var(--text-primary); margin: 28px 0 12px; }
.md-content h2 { border-left: 3px solid var(--accent); padding-left: 12px; }
.md-content p { color: var(--text-secondary); margin-bottom: 16px; }
.md-content code { background: rgba(79,195,247,0.1); color: var(--accent); padding: 2px 6px; border-radius: 4px; font-size: 0.9em; }
.md-content pre { background: #0d1117; border: 1px solid var(--border); border-radius: var(--radius); padding: 16px; overflow-x: auto; margin-bottom: 20px; }
.md-content pre code { background: none; color: inherit; padding: 0; }
.md-content blockquote { border-left: 3px solid var(--accent-2); padding: 8px 16px; background: rgba(124,77,255,0.08); margin: 16px 0; color: var(--text-secondary); }
.md-content a { color: var(--accent); }
.md-content img { max-width: 100%; border-radius: var(--radius); }
.md-content table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
.md-content th,.md-content td { border: 1px solid var(--border); padding: 8px 12px; text-align: left; }
.md-content th { background: var(--bg-card); color: var(--accent); }
.md-content ul,.md-content ol { padding-left: 24px; color: var(--text-secondary); margin-bottom: 16px; }
</style>
