<template>
    <div class="admin-page">
        <div class="container">
            <h1>Админ-панель</h1>

            <div v-if="loading" class="status-message">Загрузка...</div>
            <div v-else-if="!isAdmin" class="status-message error">
                У вас нет доступа к админ-панели
            </div>
            <div v-else class="admin-dashboard">
                <p>Добро пожаловать, администратор!</p>

                <div class="admin-links">
                <router-link to="/admin/users" class="admin-card">
                    <h3>👥 Пользователи</h3>
                    <p>Управление аккаунтами</p>
                </router-link>
                <router-link to="/admin/products" class="admin-card">
                    <h3>📦 Товары</h3>
                    <p>Редактирование каталога</p>
                </router-link>
                <router-link to="/admin/orders" class="admin-card">
                    <h3>📋 Заказы</h3>
                    <p>Обработка и просмотр</p>
                </router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useProfile } from '@/composables/useProfile'

const { isAdmin, loading } = useProfile()
</script>

<style scoped>
.admin-page {
  padding: 3rem 0;
}

.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

h1 {
  text-align: center;
  margin-bottom: 2.5rem;
  color: #2c3e50;
}

.status-message {
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
}

.status-message.error {
  color: #e74c3c;
}

.admin-dashboard {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  padding: 2.5rem;
}

.admin-dashboard p {
  text-align: center;
  font-size: 1.2rem;
  margin-bottom: 2.5rem;
  color: #7f8c8d;
}

.admin-links {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
}

.admin-card {
  display: block;
  padding: 1.75rem;
  background: #f8f9fa;
  border-radius: 12px;
  text-decoration: none;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.admin-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
  border-color: #3498db;
}

.admin-card h3 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
  font-size: 1.3rem;
}

.admin-card p {
  color: #7f8c8d;
  margin: 0;
  font-size: 1rem;
}
</style>
