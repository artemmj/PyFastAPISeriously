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
            <h3 class="product-name">{{ product.description }}</h3>
            <p class="product-price">{{ product.price }} ₽</p>
            <button class="btn btn-outline" @click="handleAddToCart">В корзину</button>
        </div>
    </div>
</template>

<script setup>
import { useCart } from '@/composables/useCart'

const props = defineProps({
    product: { type: Object, required: true }
})

const { addProduct } = useCart()

const handleAddToCart = async () => {
    try {
        await addProduct(props.product.id)
        // Можно показать уведомление, но пока — просто консоль
        console.log('Товар добавлен в корзину')
    } catch (err) {
        alert('Ошибка: ' + err.message)
    }
}
</script>

<style scoped>
/* Стили карточки — такие же, как на главной, но вынесены в компонент */
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
}

.btn-outline:hover {
  background-color: #eaf4ff;
}
</style>
