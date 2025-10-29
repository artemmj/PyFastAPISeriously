<template>
    <div class="not-found">
        <div class="container">
            <div class="content">
                <div class="illustration">
                    <!-- Простая SVG-иллюстрация (можно заменить на картинку) -->
                    <svg width="200" height="200" viewBox="0 0 200 200" fill="none">
                        <circle cx="100" cy="100" r="90" fill="#f0f4ff"/>
                        <path d="M60 100L85 125L140 75" stroke="#3498db" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>
                        <circle cx="140" cy="75" r="8" fill="#27ae60"/>
                    </svg>
                </div>
                <h1>404</h1>
                <p class="subtitle">Страница не найдена</p>
                <p class="message">
                    Кажется, вы забрели туда, где ничего нет. Но не переживайте — это случается со всеми!
                </p>
                <div class="actions">
                    <router-link to="/" class="btn btn-primary">Вернуться на главную</router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
// Никакой логики — только статическая страница
</script>

<style scoped>
.not-found {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: #f9fafb;
  padding: 2rem 1rem;
}

.container {
  max-width: 600px;
  text-align: center;
}

.content {
  background: white;
  padding: 3rem 2rem;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
}

.illustration {
  margin-bottom: 1.5rem;
}

.illustration svg {
  opacity: 0.9;
}

h1 {
  font-size: 4rem;
  font-weight: 800;
  color: #2c3e50;
  margin: 0 0 0.5rem;
  line-height: 1;
}

.subtitle {
  font-size: 1.5rem;
  color: #3498db;
  margin: 0 0 1.25rem;
  font-weight: 600;
}

.message {
  color: #7f8c8d;
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 2rem;
}

.actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn {
  padding: 0.85rem 1.75rem;
  border-radius: 50px;
  font-weight: 600;
  font-size: 1rem;
  text-decoration: none;
  display: inline-block;
  transition: all 0.3s ease;
  border: none;
}

.btn-primary {
  background: #3498db;
  color: white;
}

.btn-primary:hover {
  background: #2980b9;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
}

.btn-outline {
  background: transparent;
  color: #3498db;
  border: 2px solid #3498db;
}

.btn-outline:hover {
  background: #f0f8ff;
  transform: translateY(-2px);
}

.content {
  animation: fadeIn 0.6s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Адаптивность */
@media (max-width: 600px) {
  h1 {
    font-size: 3rem;
  }

  .subtitle {
    font-size: 1.25rem;
  }

  .actions {
    flex-direction: column;
    align-items: center;
  }

  .btn {
    width: 100%;
    max-width: 280px;
  }
}
</style>
