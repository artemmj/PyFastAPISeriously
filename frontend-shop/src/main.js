// src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Создаём и монтируем приложение
const app = createApp(App)

app.use(router)

app.mount('#app')
