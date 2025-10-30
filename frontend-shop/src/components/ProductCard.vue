<!-- Компонент карточки товара — переиспользуемый элемент -->
<template>
    <div class="product-card">
        <!-- Изображение товара. Если нет image_url — используем заглушку -->
        <img
            :src="product.image_url"
            :alt="product.name"
            class="product-image"
        />
        <div class="product-info">
            <h3 class="product-name">{{ product.title }}</h3>
            <p>{{ product.description }}</p>
            <p class="product-price">{{ product.price }} ₽</p>
            <!-- Управление корзиной -->
            <div v-if="cartItem" class="cart-controls">
                <button @click="decrease" class="cart-btn" :disabled="loading">
                    –
                </button>
                <span class="cart-quantity">{{ cartItem.quantity }}</span>
                <button @click="increase" class="cart-btn" :disabled="loading">
                    +
                </button>
            </div>
            <button v-else @click="addToCart" class="btn btn-outline" :disabled="loading">
                В корзину
            </button>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue'
import { useCart } from '@/composables/useCart'
import { useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'

// Подключаем корзину
const { cart, addProduct, removeProduct, loading } = useCart()
const { accessToken } = useAuth()
const router = useRouter()

const props = defineProps({
    product: { type: Object, required: true }
})

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// Полный URL изображения
const fullImageUrl = computed(() => {
    const url = props.product.image_url
    if (!url) return ``
    return url.startsWith('http') ? url : API_BASE_URL + url
})

// Находим товар в корзине
const cartItem = computed(() => {
    return cart.value?.items?.find(item => item.product.id === props.product.id)
})

// Добавить в корзину
const addToCart = async () => {
    try {
        await addProduct(props.product.id)
    } catch (err) {
        router.push('/login')
        console.error('Ошибка добавления в корзину:', err)
    }
}

// Увеличить количество
const increase = async () => {
    try {
        await addProduct(props.product.id)
    } catch (err) {
        console.error('Ошибка увеличения количества:', err)
    }
}

// Уменьшить количество
const decrease = async () => {
    if (!cartItem.value || cartItem.value.quantity <= 1) {
        // Если 1 шт — удаляем товар из корзины
        try {
            await removeProduct(props.product.id)
        } catch (err) {
            console.error('Ошибка удаления из корзины:', err)
        }
        return
    }
    try {
        await removeProduct(props.product.id)
    } catch (err) {
        console.error('Ошибка уменьшения количества:', err)
    }
}
</script>

<style scoped>
.product-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.product-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
}

.product-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  display: block;
}

.product-info {
  padding: 1.25rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.product-name {
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
  color: #2c3e50;
  flex: 1;
}

.product-price {
  font-size: 1.25rem;
  font-weight: bold;
  color: #27ae60;
  margin: 0.5rem 0;
}

/* Кнопки корзины */
.cart-controls {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 0.75rem;
}

.cart-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f0f8ff;
  border: 1px solid #3498db;
  border-radius: 6px;
  font-weight: bold;
  color: #3498db;
  cursor: pointer;
  transition: all 0.2s;
}

.cart-btn:hover:not(:disabled) {
  background: #e1f0ff;
}

.cart-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.cart-quantity {
  min-width: 28px;
  text-align: center;
  font-weight: 600;
  color: #2c3e50;
}

.btn-outline {
  background: transparent;
  border: 2px solid #3498db;
  color: #3498db;
  padding: 0.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.2s;
  width: 100%;
  margin-top: 0.75rem;
}

.btn-outline:hover:not(:disabled) {
  background-color: #eaf4ff;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
