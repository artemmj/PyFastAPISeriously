import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
    plugins: [
        vue(),
        vueDevTools(),
    ],
    resolve: {
        alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
        },
    },
    server: {
        port: 5173, // необязательно, но явно указываем
        proxy: {
            // Все запросы, начинающиеся с /api, перенаправляются на бэкенд
            '/api': {
                target: 'http://localhost:8000', // адрес твоего FastAPI
                changeOrigin: true,              // нужно для корректных заголовков Host
                secure: false,                   // отключает проверку SSL (для localhost)
                rewrite: (path) => path          // оставляем путь как есть: /api/... → /api/...
            },
            // Добавляем прокси для статики
            '/static': {
                target: 'http://localhost:8000',
                changeOrigin: true,
                secure: false
            }
        }
    },
})
