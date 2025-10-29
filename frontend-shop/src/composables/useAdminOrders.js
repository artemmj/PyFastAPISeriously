// Управление заказами в админке (только чтение)
import { ref } from 'vue'
import { apiFetch } from '@/utils/api'

export function useAdminOrders() {
    const orders = ref([])
    const loading = ref(false)
    const error = ref(null)

    const fetchOrders = async () => {
        loading.value = true
        error.value = null
        try {
            const response = await apiFetch('/api/orders')
            if (!response.ok) throw new Error('Не удалось загрузить заказы')
            orders.value = await response.json()
        } catch (err) {
            error.value = err.message
        } finally {
            loading.value = false
        }
    }

    // Если бэкенд поддерживает обновление статуса — раскомментируй
    // const updateOrderStatus = async (orderId, status) => { ... }

    return {
        orders,
        loading,
        error,
        fetchOrders
        // updateOrderStatus
    }
}