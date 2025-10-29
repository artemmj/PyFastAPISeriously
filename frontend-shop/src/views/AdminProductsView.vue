<template>
    <div class="admin-products">
        <div class="container">
            <h1>Управление товарами</h1>

            <!-- Форма создания нового товара -->
            <div class="create-section">
                <h2>Добавить новый товар</h2>
                <form @submit.prevent="handleCreate" class="create-form">
                    <div class="form-row">
                        <div class="form-group">
                            <label>Название</label>
                            <input v-model="newProduct.title" type="text" required />
                        </div>
                        <div class="form-group">
                            <label>Артикул</label>
                            <input v-model="newProduct.article" type="text" required />
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Цена (₽)</label>
                            <input v-model.number="newProduct.price" type="number" min="0" step="0.01" required />
                        </div>
                        <div class="form-group">
                            <label>Описание</label>
                            <textarea v-model="newProduct.description" rows="2"></textarea>
                        </div>
                    </div>
                    <button type="submit" :disabled="saving" class="btn btn-primary">
                        {{ saving ? 'Создание...' : 'Создать товар' }}
                    </button>
                </form>
            </div>

            <div v-if="loading" class="status-message">Загрузка товаров...</div>
            <div v-else-if="error" class="status-message error">{{ error }}</div>
            <div v-else class="products-table-wrapper">
                <table class="products-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Изображение</th>
                            <th>Артикул</th>
                            <th>Название</th>
                            <th>Цена (₽)</th>
                            <th>Действия</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="product in products" :key="product.id">
                            <td>{{ product.id }}</td>
                            <td class="image-cell">
                                <img
                                    :src="getFullImageUrl(product.image_url)"
                                    :alt="product.title"
                                    class="table-image"
                                    @error="handleImageError"
                                />
                                <label class="upload-label">
                                    📎 Загрузить
                                    <input
                                        type="file"
                                        accept="image/*"
                                        @change="handleFileUpload($event, product.id)"
                                        :disabled="saving"
                                        class="file-input"
                                    />
                                </label>
                            </td>
                            <td>
                                <input
                                    :value="getEditedValue(product.id, 'article')"
                                    @input="e => setEditedValue(product.id, 'article', e.target.value)"
                                    type="text"
                                    class="form-input"
                                    :disabled="saving"
                                />
                            </td>
                            <td>
                                <input
                                    :value="getEditedValue(product.id, 'title')"
                                    @input="e => setEditedValue(product.id, 'title', e.target.value)"
                                    type="text"
                                    class="form-input"
                                    :disabled="saving"
                                />
                            </td>
                            <td>
                                <input
                                    :value="getEditedValue(product.id, 'price')"
                                    @input="e => setEditedValue(product.id, 'price', e.target.value)"
                                    type="number"
                                    min="0"
                                    step="0.01"
                                    class="form-input price-input"
                                    :disabled="saving"
                                />
                            </td>
                            <td class="actions">
                                <button
                                    @click="saveProduct(product.id)"
                                    :disabled="saving || !isProductModified(product.id)"
                                    class="btn btn-primary btn-sm"
                                >
                                    Сохранить
                                </button>
                                <button
                                    @click="resetProduct(product.id)"
                                    :disabled="saving || !isProductModified(product.id)"
                                    class="btn btn-outline btn-sm"
                                >
                                    Отмена
                                </button>
                                <button
                                    @click="() => deleteProduct(product.id)"
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
import { useAdminProducts } from '@/composables/useAdminProducts'

const {
    products,
    loading,
    saving,
    error,
    fetchProducts,
    createProduct,
    updateProduct,
    deleteProduct,
    uploadImage
} = useAdminProducts()

const newProduct = ref({
    title: '',
    article: '',
    price: 0,
    description: ''
})

// Редактируемые данные
const editedProducts = ref({})

// Синхронизирует editedProducts с products
const syncEditedProducts = () => {
    const newEdited = {}
    products.value.forEach(p => {
        // Сохраняем существующие изменения, если есть
        if (editedProducts.value[p.id]) {
            newEdited[p.id] = { ...editedProducts.value[p.id] }
        } else {
            newEdited[p.id] = { ...p }
        }
    })
    editedProducts.value = newEdited
}

