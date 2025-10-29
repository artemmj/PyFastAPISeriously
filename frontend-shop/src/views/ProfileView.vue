<template>
    <div class="profile-page">
        <h1>Личный кабинет</h1>
        <div v-if="loading" class="status-message">Загрузка...</div>
        <div v-else-if="error" class="status-message error">{{ error }}</div>
        <div v-else-if="profile" class="profile-card">
            <div class="profile-header">
                <h2>{{ profile.first_name }} {{ profile.last_name }}</h2>
                <p class="email">{{ profile.email }}</p>
                <p v-if="profile.phone_number" class="phone">Телефон: {{ profile.phone_number }}</p>
            </div>

            <div class="orders-section">
                <div class="section-header">
                    <h3>Мои заказы</h3>
                    <router-link to="/orders" class="btn btn-text">Все заказы</router-link>
                </div>

                <div v-if="!orders.length" class="orders-empty">
                    У вас пока не было заказов
                </div>

                <div v-else class="orders-list">
                    <div
                        v-for="order in orders"
                        :key="order.id"
                        class="order-item"
                    >
                        <div class="order-info">
                            <span class="order-id">Заказ #{{ order.id }} </span>
                            <span class="order-date">{{ formatDate(order.created_at) }}</span>
                            <span class="order-status" :class="order.status">{{ order.status }}</span>
                        </div>
                        <div class="order-total">
                            Итого: {{ order.total_amount }} ₽
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import { useProfile } from '@/composables/useProfile'
import { useOrders } from '@/composables/useOrders'

const { profile, loading, error, fetchProfile } = useProfile()
const { orders, loading: loadingOrders, error: ordersError, fetchOrders } = useOrders()

const formatDate = (isoString) => {
    const date = new Date(isoString)
    return date.toLocaleDateString('ru-RU', {
        day: 'numeric',
        month: 'short',
        hour: '2-digit',
        minute: '2-digit'
    })
}

onMounted(() => {
    fetchProfile()
    fetchOrders()
})
</script>

<style scoped>
.profile-page {
  padding: 2rem 1rem;
  max-width: 1200px;
  margin: 0 auto;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.section-header h3 {
  margin: 0;
  color: #2c3e50;
}

.orders-section {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #eee;
}

.orders-empty {
  text-align: center;
  color: #7f8c8d;
  padding: 1rem;
}

.orders-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.order-item {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem;
  background: #f8f9fa;
  border-radius: 8px;
  font-size: 0.95rem;
}

.order-info {
  display: flex;
  flex-direction: column;
}

.order-id {
  font-weight: 600;
  color: #2c3e50;
}

.order-date {
  color: #7f8c8d;
  font-size: 0.9rem;
}

.order-total {
  font-weight: bold;
  color: #27ae60;
}

/* Кнопки */
.btn-text {
  background: none;
  border: none;
  color: #3498db;
  cursor: pointer;
  font-weight: 500;
  padding: 0.25rem;
}

.btn-text:hover {
  color: #2980b9;
  text-decoration: underline;
}

.btn-outline {
  display: inline-block;
  text-align: center;
  margin-top: 1rem;
}
</style>