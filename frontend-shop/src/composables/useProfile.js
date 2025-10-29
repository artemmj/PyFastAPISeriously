// Загрузка данных профиля с использованием токена
import { ref } from 'vue'
import { apiFetch } from '@/utils/api' // наша утилита с токеном

export function useProfile() {
    const profile = ref(null)
    const loading = ref(false)
    const error = ref(null)

    const fetchProfile = async () => {
        loading.value = true
        error.value = null

        try {
            const response = await apiFetch('/api/users/about_me') // твой эндпоинт

            if (!response.ok) {
                // Если 401 — токен недействителен
                if (response.status === 401) {
                    localStorage.removeItem('access_token')
                    localStorage.removeItem('refresh_token')
                    error.value = 'Сессия истекла. Пожалуйста, войдите снова.'
                    profile.value = null
                    return
                }
                throw new Error(`Ошибка: ${response.status}`)
            }

            profile.value = await response.json()
        } catch (err) {
            console.error('Ошибка загрузки профиля:', err)
            error.value = err.message || 'Не удалось загрузить данные профиля'
        } finally {
            loading.value = false
        }
    }

    return {
        profile,
        loading,
        error,
        fetchProfile
    }
}
