<!-- Компонент шапки сайта с динамическими кнопками аутентификации -->
<template>
    <header class="app-header">
        <div class="container">
            <nav class="nav">
                <!-- Логотип / Главная -->
                <router-link to="/" class="logo">ShopVue</router-link>

                <!-- Основное меню -->
                <ul class="nav-links">
                    <li><router-link to="/catalog">Каталог</router-link></li>
                    <li><router-link to="/cart">Корзина</router-link></li>
                </ul>

                <!-- Кнопки аутентификации -->
                <div class="auth-buttons">
                    <template v-if="isAuthenticated">
                        <router-link to="/profile" class="btn btn-text">ЛК</router-link>
                        <router-link to="/orders" class="btn btn-text">Заказы</router-link>
                        <button @click="handleLogout" class="btn btn-text">Выйти</button>
                    </template>
                    <template v-else>
                        <!-- Не авторизованный -->
                        <router-link to="/auth/login" class="btn btn-outline">Войти</router-link>
                        <router-link to="/auth/register" class="btn btn-primary">Регистрация</router-link>
                    </template>
                </div>
            </nav>
        </div>
    </header>
</template>

<script setup>
import { computed } from 'vue'
import { useAuth } from '@/composables/useAuth'
import { useRouter } from 'vue-router'

const { accessToken, logout } = useAuth()
const router = useRouter()

// Проверяем, авторизован ли пользователь
const isAuthenticated = computed(() => !!accessToken.value)

// Простой способ получить email из токена (если он там есть)
// ⚠️ В реальном проекте лучше хранить профиль отдельно, но пока — заглушка
const userEmail = computed(() => {
  if (!accessToken.value) return ''
  try {
    // Декодируем payload JWT (без проверки подписи — только для UI)
    const payload = JSON.parse(atob(accessToken.value.split('.')[1]))
    return payload.email || 'Пользователь'
  } catch (e) {
    return 'Пользователь'
  }
})

// Обработчик выхода
const handleLogout = () => {
  logout()
  // Перенаправляем на главную
  router.push('/')
}
</script>

<style scoped>
.app-header {
  background: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 0.5rem 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.5rem;
  font-weight: 800;
  color: #2c3e50;
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav-links a {
  text-decoration: none;
  color: #34495e;
  font-weight: 500;
  transition: color 0.2s;
}

.nav-links a:hover,
.nav-links a.router-link-exact-active {
  color: #3498db;
}

.auth-buttons {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-greeting {
  color: #2c3e50;
  font-weight: 500;
}

/* Кнопки */
.btn {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: 600;
  text-decoration: none;
  display: inline-block;
  text-align: center;
  cursor: pointer;
  border: none;
  font-size: 0.95rem;
}

.btn-outline {
  background: transparent;
  border: 1px solid #3498db;
  color: #3498db;
}

.btn-outline:hover {
  background: #f0f8ff;
}

.btn-primary {
  background: #3498db;
  color: white;
  border: 1px solid #3498db;
}

.btn-primary:hover {
  background: #2980b9;
}

.btn-text {
  background: transparent;
  color: #3498db;
  padding: 0.5rem;
  font-weight: 500;
  border: none;
  cursor: pointer;
  text-decoration: none;
}

.btn-text:hover {
  color: #2980b9;
  text-decoration: underline;
}
</style>
