// Управление заказами: создание, получение списка
import { ref } from 'vue'
import { apiFetch } from '@/utils/api'

export function useOrders() {
    const orders = ref([])
    const loading = ref(false)
    const error = ref(null)
    const creating = ref(false)

    const fetchOrders = async () => {
        loading.value = true
        error.value = null

        try {
            const response = await apiFetch('/api/orders/my')
            if (!response.ok) throw new Error('Не удалось загрузить заказы')
            orders.value = await response.json()
        } catch (err) {
            error.value = err.message
        } finally {
            loading.value = false
        }
    }

    const createOrder = async () => {
        creating.value = true
        error.value = null

        try {
            const response = await apiFetch('/api/orders', {
                method: 'POST'
            })
            if (!response.ok) {
                const errData = await response.json().catch(() => ({}))
                throw new Error(errData.detail || 'Не удалось создать заказ')
            }
            // После создания — обновляем список заказов и корзину
            await fetchOrders()
            return await response.json()
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            creating.value = false
        }
    }

    return {
        orders,
        loading,
        creating,
        error,
        fetchOrders,
        createOrder
    }
}