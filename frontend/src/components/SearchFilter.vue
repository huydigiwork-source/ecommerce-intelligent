<template>
  <div class="search-section">
    <h3>🔍 Search & Filter Products</h3>
    <form class="search-form" @submit.prevent="submit">
      <input
        type="text"
        v-model="query"
        placeholder="Search products..."
        class="search-input"
      />
      <select v-model="category" class="filter-select">
        <option value="">All Categories</option>
        <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
      </select>
      <input
        type="number"
        v-model="minPrice"
        placeholder="Min Price"
        class="filter-select"
      />
      <input
        type="number"
        v-model="maxPrice"
        placeholder="Max Price"
        class="filter-select"
      />
      <input
        type="number"
        v-model="minRating"
        placeholder="Min Rating"
        step="0.1"
        min="0"
        max="5"
        class="filter-select"
      />
      <button type="submit" class="btn">Search</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'SearchFilter',
  data() {
    return {
      query: '',
      category: '',
      minPrice: '',
      maxPrice: '',
      minRating: '',
      categories: []
    }
  },
  methods: {
    submit() {
      this.$emit('search', {
        query: this.query,
        category: this.category,
        minPrice: this.minPrice,
        maxPrice: this.maxPrice,
        minRating: this.minRating
      })
    },
    async loadCategories() {
      try {
        const res = await fetch('/stats/categories')
        const data = await res.json()
        this.categories = Object.keys(data)
      } catch (error) {
        console.error('Failed to load categories:', error)
      }
    }
  },
  mounted() {
    this.loadCategories()
  }
}
</script>

<style scoped>
.search-section {
  background: white;
  padding: 25px;
  border-radius: 15px;
  margin-bottom: 30px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.search-section h3 {
  color: #667eea;
  margin-bottom: 20px;
}

.search-form {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.search-input {
  flex: 1;
  min-width: 300px;
  padding: 15px;
  border: 2px solid #ddd;
  border-radius: 10px;
  font-size: 1em;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
}

.filter-select {
  padding: 15px;
  border: 2px solid #ddd;
  border-radius: 10px;
  font-size: 1em;
  background: white;
}

.btn {
  padding: 15px 30px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1em;
  cursor: pointer;
}

.btn:hover {
  background: #764ba2;
}

@media (max-width: 768px) {
  .search-form {
    flex-direction: column;
  }
  .search-input {
    min-width: 100%;
  }
}
</style>