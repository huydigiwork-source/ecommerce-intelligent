<template>
  <div class="table-section">
    <h3>📦 Products</h3>
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Category</th>
            <th>Brand</th>
            <th>Price</th>
            <th>Rating</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in products" :key="product.product_name">
            <td>{{ product.product_name || '-' }}</td>
            <td>{{ product.category || '-' }}</td>
            <td>{{ product.brand || '-' }}</td>
            <td>${{ product.price || 0 }}</td>
            <td>{{ product.rating || '-' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="pagination">
      <button @click="changePage(currentPage - 1)" :disabled="currentPage === 1">Previous</button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button @click="changePage(currentPage + 1)" :disabled="currentPage === totalPages">Next</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Table',
  props: {
    products: Array,
    currentPage: Number,
    totalPages: Number
  },
  methods: {
    changePage(page) {
      if (page < 1 || page > this.totalPages) return
      this.$emit('page-change', page)
    }
  }
}
</script>

<style scoped>
.table-section {
  background: white;
  padding: 25px;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.table-section h3 {
  color: #667eea;
  margin-bottom: 20px;
}

.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 15px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background: #667eea;
  color: white;
  font-weight: bold;
}

tr:hover {
  background: #f5f5f5;
}

.pagination {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 20px;
}

.pagination button {
  padding: 10px 20px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.pagination button:hover:not(:disabled) {
  background: #764ba2;
}

.pagination button:disabled {
  background: #ddd;
  cursor: not-allowed;
}
</style>