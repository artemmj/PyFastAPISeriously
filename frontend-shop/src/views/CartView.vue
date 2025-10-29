<template>
    <div class="cart-page">
        <h1>Корзина</h1>

        <div v-if="loading" class="status-message">Загрузка корзины...</div>
        <div v-else-if="error" class="status-message error">{{ error }}</div>
        <div v-else>
            <div v-if="!cart?.items?.length" class="cart-empty">
                <p>Моя корзина пуста</p>
                <router-link to="/catalog" class="btn btn-primary">Выбрать товары</router-link>
            </div>
            <div v-else>
                <div class="cart-items">
                <div v-for="item in cart.items" :key="item.id" class="cart-item">
                    <img
                        :src="getFullImageUrl(item.product.image_url)"
                        :alt="item.product.title"
                        class="cart-item-image"
                    />
                    <div class="cart-item-info">
                        <h3>{{ item.product.title }}</h3>
                        <p class="price">{{ item.product.price }} ₽ × {{ item.quantity }}</p>
                        <p class="total">Итого: {{ item.product.price * item.quantity }} ₽</p>
                    </div>
                    <div class="cart-item-actions">
                        <button @click="() => removeProduct(item.product.id)" class="btn btn-sm">–</button>
                        <button @click="() => addProduct(item.product.id)" class="btn btn-sm">+</button>
                    </div>
                </div>
                </div>

                <div class="cart-summary">
                    <p class="total-sum">Итого: {{ totalSum }} ₽</p>
                    <button @click="clearCart" class="btn btn-text">Очистить корзину</button>
                    <button 
                        @click="handleCheckout" 
                        :disabled="creating || !cart?.items?.length" 
                        class="btn btn-primary checkout-btn"
                    >
                        {{ creating ? 'Оформление...' : 'Оформить заказ' }}
                    </button>
                </div>
                
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useCart } from '@/composables/useCart'
import { useOrders } from '@/composables/useOrders'
import { useRouter } from 'vue-router'

const router = useRouter()
const { cart, fetchCart, loading, error, addProduct, removeProduct, clearCart } = useCart()
const { createOrder, creating, error: orderError } = useOrders()
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const getFullImageUrl = (url) => {
    if (!url) return ``
    return url.startsWith('http') ? url : API_BASE_URL + url
}

// Считаем общую сумму
const totalSum = computed(() => {
    if (!cart.value) return 0
    return cart.value.items.reduce((sum, item) => {
        return sum + item.product.price * item.quantity
    }, 0)
})

const handleCheckout = async () => {
    try {
        await createOrder()
        // Успешно — обновляем корзину и переходим к заказам
        await fetchCart()
        router.push('/orders')
    } catch (err) {
        // Ошибка уже в orderError, но можно показать alert
        console.error('Ошибка оформления:', err)
    }
}

// Загружаем корзину при входе
onMounted(() => {
    fetchCart()
})

</script>

<style scoped>
.cart-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 1rem;
}

.cart-page h1 {
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

.cart-empty {
  text-align: center;
  padding: 2rem;
}

.cart-empty .btn {
  margin-top: 1rem;
}

.cart-items {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.cart-item {
  display: flex;
  gap: 1.5rem;
  padding: 1.5rem;
  border: 1px solid #eee;
  border-radius: 12px;
  align-items: center;
}

.cart-item-image {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 8px;
}

.cart-item-info h3 {
  margin: 0 0 0.5rem;
}

.price {
  color: #3498db;
  font-weight: 600;
}

.total {
  color: #27ae60;
  font-weight: bold;
  margin-top: 0.25rem;
}

.cart-item-actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.btn-sm {
  width: 40px;
  height: 40px;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cart-summary {
  text-align: right;
  padding: 1.5rem;
  border-top: 2px solid #eee;
}

.total-sum {
  font-size: 1.5rem;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.checkout-btn {
  margin-left: 1rem;
}

.btn-text {
  color: #e74c3c;
  background: none;
  border: none;
  cursor: pointer;
}

.btn-text:hover {
  text-decoration: underline;
}
</style>