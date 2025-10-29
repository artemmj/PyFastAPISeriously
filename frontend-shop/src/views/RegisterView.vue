<template>
    <div class="auth-page">
        <h1>Регистрация</h1>
        <form @submit.prevent="handleSubmit" class="auth-form">
            <div class="form-group">
                <label>Email</label>
                <input v-model="form.email" type="email" required />
            </div>
            <div class="form-group">
                <label>Телефон</label>
                <input v-model="form.phone_number" type="text" required />
            </div>
            <div class="form-group">
                <label>Имя</label>
                <input v-model="form.first_name" type="text" required />
            </div>
            <div class="form-group">
                <label>Фамилия</label>
                <input v-model="form.last_name" type="text" required />
            </div>
            <div class="form-group">
                <label>Пароль</label>
                <input v-model="form.password" type="password" minlength="6" required />
            </div>
            <div class="form-group">
                <label>Подтверждение пароля</label>
                <input v-model="form.confirm_password" type="password" required />
            </div>

            <!-- Сообщение об ошибке -->
            <div v-if="error" class="error-message">{{ error }}</div>

            <!-- Сообщение об успехе -->
            <div v-if="success" class="success-message">
                Регистрация успешна! Теперь вы можете <router-link to="/auth/login">войти</router-link>.
            </div>

            <button type="submit" :disabled="loading" class="btn btn-primary">
                {{ loading ? 'Отправка...' : 'Зарегистрироваться' }}
            </button>

            <p class="auth-link">
                Уже есть аккаунт? <router-link to="/auth/login">Войти</router-link>
            </p>
        </form>
    </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useAuth } from '@/composables/useAuth'

const { register } = useAuth()

const form = reactive({
    email: '',
    phone_number: '',
    first_name: '',
    last_name: '',
    password: '',
    confirm_password: ''
})

const loading = ref(false)
const error = ref(null)
const success = ref(false)

const handleSubmit = async () => {
    // Валидация паролей на фронтенде
    if (form.password !== form.confirm_password) {
        error.value = 'Пароли не совпадают'
        return
    }

    loading.value = true
    error.value = null
    success.value = false

    try {
        await register(form)
        success.value = true
        // Очищаем форму
        Object.keys(form).forEach(key => form[key] = '')
    } catch (err) {
        error.value = err.message
    } finally {
        loading.value = false
    }
}
</script>

<style scoped>
.auth-page {
  max-width: 500px;
  margin: 3rem auto;
  padding: 0 1rem;
}

.auth-page h1 {
  text-align: center;
  margin-bottom: 2rem;
  color: #2c3e50;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #34495e;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
}

.error-message {
  color: #e74c3c;
  background: #fdf2f2;
  padding: 0.75rem;
  border-radius: 8px;
  text-align: center;
}

.success-message {
  color: #27ae60;
  background: #f2fdf5;
  padding: 0.75rem;
  border-radius: 8px;
  text-align: center;
}

.btn {
  padding: 0.75rem;
  font-size: 1rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  background: #3498db;
  color: white;
  font-weight: 600;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.auth-link {
  text-align: center;
  margin-top: 1rem;
}

.auth-link a {
  color: #3498db;
  text-decoration: none;
}
</style>
