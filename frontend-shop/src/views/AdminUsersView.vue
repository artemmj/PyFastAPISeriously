<template>
  <div class="admin-users">
    <div class="container">
      <!-- Форма создания нового пользователя -->
      <div class="create-section">
        <h2>Добавить пользователя</h2>
        <form @submit.prevent="handleCreate" class="create-form">
          <div class="form-row">
            <div class="form-group">
              <label>Имя</label>
              <input v-model="newUser.first_name" type="text" required />
            </div>
            <div class="form-group">
              <label>Фамилия</label>
              <input v-model="newUser.last_name" type="text" required />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Email</label>
              <input v-model="newUser.email" type="email" required />
            </div>
            <div class="form-group">
              <label>Телефон</label>
              <input v-model="newUser.phone_number" type="text" required />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Пароль</label>
              <input v-model="newUser.password" type="password" minlength="6" required />
            </div>
            <div class="form-group">
              <label>Роль</label>
              <select v-model.number="newUser.role_id" class="form-select">
                <option :value="1">Админ</option>
                <option :value="2">Модератор</option>
                <option :value="3">Пользователь</option>
              </select>
            </div>
          </div>
          <button type="submit" :disabled="saving" class="btn btn-primary">
            {{ saving ? 'Создание...' : 'Создать пользователя' }}
          </button>
        </form>
      </div>

      <!-- Заголовок и таблица -->
      <h1>Управление пользователями</h1>

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
              <td>
                <div class="name-fields">
                  <input
                    :value="getEditedValue(user.id, 'first_name')"
                    @input="e => setEditedValue(user.id, 'first_name', e.target.value)"
                    type="text"
                    class="form-input"
                    :disabled="saving"
                  />
                  <input
                    :value="getEditedValue(user.id, 'last_name')"
                    @input="e => setEditedValue(user.id, 'last_name', e.target.value)"
                    type="text"
                    class="form-input"
                    :disabled="saving"
                  />
                </div>
              </td>
              <td>
                <input
                  :value="getEditedValue(user.id, 'email')"
                  @input="e => setEditedValue(user.id, 'email', e.target.value)"
                  type="email"
                  class="form-input"
                  :disabled="saving"
                />
              </td>
              <td>
                <input
                  :value="getEditedValue(user.id, 'phone_number')"
                  @input="e => setEditedValue(user.id, 'phone_number', e.target.value)"
                  type="text"
                  class="form-input"
                  :disabled="saving"
                />
              </td>
              <td>
                <select
                  :value="getEditedValue(user.id, 'role_id')"
                  @change="e => setEditedValue(user.id, 'role_id', parseInt(e.target.value))"
                  :disabled="saving"
                  class="role-select"
                >
                  <option :value="1">Админ</option>
                  <option :value="2">Модератор</option>
                  <option :value="3">Пользователь</option>
                </select>
              </td>
              <td class="actions">
                <button
                  @click="saveUser(user.id)"
                  :disabled="saving || !isUserModified(user.id)"
                  class="btn btn-primary btn-sm"
                >
                  Сохранить
                </button>
                <button
                  @click="resetUser(user.id)"
                  :disabled="saving || !isUserModified(user.id)"
                  class="btn btn-outline btn-sm"
                >
                  Отмена
                </button>
                <button
                  @click="() => deleteUser(user.id)"
                  :disabled="saving"
                  class="btn btn-danger btn-sm"
                >
                  Удалить
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
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

// Данные нового пользователя
const newUser = ref({
  first_name: '',
  last_name: '',
  email: '',
  phone_number: '',
  password: '',
  confirm_password: '',
  role_id: 3
})

// Редактируемые копии существующих пользователей
const editedUsers = ref({})

const syncEditedUsers = () => {
    const newEdited = {}
    users.value.forEach(p => {
        if (editedUsers.value[p.id]) {
            newEdited[p.id] = { ...editedUsers.value[p.id] }
        } else {
            newEdited[p.id] = { ...p }
        }
    })
    editedUsers.value = newEdited
}

// Безопасное чтение значения
const getEditedValue = (userId, field) => {
  return editedUsers.value[userId]?.[field] ?? ''
}

// Безопасная запись значения
const setEditedValue = (userId, field, value) => {
  if (!editedUsers.value[userId]) {
    const original = users.value.find(u => u.id === userId)
    editedUsers.value[userId] = original ? { ...original } : { id: userId }
  }
  editedUsers.value[userId][field] = value
}

// Проверка, были ли внесены изменения
const isUserModified = (userId) => {
  const original = users.value.find(u => u.id === userId)
  const edited = editedUsers.value[userId]
  if (!original || !edited) return false
  return (
    original.first_name !== edited.first_name ||
    original.last_name !== edited.last_name ||
    original.email !== edited.email ||
    original.phone_number !== edited.phone_number ||
    original.role_id !== edited.role_id
  )
}

// Сохранить изменения
const saveUser = async (userId) => {
  try {
    await updateUser(userId, editedUsers.value[userId])
    // Обновляем editedUsers после успешного сохранения
    const updated = users.value.find(u => u.id === userId)
    if (updated) {
      editedUsers.value[userId] = { ...updated }
    }
  } catch (err) {
    console.error('Ошибка сохранения пользователя:', err)
  }
}

// Отменить изменения
const resetUser = (userId) => {
  const original = users.value.find(u => u.id === userId)
  if (original) {
    editedUsers.value[userId] = { ...original }
  }
}

// Создать нового пользователя
const handleCreate = async () => {
  try {
    newUser.value.confirm_password = newUser.value.password  // TODO
    await createUser(newUser.value)
    // Сброс формы
    newUser.value = {
      first_name: '',
      last_name: '',
      email: '',
      phone_number: '',
      password: '',
      role_id: 2
    }
  } catch (err) {
    console.error('Ошибка создания пользователя:', err)
  }
}

// Загрузка при монтировании
onMounted(() => {
  fetchUsers().then(syncEditedUsers)
})

watch(users, syncEditedUsers)
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

.name-fields {
  display: flex;
  gap: 0.5rem;
}

.name-fields .form-input {
  flex: 1;
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

/* Адаптивность */
@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }

  .name-fields {
    flex-direction: column;
    gap: 0.5rem;
  }
}
</style>
