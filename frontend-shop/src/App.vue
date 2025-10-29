<template>
    <div id="app">
        <TheHeader />
        <main class="main">
            <router-view />
        </main>
        <footer class="footer">
            © 2025 ShopVue — Интернет-магазин
        </footer>
    </div>
</template>

<script setup>
import TheHeader from '@/components/layout/TheHeader.vue'
</script>

<style>
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
    color: #333;
}

#app {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

.header, .footer {
    padding: 1rem;
    background: #f8f9fa;
    text-align: center;
}

.main {
    flex: 1;
    padding: 2rem;
}
</style>
