<!-- Страница каталога товаров -->
<template>
    <div class="catalog-page">
        <h1 class="page-title">Каталог товаров</h1>
        <div v-if="loading" class="status-message">Загрузка товаров...</div>
        <div v-else-if="error" class="status-message error">
            Ошибка: {{ error }}
            <button @click="loadProducts" class="btn btn-primary retry-btn">Повторить</button>
        </div>
        <div v-else class="products-container">
            <div v-if="products.length === 0" class="status-message">
                Товары не найдены
            </div>
            <div v-else class="products-grid">
                <ProductCard
                    v-for="product in products"
                    :key="product.id"
                    :product="product"
                />
            </div>
        </div>
    </div>
</template>

<script setup>
// Импортируем компонент и composable
import { onMounted, computed } from 'vue'
import ProductCard from '@/components/ProductCard.vue'
import { useProducts } from '@/composables/useProducts'
import { useCart } from '@/composables/useCart'

// Инициализируем логику загрузки
const { products, loading, error, fetchProducts } = useProducts()
const { fetchCart } = useCart()

// Загружаем товары при входе на страницу
const loadProducts = () => {
    fetchProducts()
}

onMounted(() => {
    loadProducts()
    // Загружаем корзину ОДИН РАЗ при входе в каталог
    const token = localStorage.getItem('access_token')
    if (token) {
        fetchCart()
    }
})
</script>

<style scoped>
.catalog-page {
  padding: 2rem 1rem;
  max-width: 1200px;
  margin: 0 auto;
}

.page-title {
  text-align: center;
  margin-bottom: 2rem;
  font-size: 2rem;
  color: #2c3e50;
}

.status-message {
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
  color: #7f8c8d;
}

.status-message.error {
  color: #e74c3c;
}

.retry-btn {
  margin-top: 1rem;
}

.products-container {
  min-height: 400px;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 2rem;
}
</style>
