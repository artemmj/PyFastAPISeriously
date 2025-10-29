<template>
    <div class="profile-page">
        <h1>Личный кабинет</h1>

        <div v-if="loading" class="status-message">Загрузка...</div>
        <div v-else-if="error" class="status-message error">{{ error }}</div>
        <div v-else-if="profile" class="profile-card">
        <!-- Профиль -->
        <div class="profile-header">
            <h2>{{ profile.first_name }} {{ profile.last_name }}</h2>
            <p class="email">{{ profile.email }}</p>
            <p v-if="profile.phone_number" class="phone">Телефон: {{ profile.phone_number }}</p>
        </div>

        <!-- Корзина -->
        <div class="cart-section">
            <div class="cart-header">
                <h3>Ваша корзина</h3>
                <button v-if="cart?.items?.length" @click="clearCart" class="btn btn-text">
                    Очистить
                </button>
            </div>
            <div v-if="!cart?.items?.length" class="cart-empty">
                Корзина пуста
            </div>
            <div v-else class="cart-items">
                <div v-for="item in cart.items" :key="item.id" class="cart-item">
                    <img
                        :src="getFullImageUrl(item.product.image_url)"
                        :alt="item.product.title"
                        class="cart-item-image"
                    />
                    <div class="cart-item-info">
                        <h4>{{ item.product.title }}</h4>
                        <p class="price">{{ item.product.price }} ₽</p>
                        <p class="quantity">Кол-во: {{ item.quantity }}</p>
                    </div>
                    <div class="cart-item-actions">
                        <button @click="() => removeProduct(item.product.id)" class="btn btn-sm">
                            –
                        </button>
                        <button @click="() => addProduct(item.product.id)" class="btn btn-sm">
                            +
                        </button>
                    </div>
                </div>
            </div>
            <router-link to="/cart" class="btn btn-outline cart-link">Подробнее</router-link>
        </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import { useProfile } from '@/composables/useProfile'
import { useCart } from '@/composables/useCart'

const { profile, loading, error, fetchProfile } = useProfile()
const { cart, fetchCart, addProduct, removeProduct, clearCart } = useCart()

// Базовый URL для изображений
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const getFullImageUrl = (url) => {
  if (!url) return ``
  return url.startsWith('http') ? url : API_BASE_URL + url
}

onMounted(() => {
  fetchProfile()
  fetchCart()
})
</script>

<style scoped>
/* ... предыдущие стили ... */

.cart-section {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #eee;
}

.cart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.cart-header h3 {
  margin: 0;
}

.cart-empty {
  text-align: center;
  color: #7f8c8d;
  padding: 1rem;
}

.cart-items {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.cart-item {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid #eee;
  border-radius: 8px;
  align-items: center;
}

.cart-item-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 4px;
}

.cart-item-info {
  flex: 1;
}

.cart-item-info h4 {
  margin: 0 0 0.25rem;
  font-size: 1rem;
}

.price {
  color: #27ae60;
  font-weight: bold;
  margin: 0.25rem 0;
}

.quantity {
  color: #7f8c8d;
  font-size: 0.9rem;
  margin: 0;
}

.cart-item-actions {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.btn-sm {
  width: 30px;
  height: 30px;
  padding: 0;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cart-link {
  display: block;
  text-align: center;
  margin-top: 1.5rem;
}
</style>