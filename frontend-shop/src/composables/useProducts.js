// composable для работы с API продуктов
// Можно использовать в любом компоненте: CatalogView, HomeView и т.д.

import { ref } from 'vue'
import { apiFetch } from '../utils/api.js'

export function useProducts() {
    // Состояния
    const products = ref([])
    const loading = ref(true)
    const error = ref(null)

    // Функция загрузки
    const fetchProducts = async () => {
        loading.value = true
        error.value = null

        try {
            // ⚠️ Замени URL на твой реальный FastAPI эндпоинт
            const response = await apiFetch('/api/products')

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`)
            }

            const data = await response.json()
            products.value = Array.isArray(data) ? data : []
        } catch (err) {
            console.error('Ошибка загрузки товаров:', err)
            error.value = err.message || 'Не удалось загрузить товары'
        } finally {
            loading.value = false
        }
    }

    // Автоматически загружаем при монтировании (опционально)
    // Но лучше вызывать явно в компоненте — гибче
    // onMounted(() => {
    //   fetchProducts()
    // })

    return {
        products,
        loading,
        error,
        fetchProducts
    }
}
