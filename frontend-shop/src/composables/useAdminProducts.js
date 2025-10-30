// Управление товарами в админке
import { ref } from 'vue'
import { apiFetch } from '@/utils/api'

export function useAdminProducts() {
    const products = ref([])
    const loading = ref(false)
    const error = ref(null)
    const saving = ref(false)

    // Загрузить все товары
    const fetchProducts = async () => {
        loading.value = true
        error.value = null
        try {
            const response = await apiFetch('/api/products/')
            if (!response.ok) throw new Error('Не удалось загрузить товары')
            products.value = await response.json()
        } catch (err) {
            error.value = err.message
        } finally {
            loading.value = false
        }
    }

    // Обновить товар
    const updateProduct = async (productId, productData) => {
        saving.value = true
        error.value = null
        try {
            const response = await apiFetch(`/api/products/${productId}`, {
                method: 'PUT',
                body: JSON.stringify(productData)
            })
            if (!response.ok) {
                const errData = await response.json().catch(() => ({}))
                throw new Error(errData.detail || 'Ошибка обновления товара')
            }
            const updatedProduct = await response.json()
            const index = products.value.findIndex(p => p.id === productId)
            if (index !== -1) {
                products.value[index] = updatedProduct
            }
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            saving.value = false
        }
    }

    // Удалить товар
    const deleteProduct = async (productId) => {
        if (!confirm('Удалить товар? Это действие нельзя отменить.')) return

        saving.value = true
        error.value = null
        try {
            const response = await apiFetch(`/api/products/${productId}`, {
                method: 'DELETE'
            })
            if (!response.ok) {
                const errData = await response.json().catch(() => ({}))
                throw new Error(errData.detail || 'Ошибка удаления товара')
            }
            products.value = products.value.filter(p => p.id !== productId)
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            saving.value = false
        }
    }

    // Создать новый товар
    const createProduct = async (productData) => {
        saving.value = true
        error.value = null
        try {
            const response = await apiFetch('/api/products/', {
                method: 'POST',
                body: JSON.stringify(productData)
            })
            if (!response.ok) {
                const errData = await response.json().catch(() => ({}))
                throw new Error(errData.detail || 'Ошибка создания товара')
            }
            const newProduct = await response.json()
            products.value.unshift(newProduct) // добавляем в начало списка
            return newProduct // ✅ Возвращаем новый товар
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            saving.value = false
        }
    }

    // Загрузить изображение для товара
    const uploadImage = async (productId, file) => {
        saving.value = true
        error.value = null
        try {
            const formData = new FormData()
            formData.append('file', file)

            const token = localStorage.getItem('access_token')
            const response = await fetch(`/api/products/${productId}/upload_image`, {
                method: 'POST',
                headers: {
                    ...(token ? { 'access_token': token } : {})
                },
                body: formData
            })

            if (!response.ok) {
                const errData = await response.json().catch(() => ({}))
                throw new Error(errData.detail || 'Ошибка загрузки изображения')
            }

            const result = await response.json()
            // Обновляем глобальный список
            const product = products.value.find(p => p.id === productId)
            if (product) {
                product.image_url = result.image_url
            }
            return result.image_url
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            saving.value = false
        }
    }

    return {
        products,
        loading,
        saving,
        error,
        fetchProducts,
        updateProduct,
        deleteProduct,
        createProduct,
        uploadImage
    }
}
