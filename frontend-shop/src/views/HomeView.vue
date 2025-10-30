<template>
    <div class="home">
        <!-- Hero Section -->
        <section class="hero">
            <div class="hero-content">
                <h1 class="hero-title">Ваш стиль — ваш выбор.</h1>
                <h1 class="hero-title">Стиль — это все.</h1>
                <p class="hero-subtitle">
                    Немного несуществующих товаров для несуществующих клиентов - все, чтобы вам было удобно.
                </p>
                <div class="hero-buttons">
                    <router-link to="/catalog" class="btn btn-primary">Смотреть каталог</router-link>
                    <router-link to="/about" class="btn btn-secondary">О нас</router-link>
                </div>
            </div>
        </section>

        <!-- Features Section -->
        <section class="features">
            <div class="container">
                <h2 class="section-title">Почему выбирают нас</h2>
                <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">🚚</div>
                    <h3>Быстрая доставка</h3>
                    <p>Доставим заказ в течение 24 часов по городу</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🔒</div>
                    <h3>Безопасно</h3>
                    <p>Защита данных и безопасная оплата</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🔄</div>
                    <h3>Возврат 30 дней</h3>
                    <p>Не подошёл товар? Вернём без вопросов</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">💬</div>
                    <h3>Поддержка 24/7</h3>
                    <p>Поможем с выбором и ответим на вопросы</p>
                </div>
                </div>
            </div>
        </section>

        <!-- Featured Products -->
        <section class="featured">
            <div class="container">
                <div class="section-header">
                    <h2 class="section-title">Популярные товары</h2>
                    <router-link to="/catalog" class="view-all">Смотреть все →</router-link>
                </div>
                <div class="products-grid">
                    <ProductCard
                        v-for="product in products.slice(0, 2)"
                        :key="product.id"
                        :product="product"
                    />
                </div>
            </div>
        </section>

        <!-- CTA Section -->
        <section class="cta">
            <template v-if="isAuthenticated">
                <div class="container">
                    <h2>Готовы сделать покупку?</h2>
                    <p>Ну и чего же вы ждете?</p>
                </div>
            </template>
            <template v-else>
                <div class="container">
                    <h2>Готовы сделать покупку?</h2>
                    <p>Присоединяйтесь к тысячам довольных клиентов уже сегодня.</p>
                    <router-link to="/auth/register" class="btn btn-secondary">Зарегистрироваться</router-link>
                </div>
            </template>
        </section>
    </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useAuth } from '@/composables/useAuth'
import { useProducts } from '@/composables/useProducts'
import ProductCard from '@/components/ProductCard.vue'
import { useCart } from '@/composables/useCart'

const { accessToken } = useAuth()
const isAuthenticated = computed(() => !!accessToken.value)
const { products, fetchProducts } = useProducts()
const { fetchCart } = useCart()

const loadProducts = () => {
    fetchProducts()
    fetchCart()
}

const loadCart = () => {
    fetchCart()
}

onMounted(() => {
    loadProducts()
    loadCart()
})
</script>

<style scoped>
.home {
  overflow: hidden;
}

.hero {
  background: linear-gradient(120deg, #f5f7fa 0%, #e4edf9 100%);
  padding: 5rem 1rem;
  text-align: center;
  position: relative;
}

.hero::before {
  content: '';
  position: absolute;
  top: -100px;
  left: -100px;
  width: 300px;
  height: 300px;
  border-radius: 50%;
  background: rgba(52, 152, 219, 0.08);
  z-index: 0;
}

.hero::after {
  content: '';
  position: absolute;
  bottom: -150px;
  right: -100px;
  width: 400px;
  height: 400px;
  border-radius: 50%;
  background: rgba(39, 174, 96, 0.06);
  z-index: 0;
}

.hero-content {
  position: relative;
  z-index: 1;
  max-width: 700px;
  margin: 0 auto;
}

.hero-title {
  font-size: 2.8rem;
  font-weight: 800;
  margin-bottom: 1rem;
  color: #2c3e50;
  line-height: 1.2;
}

.hero-subtitle {
  font-size: 1.25rem;
  color: #7f8c8d;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.hero-buttons {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
}

/* === Features === */
.features {
  padding: 4rem 0;
  background: white;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.section-title {
  text-align: center;
  font-size: 2.2rem;
  color: #2c3e50;
  margin-bottom: 3rem;
  position: relative;
}

.section-title::after {
  content: '';
  display: block;
  width: 60px;
  height: 4px;
  background: #3498db;
  margin: 0.5rem auto 0;
  border-radius: 2px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 2rem;
}

.feature-card {
  text-align: center;
  padding: 2rem 1.5rem;
  border-radius: 16px;
  background: #f8f9fa;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
}

.feature-icon {
  font-size: 2.5rem;
  margin-bottom: 1.25rem;
}

.feature-card h3 {
  font-size: 1.25rem;
  margin-bottom: 0.75rem;
  color: #2c3e50;
}

.feature-card p {
  color: #7f8c8d;
  line-height: 1.6;
}

/* === Featured Products === */
.featured {
  padding: 5rem 0;
  background: #f9fafb;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2.5rem;
}

.section-header .section-title {
  margin-bottom: 0;
  text-align: left;
}

.view-all {
  color: #3498db;
  text-decoration: none;
  font-weight: 600;
  font-size: 1.1rem;
  transition: color 0.2s;
}

.view-all:hover {
  color: #2980b9;
  text-decoration: underline;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 2.5rem;
}

/* === CTA === */
.cta {
  padding: 5rem 1rem;
  text-align: center;
  background: linear-gradient(135deg, #3498db 0%, #2c3e50 100%);
  color: white;
}

.cta h2 {
  font-size: 2.2rem;
  margin-bottom: 1rem;
}

.cta p {
  font-size: 1.1rem;
  opacity: 0.9;
  max-width: 600px;
  margin: 0 auto 2rem;
}

.btn-secondary {
  background: white;
  color: #3498db;
  border: 2px solid white;
}

.btn-secondary:hover {
  background: #f0f8ff;
  transform: translateY(-2px);
}

/* === Кнопки (общие) === */
.btn {
  padding: 0.85rem 1.75rem;
  border-radius: 50px;
  font-weight: 600;
  font-size: 1.05rem;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  text-align: center;
  transition: all 0.3s ease;
  border: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.btn-primary {
  background: #3498db;
  color: white;
}

.btn-primary:hover {
  background: #2980b9;
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(52, 152, 219, 0.4);
}

/* Адаптивность */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.2rem;
  }

  .hero-subtitle {
    font-size: 1.1rem;
  }

  .hero-buttons {
    flex-direction: column;
    align-items: center;
  }

  .section-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .view-all {
    align-self: center;
  }
}
</style>
