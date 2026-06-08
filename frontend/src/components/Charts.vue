<template>
  <div class="charts-grid">
    <div class="chart-card">
      <h3>📊 Top 10 Categories</h3>
      <VChart :option="categoriesOption" />
    </div>
    <div class="chart-card">
      <h3>🏆 Top 10 Brands</h3>
      <VChart :option="brandsOption" />
    </div>
    <div class="chart-card">
      <h3>💰 Price by Category</h3>
      <VChart :option="priceOption" />
    </div>
    <div class="chart-card">
      <h3>⭐ Rating by Category</h3>
      <VChart :option="ratingOption" />
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import VChart from 'vue-echarts'
import { BarChart, PieChart, LineChart } from 'echarts/charts'
import { GridComponent, LegendComponent, TitleComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'

VChart.use([
  BarChart,
  PieChart,
  LineChart,
  GridComponent,
  LegendComponent,
  TitleComponent,
  CanvasRenderer
])

export default defineComponent({
  name: 'Charts',
  components: { VChart },
  data() {
    return {
      categoriesOption: {
        xAxis: { type: 'category', data: [] },
        yAxis: { type: 'value' },
        series: [{ type: 'bar', data: [], itemStyle: { color: '#667eea' } }],
        toolbox: { show: false }
      },
      brandsOption: {
        series: [{
          type: 'pie',
          data: [],
          itemStyle: {
            color: ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b', '#fa709a', '#fee140']
          }
        }],
        toolbox: { show: false }
      },
      priceOption: {
        xAxis: { type: 'category', data: [] },
        yAxis: { type: 'value' },
        series: [{ type: 'bar', data: [], itemStyle: { color: '#667eea' } }],
        toolbox: { show: false }
      },
      ratingOption: {
        xAxis: { type: 'category', data: [] },
        yAxis: { type: 'value', min: 0, max: 5 },
        series: [{
          type: 'line',
          data: [],
          smooth: true,
          itemStyle: { color: '#764ba2' },
          areaStyle: { color: 'rgba(118, 75, 162, 0.2)' }
        }],
        toolbox: { show: false }
      }
    }
  },
  methods: {
    async loadCharts() {
      try {
        // Categories
        const catsRes = await fetch('/stats/categories')
        const catsData = await catsRes.json()
        this.categoriesOption.xAxis.data = Object.keys(catsData)
        this.categoriesOption.series[0].data = Object.values(catsData)

        // Brands
        const brandsRes = await fetch('/stats/brands')
        const brandsData = await brandsRes.json()
        this.brandsOption.series[0].data = Object.keys(brandsData).map((key, i) => ({
          name: key,
          value: brandsData[key]
        }))

        // Price
        const priceRes = await fetch('/stats/price')
        const priceData = await priceRes.json()
        this.priceOption.xAxis.data = priceData.map(d => d.category)
        this.priceOption.series[0].data = priceData.map(d => d.mean)

        // Rating
        const ratingRes = await fetch('/stats/rating')
        const ratingData = await ratingRes.json()
        this.ratingOption.xAxis.data = ratingData.map(d => d.category)
        this.ratingOption.series[0].data = ratingData.map(d => d.mean)
      } catch (error) {
        console.error('Failed to load charts:', error)
      }
    }
  },
  mounted() {
    this.loadCharts()
  }
})
</script>

<style scoped>
.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 30px;
  margin-bottom: 30px;
}

.chart-card {
  background: white;
  padding: 25px;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.chart-card h3 {
  color: #667eea;
  margin-bottom: 20px;
  text-align: center;
}

.chart-card div {
  height: 300px;
}
</style>