// Утилита для безопасных запросов с токеном
import { useAuth } from '@/composables/useAuth'

// Получаем текущий токен (через composable)
// Но composable нельзя вызывать вне setup(), поэтому делаем через функцию
export const apiFetch = async (url, options = {}) => {
    const token = localStorage.getItem('access_token')

    // Копируем заголовки, чтобы не мутировать оригинальный объект
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    }

    // Добавляем токен, если он есть
    if (token) {
        headers['access_token'] = token
    }

    const config = {
        ...options,
        headers
    }

    const response = await fetch(url, config)

    // Можно добавить обработку 401 (неавторизован) — например, очистить токены
    if (response.status === 401) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        // Перенаправить на логин требует доступа к router — лучше в компоненте
    }

    return response
}
