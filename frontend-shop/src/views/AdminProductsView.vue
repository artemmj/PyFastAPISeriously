<template>
    <div class="admin-products">
        <div class="container">
            <div class="page-header">
                <h1>Управление товарами</h1>
                <button @click="openCreateModal" class="btn btn-primary">+ Добавить товар</button>
            </div>

            <div v-if="loading && products.length === 0" class="status-message">Загрузка товаров...</div>
            <div v-else-if="error" class="status-message error">{{ error }}</div>
            <div v-else-if="products.length === 0" class="status-message">Товары не найдены</div>
            <div v-else class="products-table-wrapper">
                <table class="products-table">
                    <thead>
                        <tr>
                        <th>ID</th>
                        <th>Изображение</th>
                        <th>Название</th>
                        <th>Категория</th>
                        <th>Артикул</th>
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
                            </td>
                            <td>{{ product.title }}</td>
                            <td>{{ product.category?.title || '—' }}</td>
                            <td>{{ product.article }}</td>
                            <td>{{ product.price }} ₽</td>
                            <td class="actions">
                                <button @click="openEditModal(product)" class="btn btn-outline btn-sm">Редактировать</button>
                                <button @click="() => deleteProduct(product.id)" :disabled="saving" class="btn btn-danger btn-sm">
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
                        <h3>{{ editingProduct ? 'Редактировать товар' : 'Добавить товар' }}</h3>
                        <button @click="closeModal" class="modal-close">&times;</button>
                    </div>
                    <form @submit.prevent="handleSubmit" class="modal-form">
                        <div class="form-row">
                            <div class="form-group">
                                <label>Название</label>
                                <input v-model="modalForm.title" type="text" required />
                            </div>
                            <div class="form-group">
                                <label>Категория</label>
                                <select v-model.number="modalForm.category_id" required class="form-select">
                                    <option value="">Выберите категорию</option>
                                    <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                                        {{ cat.title }}
                                    </option>
                                </select>
                            </div>
                        </div>
                        <div class="form-row">
                            <div class="form-group">
                                <label>Артикул</label>
                                <input v-model="modalForm.article" type="text" required />
                            </div>
                            <div class="form-group">
                                <label>Цена (₽)</label>
                                <input v-model.number="modalForm.price" type="number" min="0" step="0.01" required />
                            </div>
                            <div class="form-group">
                                <label>Изображение</label>
                                <div class="image-upload">
                                <img
                                    v-if="imagePreview"
                                    :src="imagePreview"
                                    alt="Предпросмотр"
                                    class="preview-image"
                                />
                                <label class="upload-label">
                                    📎 Выбрать файл
                                    <input
                                    type="file"
                                    accept="image/*"
                                    @change="handleFileChange"
                                    ref="fileInput"
                                    class="file-input"
                                    />
                                </label>
                                <p v-if="selectedFileName" class="file-name">{{ selectedFileName }}</p>
                                </div>
                            </div>
                        </div>
                        <div class="form-row">
                            <div class="form-group">
                                <label>Описание</label>
                                <textarea v-model="modalForm.description" rows="3"></textarea>
                            </div>
                        </div>
                        <div class="modal-actions">
                            <button type="submit" :disabled="saving" class="btn btn-primary">
                                {{ saving ? 'Сохранение...' : (editingProduct ? 'Сохранить' : 'Создать') }}
                            </button>
                            <button @click="closeModal" type="button" class="btn btn-outline">Отмена</button>
                        </div>
                    </form>
                </div>
            </div>

            <!-- Управление категориями -->
            <div class="categories-section">
                <div class="page-header">
                    <h2>Категории товаров</h2>
                    <button @click="openCategoryModal(null)" class="btn btn-primary">+ Добавить категорию</button>
                </div>

                <div v-if="categoriesLoading" class="status-message">Загрузка категорий...</div>
                <div v-else-if="categories.length === 0" class="status-message">Нет категорий</div>
                <div v-else class="categories-list">
                    <div v-for="cat in categories" :key="cat.id" class="category-item">
                        <span>{{ cat.title }}</span>
                        <div class="category-actions">
                            <button @click="openCategoryModal(cat)" class="btn btn-outline btn-sm">
                                Редактировать
                            </button>
                            <button @click="() => deleteCategory(cat.id)" :disabled="saving" class="btn btn-danger btn-sm">
                                Удалить
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Модалка категории (создание/редактирование) -->
            <div v-if="isCategoryModalOpen" class="modal-overlay" @click="closeCategoryModal">
                <div class="modal" @click.stop>
                    <div class="modal-header">
                        <h3>{{ editingCategory ? 'Редактировать категорию' : 'Добавить категорию' }}</h3>
                        <button @click="closeCategoryModal" class="modal-close">&times;</button>
                    </div>
                    <form @submit.prevent="handleCategorySubmit" class="modal-form">
                        <div class="form-group">
                            <label>Название категории</label>
                            <input v-model="categoryForm.title" type="text" required />
                        </div>
                        <div class="modal-actions">
                            <button type="submit" :disabled="saving" class="btn btn-primary">
                            {{ saving ? 'Сохранение...' : (editingCategory ? 'Сохранить' : 'Создать') }}
                            </button>
                            <button @click="closeCategoryModal" type="button" class="btn btn-outline">Отмена</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
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
    uploadImage,
    categories,
    categoriesLoading,
    fetchCategories,
    createCategory,
    updateCategory,
    deleteCategory
} = useAdminProducts()

