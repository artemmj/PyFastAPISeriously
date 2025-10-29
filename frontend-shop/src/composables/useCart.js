// Управление корзиной: добавление, удаление, очистка
import { ref } from 'vue'
import { apiFetch } from '@/utils/api'

export function useCart() {
    // Храним текущую корзину (из /users/about_me)
    const cart = ref(null)
    const loading = ref(false)
    const error = ref(null)

    // Загрузка корзины (через профиль)
    const fetchCart = async () => {
        loading.value = true
        error.value = null
        try {
            const response = await apiFetch('/api/users/about_me')
            if (!response.ok) throw new Error('Не удалось загрузить корзину')
            const data = await response.json()
            cart.value = data.cart
        } catch (err) {
            error.value = err.message
        } finally {
            loading.value = false
        }
    }

    // Добавить товар в корзину
    const addProduct = async (productId) => {
        try {
            const response = await apiFetch(`/api/carts/add_product/${productId}`, {
                method: 'POST'
            })
            if (!response.ok) throw new Error('Не удалось добавить товар')
                await fetchCart() // обновляем корзину
        } catch (err) {
            error.value = err.message
            throw err
        }
    }

    // Удалить товар из корзины
    const removeProduct = async (productId) => {
        try {
            const response = await apiFetch(`/api/carts/remove_product/${productId}`, {
                method: 'POST'
            })
            if (!response.ok) throw new Error('Не удалось удалить товар')
            await fetchCart() // обновляем корзину
        } catch (err) {
            error.value = err.message
            throw err
        }
    }

    // Очистить корзину
    const clearCart = async () => {
        try {
            const response = await apiFetch('/api/carts/clear_cart', {
                method: 'POST'
            })
            if (!response.ok) throw new Error('Не удалось очистить корзину')
            await fetchCart()
        } catch (err) {
            error.value = err.message
            throw err
        }
    }

    return {
        cart,
        loading,
        error,
        fetchCart,
        addProduct,
        removeProduct,
        clearCart
    }
}