const handleCreate = async () => {
    try {
        const newProductObj = await createProduct(newProduct.value)
        // ✅ Инициализируем editedProducts для нового товара
        editedProducts.value[newProductObj.id] = { ...newProductObj }
        // Сброс формы
        newProduct.value = { title: '', article: '', price: 0, description: '' }
    } catch (err) {
        console.error('Ошибка создания:', err)
    }
}

// Загрузка изображения
const handleFileUpload = async (event, productId) => {
    const file = event.target.files[0]
    if (!file) return

    try {
        // Получаем новый image_url
        const newImageUrl = await uploadImage(productId, file)
        // Обновляем editedProducts вручную
        if (editedProducts.value[productId]) {
            editedProducts.value[productId].image_url = newImageUrl
        }
        event.target.value = ''
    } catch (err) {
        console.error('Ошибка загрузки изображения:', err)
        alert('Не удалось загрузить изображение: ' + err.message)
    }
}

// Остальные функции
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const getFullImageUrl = (url) => {
    if (!url) return ''
    return url.startsWith('http') ? url : API_BASE_URL + url
}

const handleImageError = (e) => {
    e.target.src = ''
}

const isProductModified = (id) => {
    const original = products.value.find(p => p.id === id)
    const edited = editedProducts.value[id]
    if (!original || !edited) return false
    return (
        original.title !== edited.title ||
        original.article !== edited.article ||
        original.price !== edited.price ||
        original.description !== edited.description ||
        original.image_url !== edited.image_url
    )
}

const saveProduct = async (id) => {
    try {
        await updateProduct(id, editedProducts.value[id])
        syncEditedProducts() // обновляем после сохранения
    } catch (err) {
        console.error('Ошибка сохранения:', err)
    }
}

const resetProduct = (id) => {
    const original = products.value.find(p => p.id === id)
    if (original) {
        editedProducts.value[id] = { ...original }
    }
}

// Безопасное получение значения из editedProducts
const getEditedValue = (productId, field) => {
    return editedProducts.value[productId]?.[field] ?? ''
}

// Безопасная установка значения
const setEditedValue = (productId, field, value) => {
    if (!editedProducts.value[productId]) {
        // Инициализируем, если ещё не создано
        const original = products.value.find(p => p.id === productId)
        editedProducts.value[productId] = original ? { ...original } : { id: productId }
    }
    editedProducts.value[productId][field] = value
}

// Загрузка и синхронизация
onMounted(() => {
    fetchProducts().then(syncEditedProducts)
})

// Также синхронизируем при изменении products (на случай удаления)
watch(products, syncEditedProducts)
</script>

<style scoped>
.admin-products {
  padding: 2rem 0;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

h1 {
  text-align: center;
  margin-bottom: 2rem;
  color: #2c3e50;
}

.status-message {
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
}

.status-message.error {
  color: #e74c3c;
}

.products-table-wrapper {
  overflow-x: auto;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  padding: 1rem;
}

.products-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 800px;
}

.products-table th,
.products-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.products-table th {
  background: #f8f9fa;
  font-weight: 600;
  color: #2c3e50;
  white-space: nowrap;
}

.products-table tbody tr:hover {
  background: #fafbff;
}

.image-cell {
  width: 80px;
  text-align: center;
}

.table-image {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.95rem;
}

.price-input {
  max-width: 120px;
}

.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.btn-sm {
  padding: 0.4rem 0.8rem;
  font-size: 0.85rem;
  border-radius: 6px;
}

.btn-primary {
  background: #3498db;
  color: white;
  border: none;
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
  border: none;
}

.btn-danger:hover:not(:disabled) {
  background: #c0392b;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

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
}

.create-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #2c3e50;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
}

/* Загрузка изображения */
.upload-label {
  display: block;
  margin-top: 0.5rem;
  font-size: 0.85rem;
  color: #3498db;
  cursor: pointer;
  text-align: center;
}

.upload-label:hover {
  text-decoration: underline;
}

.file-input {
  display: none;
}

/* Адаптивность */
@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>