<script setup>
import { useReveal } from "@/composables/useReveal";

// TODO: заменить на реальные брендовые предметы (стаканы, пакеты, вывески)
import salonOne from "@/assets/salon-1.jpg";
import salonTwo from "@/assets/salon-2.jpg";

const { revealRef } = useReveal();
</script>

<template>
  <section class="section about">
    <div class="about-card card reveal" :ref="revealRef">
      <div>
        <p class="tag">О бренде</p>
        <h2>BIZU — beauty & healthy bar</h2>
        <p class="muted">
          BIZU объединяет уход за кожей и телом, мягкий wellness‑подход и эстетичный сервис. Мы
          работаем в тёплой eggshell‑палитре с акцентами avocado/matcha и спокойной атмосферой.
        </p>
      </div>
      <div class="brand-grid">
        <figure class="brand-item">
          <img :src="salonOne" alt="Брендовые напитки" />
          <figcaption>Фирменные напитки</figcaption>
        </figure>
        <figure class="brand-item">
          <img :src="salonTwo" alt="Уютное пространство" />
          <figcaption>Детали интерьера</figcaption>
        </figure>
      </div>
    </div>
  </section>
</template>

<style scoped>
.about-card {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1rem;
  background: radial-gradient(circle at 20% 20%, rgba(168, 195, 159, 0.12), transparent),
    var(--card);
}

.brand-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 0.8rem;
}

.brand-item {
  margin: 0;
  position: relative;
  overflow: hidden;
  border-radius: 14px;
  background: #f7f3ea;
  box-shadow: 0 16px 30px rgba(31, 58, 43, 0.12);
}

.brand-item img {
  width: 100%;
  height: 160px;
  object-fit: cover;
}

.brand-item figcaption {
  position: absolute;
  inset: auto 0 0 0;
  padding: 0.6rem 0.8rem;
  background: linear-gradient(180deg, transparent, rgba(0, 0, 0, 0.42));
  color: #fff;
  font-weight: 700;
}
</style>
