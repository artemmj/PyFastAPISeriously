<template>
    <div class="about-page">
        <div class="container">
            <h1>О нас</h1>

            <section class="intro">
                <p>
                    <strong>ShopVue</strong> — современный интернет-магазин, созданный для тех, кто ценит качество, удобство и скорость.
                </p>
                <p>
                    Мы тщательно отбираем товары, работаем напрямую с проверенными поставщиками и заботимся о каждом клиенте — от выбора до доставки.
                </p>
            </section>

            <section class="values">
                <h2>Наши ценности</h2>
                <div class="values-grid">
                    <div class="value-item">
                        <h3>Качество</h3>
                        <p>Только проверенные товары с гарантией производителя.</p>
                    </div>
                    <div class="value-item">
                        <h3>Простота</h3>
                        <p>Интуитивный интерфейс и быстрое оформление заказа.</p>
                    </div>
                    <div class="value-item">
                        <h3>Поддержка</h3>
                        <p>Помогаем 24/7 — до и после покупки.</p>
                    </div>
                </div>
            </section>

            <section class="team">
                <h2>Команда</h2>
                <p>За ShopVue стоит небольшая, но увлечённая команда разработчиков и логистов, объединённых общей целью — сделать онлайн-шопинг приятным и надёжным.</p>
            </section>

            <section class="contact">
                <h2>Связаться с нами</h2>
                <p>📧 <a href="mailto:hello@shopvue.local">hello@shopvue.local</a></p>
                <p>📞 +7 (495) 123-45-67</p>
            </section>
        </div>
    </div>
</template>

<script setup>
</script>

<style scoped>
.about-page {
  padding: 3rem 0;
  line-height: 1.7;
  color: #2c3e50;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

h1 {
  font-size: 2.5rem;
  font-weight: 700;
  text-align: center;
  margin-bottom: 2.5rem;
  color: #2c3e50;
}

h2 {
  font-size: 1.8rem;
  margin: 2.5rem 0 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #eee;
  color: #2c3e50;
}

p {
  margin-bottom: 1.25rem;
  font-size: 1.05rem;
  color: #34495e;
}

strong {
  color: #3498db;
}

.values-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.75rem;
  margin-top: 1rem;
}

.value-item h3 {
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
  color: #3498db;
}

.value-item p {
  margin-bottom: 0;
  color: #7f8c8d;
}

.contact a {
  color: #3498db;
  text-decoration: none;
}

.contact a:hover {
  text-decoration: underline;
}

/* Адаптивность */
@media (max-width: 600px) {
  h1 {
    font-size: 2rem;
  }

  h2 {
    font-size: 1.5rem;
  }
}
</style>