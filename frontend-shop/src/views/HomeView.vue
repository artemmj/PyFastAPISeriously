<template>
    <div class="home">
        <!-- Hero Section -->
        <section class="hero">
            <h1>Добро пожаловать в ShopVue.js!</h1>
            <p>Классные несуществующие товары для всех и каждого — от ничего до всего.</p>
            <router-link to="/catalog" class="btn btn-primary">Смотреть каталог</router-link>
        </section>
    </div>
</template>

<style scoped>
.home {
  padding: 2rem 1rem;
  max-width: 1200px;
  margin: 0 auto;
}

/* Hero */
.hero {
  text-align: center;
  padding: 3rem 1rem;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4edf9 100%);
  border-radius: 12px;
  margin-bottom: 3rem;
}

.hero h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  color: #2c3e50;
}

.hero p {
  font-size: 1.2rem;
  color: #7f8c8d;
  margin-bottom: 1.5rem;
}

/* Buttons */
.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
  display: inline-block;
  text-align: center;
}

.btn-primary {
  background-color: #3498db;
  color: white;
  border: none;
}

.btn-primary:hover {
  background-color: #2980b9;
  transform: translateY(-2px);
}
</style>
