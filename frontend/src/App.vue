<template>
  <div class="container">
    <header>
      <h1>🛍️ E-Commerce Product Intelligence</h1>
      <p>Browse, search, and analyze thousands of products</p>
    </header>

    <Insights />
    <Charts />
    <SearchFilter @search="handleSearch" />
    <Table
      :products="products"
      :currentPage="currentPage"
      :totalPages="totalPages"
      @page-change="changePage"
    />
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import Insights from './components/Insights.vue'
import Charts from './components/Charts.vue'
import SearchFilter from './components/SearchFilter.vue'
import Table from './components/Table.vue'

export default defineComponent({
  name: 'App',
  components: { Insights, Charts, SearchFilter, Table },
  data() {
    return {
      products: [],
      currentPage: 1,
      totalPages: 1,
      filters: {}
    }
  },
  methods: {
    async loadProducts() {
      try {
        const params = new URLSearchParams({
          page: this.currentPage,
          limit: 50
        })
        if (this.filters.category) params.append('category', this.filters.category)
        if (this.filters.minPrice) params.append('min_price', this.filters.minPrice)
        if (this.filters.maxPrice) params.append('max_price', this.filters.maxPrice)
        if (this.filters.minRating) params.append('min_rating', this.filters.minRating)

        const res = await fetch(`/filter?${params}`)
        const data = await res.json()
        this.products = data.data
        this.totalPages = data.total_pages
      } catch (error) {
        console.error('Failed to load products:', error)
      }
    },
    changePage(page) {
      this.currentPage = page
      this.loadProducts()
    },
    handleSearch(filters) {
      this.filters = filters
      this.currentPage = 1
      this.loadProducts()
    }
  },
  mounted() {
    this.loadProducts()
  }
})
</script>

<style>
.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

header {
  background: white;
  padding: 30px;
  text-align: center;
  border-radius: 15px;
  margin-bottom: 30px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

header h1 {
  color: #667eea;
  font-size: 2.5em;
  margin-bottom: 10px;
}

header p {
  color: #666;
  font-size: 1.2em;
}
</style>