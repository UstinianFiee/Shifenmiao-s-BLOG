<template>
  <div class="container" style="padding: 120px 24px 80px">
    <h1 class="page-title fade-in-up">分类：{{ name }}</h1>
    <div class="glow-divider"></div>
    <div class="articles-grid">
      <ArticleCard v-for="a in articles" :key="a.id" :article="a" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../../api'
import ArticleCard from '../../components/front/ArticleCard.vue'

const route = useRoute()
const articles = ref([])
const name = ref('')

onMounted(async () => {
  const [arts, cats] = await Promise.all([
    api.get('/articles', { params: { category_id: route.params.id, per_page: 50 } }),
    api.get('/categories'),
  ])
  articles.value = arts.data.items
  const cat = cats.data.find(c => c.id == route.params.id)
  name.value = cat?.name || ''
})
</script>

<style scoped>
.page-title { font-size: 28px; font-weight: 700; margin-bottom: 24px; }
.articles-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 24px; }
</style>
