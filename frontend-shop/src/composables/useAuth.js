// composable для управления аутентификацией
import { ref } from 'vue'
import { useProfile } from '@/composables/useProfile'

// Храним токены реактивно (можно использовать в шаблонах)
const accessToken = ref(localStorage.getItem('access_token') || null)
const refreshToken = ref(localStorage.getItem('refresh_token') || null)

// Сохраняем токены в localStorage и реактивных переменных
const setTokens = (access, refresh) => {
    accessToken.value = access
    refreshToken.value = refresh
    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)
}

// Очищаем токены (выход из аккаунта)
const clearTokens = () => {
    accessToken.value = null
    refreshToken.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
}

// Регистрация нового пользователя
const register = async (userData) => {
    const response = await fetch('/api/auth/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
    })

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || 'Ошибка регистрации')
    }

    // После регистрации — автоматически не логинимся, только сообщаем об успехе
    return await response.json()
}

// Вход (получение JWT)
const login = async (credentials) => {
    const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(credentials)
    })

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || 'Неверный email или пароль')
    }

    const tokens = await response.json()
    setTokens(tokens.access_token, tokens.refresh_token)

    const { fetchProfile } = useProfile()
    fetchProfile()

    return tokens
}

// Выход из аккаунта
const logout = () => {
    clearTokens()
}

// Экспортируем всё, что нужно
export function useAuth() {
    return {
        accessToken,
        refreshToken,
        register,
        login,
        logout,
        isAuthenticated: () => !!accessToken.value
    }
}