// === Товары ===
const isModalOpen = ref(false)
const editingProduct = ref(null)
const modalForm = ref({
    title: '',
    category_id: null,
    article: '',
    price: 0,
    description: ''
})

// Файл и превью
const fileInput = ref(null)
const imageFile = ref(null)
const imagePreview = ref(null)
const selectedFileName = ref('')

// === Категории ===
const newCategoryTitle = ref('')

// URL для изображений
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const getFullImageUrl = (url) => {
    if (!url) return ''
    return url.startsWith('http') ? url : API_BASE_URL + url
}

const handleImageError = (e) => {
    e.target.src = ''
}

// Обработка выбора файла
const handleFileChange = (event) => {
    const file = event.target.files[0]
    if (file) {
        imageFile.value = file
        selectedFileName.value = file.name

        // Превью
        const reader = new FileReader()
        reader.onload = (e) => {
            imagePreview.value = e.target.result
        }
        reader.readAsDataURL(file)
    } else {
        resetFile()
    }
}

// Сброс файла
const resetFile = () => {
    imageFile.value = null
    imagePreview.value = null
    selectedFileName.value = ''
    if (fileInput.value) fileInput.value.value = ''
}

// Открыть модалку создания
const openCreateModal = () => {
    editingProduct.value = null
    modalForm.value = { title: '', category_id: null, article: '', price: 0, description: '' }
    resetFile()
    isModalOpen.value = true
}

// Открыть модалку редактирования
const openEditModal = (product) => {
    editingProduct.value = product
    modalForm.value = {
        title: product.title,
        category_id: product.category?.id || null,
        article: product.article,
        price: product.price,
        description: product.description || ''
    }
    // Сброс файла (новое изображение — опционально)
    resetFile()
    // Превью текущего изображения
    if (product.image_url) {
        imagePreview.value = getFullImageUrl(product.image_url)
    }
    isModalOpen.value = true
}

// Закрыть модалку
const closeModal = () => {
    isModalOpen.value = false
    editingProduct.value = null
    resetFile()
}

// Отправка формы
const handleSubmit = async () => {
    try {
        if (editingProduct.value) {
            // Редактирование
            await updateProduct(editingProduct.value.id, modalForm.value)
            // Загрузка изображения, если файл выбран
            if (imageFile.value) {
                await uploadImage(editingProduct.value.id, imageFile.value)
            }
        } else {
            // Создание
            const newProduct = await createProduct(modalForm.value)
            // Загрузка изображения, если файл выбран
            if (imageFile.value) {
                await uploadImage(newProduct.id, imageFile.value)
            }
        }
        closeModal()
        fetchProducts()
    } catch (err) {
        console.error('Ошибка:', err)
    }
}

// === Категории ===
const isCategoryModalOpen = ref(false)
const editingCategory = ref(null) // null = создание, объект = редактирование
const categoryForm = ref({ title: '' })

// Открыть модалку категории (создание или редактирование)
const openCategoryModal = (category) => {
    editingCategory.value = category
    categoryForm.value = {
        title: category?.title || ''
    }
    isCategoryModalOpen.value = true
}

const closeCategoryModal = () => {
    isCategoryModalOpen.value = false
    editingCategory.value = null
}

// Отправка формы категории
const handleCategorySubmit = async () => {
    try {
        if (editingCategory.value) {
            await updateCategory(editingCategory.value.id, categoryForm.value)
        } else {
            await createCategory(categoryForm.value)
        }
        closeCategoryModal()
    } catch (err) {
        console.error('Ошибка:', err)
    }
}

// Загрузка
onMounted(() => {
    fetchProducts()
    fetchCategories()
})
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

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.page-header h1 {
  color: #2c3e50;
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

.actions {
  display: flex;
  gap: 0.5rem;
}

/* Модальное окно — те же стили, что и у пользователей */
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
.form-select,
textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
}

textarea {
  resize: vertical;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}

/* Кнопки — общие стили */
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

/* Загрузка изображения в модалке */
.image-upload {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.75rem;
}

.preview-image {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.upload-label {
  display: inline-block;
  padding: 0.5rem 1rem;
  background: #f0f8ff;
  color: #3498db;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.95rem;
}

.upload-label:hover {
  background: #e1f0ff;
}

.file-input {
  display: none;
}

.file-name {
  font-size: 0.85rem;
  color: #7f8c8d;
  margin: 0;
}

.categories-section {
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 2px solid #eee;
}

.categories-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(500px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.category-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.category-actions {
  display: flex;
  gap: 0.5rem;
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
