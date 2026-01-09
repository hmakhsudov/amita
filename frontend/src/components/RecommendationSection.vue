<script setup>
import { useReveal } from "@/composables/useReveal";

const { revealRef } = useReveal();
</script>

<template>
  <section class="section recommend">
    <div class="section-heading reveal" :ref="revealRef">
      <p class="tag">ИИ-ассистент</p>
      <h2>Подбор ухода с помощью ИИ</h2>
      <p class="muted">
        Наш ИИ-ассистент помогает выбрать услуги под ваши цели и состояние кожи и тела.
      </p>
    </div>
    <div class="card recommend-card reveal" :ref="revealRef">
      <div class="top">
        <div>
          <p class="pill">Помощник</p>
          <h3>Индивидуальные рекомендации</h3>
          <p class="muted">
            ИИ учитывает ваши цели, время и комфорт, чтобы подобрать подходящие процедуры из
            каталога.
          </p>
        </div>
        <router-link class="cta secondary" to="/assistant">Попробовать ассистента</router-link>
      </div>
    </div>
  </section>
</template>

<style scoped>
.recommend {
  position: relative;
}

.recommend-card {
  position: relative;
  overflow: hidden;
  background: linear-gradient(180deg, rgba(232, 234, 108, 0.08), rgba(255, 255, 255, 0.92));
}

.recommend-card::after {
  content: "";
  position: absolute;
  inset: -2px;
  background: url("@/assets/fruit-pattern.svg");
  opacity: 0.1;
  pointer-events: none;
}

.recommend-card > * {
  position: relative;
  z-index: 1;
}

.top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
}

@media (max-width: 640px) {
  .top {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
