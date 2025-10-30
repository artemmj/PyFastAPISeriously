<template>
    <div class="admin-users">
        <div class="container">
            <div class="page-header">
                <h1>Управление пользователями</h1>
                <button @click="openCreateModal" class="btn btn-primary">+ Добавить пользователя</button>
            </div>

            <div v-if="loading && users.length === 0" class="status-message">Загрузка пользователей...</div>
            <div v-else-if="error" class="status-message error">{{ error }}</div>
            <div v-else-if="users.length === 0" class="status-message">Пользователи не найдены</div>
            <div v-else class="users-table-wrapper">
                <table class="users-table">
                <thead>
                    <tr>
                    <th>ID</th>
                    <th>Имя</th>
                    <th>Email</th>
                    <th>Телефон</th>
                    <th>Роль</th>
                    <th>Действия</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="user in users" :key="user.id">
                    <td>{{ user.id }}</td>
                    <td>{{ user.first_name }} {{ user.last_name }}</td>
                    <td>{{ user.email }}</td>
                    <td>{{ user.phone_number || '—' }}</td>
                    <td>
                        <span :class="`role-badge role-${user.role_id}`">
                        {{ user.role_id === 1 ? 'Админ' : (user.role_id === 2 ? 'Модератор' : 'Пользователь') }}
                        </span>
                    </td>
                    <td class="actions">
                        <button @click="openEditModal(user)" class="btn btn-outline btn-sm">Редактировать</button>
                        <button @click="() => deleteUser(user.id)" :disabled="saving" class="btn btn-danger btn-sm">
                        Удалить
                        </button>
                    </td>
                    </tr>
                </tbody>
                </table>
            </div>

            <!-- Модальное окно -->
            <div v-if="isModalOpen" class="modal-overlay" @click="closeModal">
                <div class="modal" @click.stop>
                <div class="modal-header">
                    <h3>{{ editingUser ? 'Редактировать пользователя' : 'Добавить пользователя' }}</h3>
                    <button @click="closeModal" class="modal-close">&times;</button>
                </div>
                <form @submit.prevent="handleSubmit" class="modal-form">
                    <div class="form-row">
                        <div class="form-group">
                            <label>Имя</label>
                            <input v-model="modalForm.first_name" type="text" required />
                        </div>
                        <div class="form-group">
                            <label>Фамилия</label>
                            <input v-model="modalForm.last_name" type="text" required />
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Email</label>
                            <input v-model="modalForm.email" type="email" required />
                        </div>
                        <div class="form-group">
                            <label>Телефон</label>
                            <input v-model="modalForm.phone_number" type="text" />
                        </div>
                    </div>
                    <div v-if="!editingUser" class="form-row">
                        <div class="form-group">
                            <label>Пароль</label>
                            <input v-model="modalForm.password" type="password" minlength="6" required />
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Роль</label>
                            <select v-model.number="modalForm.role_id" class="form-select">
                                <option :value="1">Админ</option>
                                <option :value="2">Модератор</option>
                                <option :value="3">Пользователь</option>
                            </select>
                        </div>
                    </div>
                    <div class="modal-actions">
                        <button type="submit" :disabled="saving" class="btn btn-primary">
                            {{ saving ? 'Сохранение...' : (editingUser ? 'Сохранить' : 'Создать') }}
                        </button>
                        <button @click="closeModal" type="button" class="btn btn-outline">Отмена</button>
                    </div>
                </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAdminUsers } from '@/composables/useAdminUsers'

const {
    users,
    loading,
    saving,
    error,
    fetchUsers,
    createUser,
    updateUser,
    deleteUser
} = useAdminUsers()

// Модалка
const isModalOpen = ref(false)
const editingUser = ref(null) // null = создание, объект = редактирование
const modalForm = ref({
    first_name: '',
    last_name: '',
    email: '',
    phone_number: '',
    password: '',
    confirm_password: '',
    role_id: 2
})

// Открыть модалку создания
const openCreateModal = () => {
    editingUser.value = null
    modalForm.value = {
        first_name: '',
        last_name: '',
        email: '',
        phone_number: '',
        password: '',
        confirm_password: '',
        role_id: 2
    }
    isModalOpen.value = true
}

