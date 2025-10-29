<template>
    <div class="auth-page">
        <h1>Вход</h1>
        <form @submit.prevent="handleSubmit" class="auth-form">
            <div class="form-group">
                <label>Email</label>
                <input v-model="form.email" type="email" required />
            </div>
            <div class="form-group">
                <label>Пароль</label>
                <input v-model="form.password" type="password" required />
            </div>

            <div v-if="error" class="error-message">{{ error }}</div>

            <button type="submit" :disabled="loading" class="btn btn-primary">
                {{ loading ? 'Вход...' : 'Войти' }}
            </button>

            <p class="auth-link">
                Нет аккаунта? <router-link to="/auth/register">Зарегистрироваться</router-link>
            </p>
        </form>
    </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useAuth } from '@/composables/useAuth'
import { useRouter } from 'vue-router'

const { login } = useAuth()
const router = useRouter()

const form = reactive({
    email: '',
    password: ''
})

const loading = ref(false)
const error = ref(null)

const handleSubmit = async () => {
    loading.value = true
    error.value = null

    try {
        await login(form)
        // После успешного входа — переходим на главную
        router.push('/')
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
