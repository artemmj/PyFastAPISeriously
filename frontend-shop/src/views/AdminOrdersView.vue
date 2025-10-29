<template>
  <div class="admin-orders">
    <div class="container">
      <h1>Управление заказами</h1>

      <div v-if="loading && orders.length === 0" class="status-message">Загрузка заказов...</div>
      <div v-else-if="error" class="status-message error">{{ error }}</div>
      <div v-else-if="orders.length === 0" class="status-message">Заказы не найдены</div>
      <div v-else class="orders-table-wrapper">
        <table class="orders-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Пользователь</th>
              <th>Статус</th>
              <th>Сумма (₽)</th>
              <th>Дата</th>
              <th>Товаров</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="order in orders" :key="order.id">
              <td>{{ order.id }}</td>
              <td>{{ order.user_id }}</td>
              <td>
                <span class="status-badge" :class="order.status">
                  {{ formatStatus(order.status) }}
                </span>
              </td>
              <td>{{ order.total_amount }} ₽</td>
              <td>{{ formatDate(order.created_at) }}</td>
              <td>{{ order.items?.length || 0 }}</td>
              <td class="actions">
                <button @click="openOrderDetails(order)" class="btn btn-primary btn-sm">
                  Детали
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Модалка деталей заказа -->
      <div v-if="selectedOrder" class="modal-overlay" @click="closeModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h2>Заказ #{{ selectedOrder.id }}</h2>
            <button @click="closeModal" class="modal-close">&times;</button>
          </div>
          <div class="modal-body">
            <div class="order-info">
              <p><strong>Статус:</strong> {{ formatStatus(selectedOrder.status) }}</p>
              <p><strong>Сумма:</strong> {{ selectedOrder.total_amount }} ₽</p>
              <p><strong>Дата:</strong> {{ formatDate(selectedOrder.created_at) }}</p>
              <p><strong>Пользователь ID:</strong> {{ selectedOrder.user_id }}</p>
            </div>
            <h3>Товары</h3>
            <div class="order-items">
              <div v-for="(item, idx) in selectedOrder.items" :key="idx" class="order-item">
                <span>{{ item.product.title }}</span>
                <span>{{ item.quantity }} шт × {{ item.product.price }} ₽</span>
                <span class="item-total">{{ item.quantity * item.product.price }} ₽</span>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button @click="closeModal" class="btn btn-primary">Закрыть</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAdminOrders } from '@/composables/useAdminOrders'

const {
  orders,
  loading,
  error,
  fetchOrders
} = useAdminOrders()

const selectedOrder = ref(null)

const openOrderDetails = (order) => {
  selectedOrder.value = order
}

const closeModal = () => {
  selectedOrder.value = null
}

const formatDate = (isoString) => {
  const date = new Date(isoString)
  return date.toLocaleDateString('ru-RU', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatStatus = (status) => {
  const map = {
    pending: 'В обработке',
    confirmed: 'Подтверждён',
    shipped: 'Отправлен',
    delivered: 'Доставлен',
    cancelled: 'Отменён'
  }
  return map[status] || status
}

onMounted(() => {
  fetchOrders()
})
</script>

<style scoped>
.admin-orders {
  padding: 2rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

h1 {
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

.orders-table-wrapper {
  overflow-x: auto;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  padding: 1rem;
}

.orders-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 900px;
}

.orders-table th,
.orders-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.orders-table th {
  background: #f8f9fa;
  font-weight: 600;
  color: #2c3e50;
}

.orders-table tbody tr:hover {
  background: #fafbff;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
}

.status-badge.pending { background: #fff3cd; color: #856404; }
.status-badge.confirmed { background: #d1ecf1; color: #0c5460; }
.status-badge.shipped { background: #cce5ff; color: #004085; }
.status-badge.delivered { background: #d4edda; color: #155724; }
.status-badge.cancelled { background: #f8d7da; color: #721c24; }

.actions {
  display: flex;
  gap: 0.5rem;
}

.btn-sm {
  padding: 0.4rem 0.8rem;
  font-size: 0.85rem;
  border-radius: 6px;
}

/* Модалка */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 16px;
  width: 90%;
  max-width: 700px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #eee;
}

.modal-header h2 {
  margin: 0;
  color: #2c3e50;
}

.modal-close {
  background: none;
  border: none;
  font-size: 2rem;
  cursor: pointer;
  color: #999;
}

.modal-close:hover {
  color: #333;
}

.modal-body {
  padding: 1.5rem;
}

.order-info p {
  margin: 0.5rem 0;
}

.order-items {
  margin-top: 1.5rem;
}

.order-item {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid #f0f0f0;
}

.item-total {
  font-weight: bold;
  color: #27ae60;
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #eee;
  text-align: right;
}

/* Адаптивность */
@media (max-width: 768px) {
  .modal-content {
    width: 95%;
    margin: 1rem;
  }

  .orders-table {
    min-width: 700px;
  }
}
</style>