// Открыть модалку редактирования
const openEditModal = (user) => {
    editingUser.value = user
    modalForm.value = {
        first_name: user.first_name,
        last_name: user.last_name,
        email: user.email,
        phone_number: user.phone_number || '',
        password: '', // не меняем пароль при редактировании
        confirm_password: '',
        role_id: user.role_id
    }
    isModalOpen.value = true
}

// Закрыть модалку
const closeModal = () => {
    isModalOpen.value = false
    editingUser.value = null
}

// Отправка формы
const handleSubmit = async () => {
    try {
        if (editingUser.value) {
            // Редактирование
            await updateUser(
                editingUser.value.id,
                {
                    first_name: modalForm.value.first_name,
                    last_name: modalForm.value.last_name,
                    email: modalForm.value.email,
                    phone_number: modalForm.value.phone_number,
                    role_id: modalForm.value.role_id
                    // пароль не отправляем
                }
        )
        } else {
            // Создание
            modalForm.value.confirm_password = modalForm.value.password
            await createUser(modalForm.value)
        }
        closeModal()
        fetchUsers()
    } catch (err) {
        console.error('Ошибка:', err)
    }
}

// Загрузка при монтировании
onMounted(() => {
    fetchUsers()
})
</script>

<style scoped>
.admin-users {
  padding: 2rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

/* Форма создания */
.create-section {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  margin-bottom: 2rem;
}

.create-section h2 {
  margin-bottom: 1.5rem;
  color: #2c3e50;
  font-size: 1.5rem;
}

.create-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #2c3e50;
}

.form-input,
.form-select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
}

/* Заголовок таблицы */
h1 {
  text-align: center;
  margin-bottom: 2rem;
  color: #2c3e50;
}

/* Сообщения */
.status-message {
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
  color: #7f8c8d;
}

.status-message.error {
  color: #e74c3c;
}

/* Таблица */
.users-table-wrapper {
  overflow-x: auto;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  padding: 1rem;
}

.users-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 800px;
}

.users-table th,
.users-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.users-table th {
  background: #f8f9fa;
  font-weight: 600;
  color: #2c3e50;
}

.users-table tbody tr:hover {
  background: #fafbff;
}

.role-select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.95rem;
  cursor: pointer;
}

/* Кнопки */
.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.btn {
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.85rem;
  cursor: pointer;
  border: none;
}

.btn-primary {
  background: #3498db;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #2980b9;
}

.btn-outline {
  background: transparent;
  border: 1px solid #3498db;
  color: #3498db;
}

.btn-outline:hover:not(:disabled) {
  background: #f0f8ff;
}

.btn-danger {
  background: #e74c3c;
  color: white;
}

.btn-danger:hover:not(:disabled) {
  background: #c0392b;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.page-header h1 {
  color: #2c3e50;
}

/* Таблица */
.users-table-wrapper {
  overflow-x: auto;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  padding: 1rem;
}

.users-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 800px;
}

.users-table th,
.users-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.users-table th {
  background: #f8f9fa;
  font-weight: 600;
  color: #2c3e50;
}

.role-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.role-1 {
  background: #e3f2fd;
  color: #d40f0f;
}

.role-2 {
  background: #f1f8e9;
  color: #1b38ac;
}

.role-3 {
  background: #f1f8e9;
  color: #388e3c;
}

.actions {
  display: flex;
  gap: 0.5rem;
}

/* Модальное окно */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 16px;
  width: 90%;
  max-width: 600px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #eee;
}

.modal-header h3 {
  margin: 0;
  color: #2c3e50;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.8rem;
  cursor: pointer;
  color: #999;
}

.modal-close:hover {
  color: #333;
}

.modal-form {
  padding: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #2c3e50;
}

.form-input,
.form-select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}

/* Кнопки */
.btn {
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  font-size: 0.95rem;
}

.btn-primary {
  background: #3498db;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #2980b9;
}

.btn-outline {
  background: transparent;
  border: 1px solid #3498db;
  color: #3498db;
}

.btn-outline:hover:not(:disabled) {
  background: #f0f8ff;
}

.btn-danger {
  background: #e74c3c;
  color: white;
}

.btn-danger:hover:not(:disabled) {
  background: #c0392b;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Адаптивность */
@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
  .modal-actions {
    flex-direction: column;
  }
  .btn {
    width: 100%;
  }
}
</style>
