<template>
    <div class="orders-page">
        <h1>Мои заказы</h1>

        <div v-if="loading" class="status-message">Загрузка заказов...</div>
        <div v-else-if="error" class="status-message error">{{ error }}</div>
        <div v-else-if="!orders.length" class="status-message">
            У вас пока нет заказов
        </div>
        <div v-else class="orders-list">
            <div v-for="order in orders" :key="order.id" class="order-card">
                <div class="order-header">
                    <span class="order-id">Заказ #{{ order.id }}</span>
                    <span class="order-date">{{ formatDate(order.created_at) }}</span>
                </div>
                <div class="order-items">
                    <div v-for="item in order.items" :key="item.id" class="order-item">
                        <img
                            :src="getFullImageUrl(item.product.image_url)"
                            :alt="item.product.name"
                            class="order-item-image"
                        />
                        <div class="order-item-info">
                            <h4>{{ item.product.name }}</h4>
                            <p>{{ item.product.price }} ₽ × {{ item.quantity }} = {{ item.product.price *  item.quantity}}</p>
                        </div>
                    </div>
                </div>
                <div class="order-total">
                    Итого: {{ order.total_amount }} ₽
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import { useOrders } from '@/composables/useOrders'

const { orders, loading, error, fetchOrders } = useOrders()

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const getFullImageUrl = (url) => {
  if (!url) return ``
  return url.startsWith('http') ? url : API_BASE_URL + url
}

const formatDate = (isoString) => {
  const date = new Date(isoString)
  return date.toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  fetchOrders()
})
</script>

<style scoped>
.orders-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 1rem;
}

.orders-page h1 {
  text-align: center;
  margin-bottom: 2rem;
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

.orders-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.order-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  padding: 1.5rem;
}

.order-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
  color: #2c3e50;
  font-weight: 600;
}

.order-id {
  font-size: 1.1rem;
}

.order-date {
  color: #7f8c8d;
  font-size: 0.95rem;
}

.order-items {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1rem;
}

.order-item {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.order-item-image {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 4px;
}

.order-item-info h4 {
  margin: 0 0 0.25rem;
  font-size: 1rem;
}

.order-total {
  font-weight: bold;
  color: #27ae60;
  text-align: right;
  font-size: 1.1rem;
}
</style>