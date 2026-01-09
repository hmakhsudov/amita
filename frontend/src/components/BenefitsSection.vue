<script setup>
import { useReveal } from "@/composables/useReveal";

const benefits = [
  {
    title: "Выберите услугу",
    text: "Каталог процедур с понятными ценами и длительностью. Можно выбрать мастера.",
  },
  {
    title: "Запишитесь онлайн",
    text: "Выберите дату и время — запись сохраняется сразу в системе.",
  },
  {
    title: "Личный кабинет",
    text: "Ваши записи, избранные услуги, план процедур и история посещений в одном месте.",
  },
];

const { revealRef } = useReveal();
</script>

<template>
  <section class="section">
    <div class="section-heading reveal" :ref="revealRef">
      <p class="tag">Как это работает</p>
      <h2>Запись и уход — просто и прозрачно</h2>
      <p class="muted">Выбирайте услуги, записывайтесь онлайн и управляйте визитами в кабинете.</p>
    </div>
    <div class="grid">
      <article
        v-for="benefit in benefits"
        :key="benefit.title"
        class="card benefit reveal"
        :ref="revealRef"
      >
        <div class="icon"></div>
        <h3>{{ benefit.title }}</h3>
        <p class="muted">{{ benefit.text }}</p>
      </article>
    </div>
    <div class="actions">
      <router-link class="cta primary" to="/booking">Записаться онлайн</router-link>
      <router-link class="cta secondary" to="/profile">Личный кабинет</router-link>
    </div>
  </section>
</template>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1rem;
}

.benefit {
  position: relative;
  overflow: hidden;
  transition: transform 0.25s ease, box-shadow 0.25s ease;
  background: linear-gradient(180deg, rgba(232, 234, 108, 0.08), rgba(255, 255, 255, 0.9));
}

.benefit:hover {
  transform: translateY(-4px);
  box-shadow: 0 24px 48px rgba(52, 95, 32, 0.12);
}

.icon {
  width: 36px;
  height: 36px;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--color-avocado), var(--color-matcha));
  opacity: 0.9;
  margin-bottom: 0.6rem;
}

.actions {
  margin-top: 1rem;
  display: flex;
  gap: 0.8rem;
  flex-wrap: wrap;
}

@media (max-width: 768px) {
  .actions {
    width: 100%;
  }
  .actions .cta {
    width: 100%;
    min-height: 44px;
  }
}
</style>
