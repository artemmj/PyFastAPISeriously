import { ref, computed } from 'vue'
import { apiFetch } from '@/utils/api'

// === Глобальные реактивные переменные (синглтон) ===
const profile = ref(null)
const loading = ref(false)
const error = ref(null)

// Флаг, чтобы не грузить много раз
let isFetching = false

export function useProfile() {

    const fetchProfile = async () => {
        if (isFetching) return
        isFetching = true
        loading.value = true
        error.value = null
        try {
            const response = await apiFetch('/api/users/about_me')
            if (!response.ok) {
                if (response.status === 401) {
                localStorage.removeItem('access_token')
                localStorage.removeItem('refresh_token')
                profile.value = null
                error.value = 'Сессия истекла'
                return
                }
                throw new Error('Не удалось загрузить профиль')
            }
            profile.value = await response.json()
        } catch (err) {
            error.value = err.message
        } finally {
            loading.value = false
            isFetching = false
        }
    }

    const isAdmin = computed(() => {
        return profile.value?.role_id === 1
    })

    return {
        profile,
        isAdmin,
        loading,
        error,
        fetchProfile
    }
}