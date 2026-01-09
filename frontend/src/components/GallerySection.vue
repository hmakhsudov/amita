<script setup>
import { useReveal } from "@/composables/useReveal";

// TODO: заменить на реальные фото из брендбука (авокадо, напитки, брендовые предметы)
import salonOne from "@/assets/salon-1.jpg";
import salonTwo from "@/assets/salon-2.jpg";
import salonThree from "@/assets/salon-3.jpg";
import salonFive from "@/assets/salon-5.jpg";
import salonSix from "@/assets/salon-6.jpg";
import salonSeven from "@/assets/salon-7.jpg";
import heroMain from "@/assets/hero-main.jpg";

const items = [
  { title: "Матча-коктейли", src: salonOne },
  { title: "Уютные кресла", src: salonTwo },
  { title: "Фирменные напитки", src: salonThree },
  { title: "Девушки с смузи", src: heroMain },
];

const { revealRef } = useReveal();
</script>

<template>
  <section class="section">
    <div class="section-heading reveal" :ref="revealRef">
      <p class="tag">Галерея</p>
      <h2>Пространство, напитки и детали бренда</h2>
      <p class="muted">Лайтовые тона, акцентные matcha/avocado детали, мягкий свет.</p>
    </div>
    <div class="gallery-grid">
      <figure v-for="item in items" :key="item.title" class="gallery-item reveal" :ref="revealRef">
        <img :src="item.src" :alt="item.title" />
        <figcaption>{{ item.title }}</figcaption>
      </figure>
    </div>
  </section>
</template>

<style scoped>
.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1rem;
}

.gallery-item {
  position: relative;
  overflow: hidden;
  border-radius: 18px;
  box-shadow: 0 18px 36px rgba(52, 95, 32, 0.1);
  background: #f8f4ec;
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.gallery-item img {
  width: 100%;
  height: 220px;
  object-fit: cover;
  transition: transform 0.25s ease;
}

.gallery-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 22px 46px rgba(52, 95, 32, 0.14);
}

.gallery-item:hover img {
  transform: scale(1.04);
}

.gallery-item figcaption {
  position: absolute;
  inset: auto 0 0 0;
  padding: 0.75rem 1rem;
  background: linear-gradient(180deg, transparent, rgba(0, 0, 0, 0.42));
  color: #fff;
  font-weight: 700;
}
</style>
