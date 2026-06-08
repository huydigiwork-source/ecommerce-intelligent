<template>
  <div class="insights-grid">
    <div class="insight-card" v-for="(value, key) in insights" :key="key">
      <h3>{{ labels[key] }}</h3>
      <div class="value">{{ formatValue(key, value) }}</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Insights',
  data() {
    return {
      insights: {},
      labels: {
        total_products: 'Total Products',
        categories: 'Categories',
        brands: 'Brands',
        avg_price: 'Avg Price',
        avg_rating: 'Avg Rating',
        min_price: 'Min Price',
        max_price: 'Max Price'
      }
    }
  },
  methods: {
    formatValue(key, value) {
      if (key.includes('price')) return `$${value}`
      if (key.includes('rating')) return value
      return value
    },
    async loadInsights() {
      try {
        const res = await fetch('/insights')
        this.insights = await res.json()
      } catch (error) {
        console.error('Failed to load insights:', error)
      }
    }
  },
  mounted() {
    this.loadInsights()
  }
}
</script>

<style scoped>
.insights-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.insight-card {
  background: white;
  padding: 25px;
  border-radius: 15px;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
  transition: transform 0.3s;
}

.insight-card:hover {
  transform: translateY(-5px);
}

.insight-card h3 {
  color: #666;
  font-size: 0.9em;
  margin-bottom: 10px;
}

.insight-card .value {
  color: #667eea;
  font-size: 2em;
  font-weight: bold;
}
</style>