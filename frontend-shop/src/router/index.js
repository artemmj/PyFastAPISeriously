// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

// Импорт страниц
import HomeView from '../views/HomeView.vue'
import CatalogView from '../views/CatalogView.vue'
import CartView from '../views/CartView.vue'
import ProfileView from '../views/ProfileView.vue'
import RegisterView from '../views/RegisterView.vue'
import LoginView from '../views/LoginView.vue'
import OrdersView from '../views/OrdersView.vue'
import AboutView from '@/views/AboutView.vue'
// import NotFoundView from '../views/NotFoundView.vue'

// Определяем маршруты
const routes = [
    { path: '/', name: 'Home', component: HomeView },
    { path: '/catalog', name: 'Catalog', component: CatalogView },
    { path: '/cart', name: 'Cart', component: CartView },
    { path: '/profile', name: 'Profile', component: ProfileView },
    { path: '/auth/register', name: 'Register', component: RegisterView },
    { path: '/auth/login', name: 'Login', component: LoginView },
    { path: '/orders', name: 'Orders', component: OrdersView },
    { path: '/about', name: 'About', component: AboutView },
    // 404 — должен быть последним
    // { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFoundView }
]

// Создаём роутер
const router = createRouter({
    history: createWebHistory(),
    routes
})

// Навигационный гард: защищаем приватные маршруты
router.beforeEach((to, from, next) => {
    const publicRoutes = ['/', '/about', '/catalog', '/auth/login', '/auth/register']
    const isPublic = publicRoutes.includes(to.path)
    const isAuthenticated = !!localStorage.getItem('access_token')

    if (!isPublic && !isAuthenticated) {
        // Если маршрут приватный и пользователь не залогинен — редирект на логин
        next('/auth/login')
    } else {
        next()
    }
})

export default router
