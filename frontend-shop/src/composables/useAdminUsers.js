// Управление пользователями в админке
import { ref } from 'vue'
import { apiFetch } from '@/utils/api'

export function useAdminUsers() {
    const users = ref([])
    const loading = ref(false)
    const error = ref(null)
    const saving = ref(false)

    // Загрузить всех пользователей
    const fetchUsers = async () => {
        loading.value = true
        error.value = null
        try {
            const response = await apiFetch('/api/users/')
            if (!response.ok) throw new Error('Не удалось загрузить пользователей')
            users.value = await response.json()
        } catch (err) {
            error.value = err.message
        } finally {
            loading.value = false
        }
    }

    const createUser = async (userData) => {
        saving.value = true
        error.value = null
        try {
            const response = await apiFetch('/api/auth/register', {
                method: 'POST',
                body: JSON.stringify(userData)
            })
            if (!response.ok) {
                const errData = await response.json().catch(() => ({}))
                throw new Error(errData.detail || 'Ошибка создания пользователя')
            }
            const newUser = await response.json()
            users.value.unshift(newUser)
            return newUser
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            saving.value = false
        }
    }

    // Обновить пользователя
    const updateUser = async (userId, userData) => {
        saving.value = true
        error.value = null
        try {
            const response = await apiFetch(`/api/users/${userId}`, {
                method: 'PUT',
                body: JSON.stringify(userData)
            })
            if (!response.ok) {
                const errData = await response.json().catch(() => ({}))
                throw new Error(errData.detail || 'Ошибка обновления')
            }
            const updatedUser = await response.json()
            const index = users.value.findIndex(u => u.id === userId)
            if (index !== -1) {
                users.value[index] = updatedUser
            }
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            saving.value = false
        }
    }

    // Удалить пользователя
    const deleteUser = async (userId) => {
        if (!confirm('Вы уверены, что хотите удалить этого пользователя?')) return

        saving.value = true
        error.value = null
        try {
            const response = await apiFetch(`/api/users/${userId}`, {
                method: 'DELETE'
            })
            if (!response.ok) {
                const errData = await response.json().catch(() => ({}))
                throw new Error(errData.detail || 'Ошибка удаления')
            }
            // Удаляем из списка
            users.value = users.value.filter(u => u.id !== userId)
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            saving.value = false
        }
    }

    return {
        users,
        loading,
        saving,
        error,
        fetchUsers,
        createUser,
        updateUser,
        deleteUser
    }
}
