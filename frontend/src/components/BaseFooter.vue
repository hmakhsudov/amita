<script setup>
import fruitPattern from "@/assets/fruit-pattern.svg";
</script>

<template>
  <footer class="footer">
    <div class="texture">
      <img :src="fruitPattern" alt="" aria-hidden="true" />
    </div>
    <div class="footer-inner">
      <div>
        <h4>BIZU — салон красоты и healthy bar</h4>
        <p class="muted">Нежный уход, натуральные акценты, автоматизация сервиса.</p>
      </div>
      <div class="contacts">
        <p><strong>Контакты</strong></p>
        <p>+436767460828</p>
        <p>bizu2305@gmail.com</p>
      </div>
      <div class="social">
        <p><strong>Мы рядом</strong></p>
        <p>Telegram · VK</p>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  position: relative;
  overflow: hidden;
  border-top: 1px solid rgba(52, 95, 32, 0.12);
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(8px);
}

.texture {
  position: absolute;
  inset: 0;
  opacity: 0.08;
  pointer-events: none;
}

.texture img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.footer-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1.5rem 1.25rem 2rem;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1rem;
  align-items: start;
}

.footer h4 {
  font-family: "Playfair Display", "Times New Roman", serif;
  margin-bottom: 0.35rem;
}

.footer p {
  margin: 0.2rem 0;
  color: rgba(47, 54, 47, 0.85);
}
</style>
