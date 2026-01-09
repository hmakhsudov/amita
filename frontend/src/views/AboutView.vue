<script setup>
// TODO: заменить на реальные фото брендовых предметов (стаканы, пакеты, вывески)
import heroLogo from "@/assets/logo-bizu.svg";
import salonOne from "@/assets/salon-1.jpg";
import salonThree from "@/assets/salon-3.jpg";
import { useReveal } from "@/composables/useReveal";

const team = [
  { name: "Амирa", title: "Лид-терапевт", focus: "Холистичные уходы" },
  { name: "Лина", title: "Специалист по телу", focus: "Расслабляющий массаж" },
  { name: "Кай", title: "Операции", focus: "Клиентский сервис" },
];

const { revealRef } = useReveal();
</script>

<template>
  <div class="about-page">
    <section class="section">
      <div class="hero-card card reveal" :ref="revealRef">
        <div>
          <p class="tag">О компании</p>
          <h1>Премиальный салон красоты и healthy bar</h1>
        
          <div class="contact-grid">
            <div>
              <strong>Адрес</strong>
              <p>Austria, 1030, Vienna, Modecenterstraße,20/1/2</p>
            </div>
            <div>
              <strong>Телефон</strong>
              <p>+436767460828</p>
            </div>
            <div>
              <strong>Email</strong>
              <p>bizu2305@gmail.com</p>
            </div>
            <div>
              <strong>Часы</strong>
              <p>09:00 - 20:00 ежедневно</p>
            </div>
          </div>
        </div>
        <div class="logo-block">
          <img :src="heroLogo" alt="Логотип BIZU" />
          <p class="muted">Скоро добавим брендовые изображения (стаканы, пакеты, вывески).</p>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="section-heading reveal" :ref="revealRef">
        <h2>Команда</h2>
        <p class="muted">
          Люди и технологии вместе: тёплый сервис + автоматизация рекомендаций и записи.
        </p>
      </div>
      <div class="team-grid">
        <article
          v-for="member in team"
          :key="member.name"
          class="card team-card reveal"
          :ref="revealRef"
        >
          <div class="avatar">{{ member.name[0] }}</div>
          <div>
            <h3>{{ member.name }}</h3>
            <p class="muted">{{ member.title }}</p>
            <p>{{ member.focus }}</p>
          </div>
        </article>
      </div>
    </section>

    <section class="section brand-story">
      <div class="section-heading reveal" :ref="revealRef">
        <p class="tag">Бренд-сторис</p>
        <h2>Фирменные предметы</h2>
        <p class="muted">
          Используем фото авокадо, еды, напитков и мерча (стаканы/пакеты) из брендбука. Сейчас —
          заглушки.
        </p>
      </div>
      <div class="story-grid">
        <figure class="story-card reveal" :ref="revealRef">
          <img :src="salonOne" alt="Напитки" />
          <figcaption>Напитки и смузи</figcaption>
        </figure>
        <figure class="story-card reveal" :ref="revealRef">
          <img :src="salonThree" alt="Интерьер" />
          <figcaption>Интерьер в eggshell-палитре</figcaption>
        </figure>
      </div>
    </section>
  </div>
</template>

<style scoped>
.hero-card {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
  align-items: center;
  background: radial-gradient(circle at 25% 25%, rgba(168, 195, 159, 0.12), transparent),
    var(--card);
}

.about-page {
  display: grid;
  gap: 2rem;
}

.logo-block {
  text-align: center;
  background: rgba(255, 255, 255, 0.95);
  padding: 1.25rem;
  border-radius: 16px;
  border: 1px solid rgba(31, 58, 43, 0.12);
}

.logo-block img {
  width: 140px;
}

.contact-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 0.6rem;
  margin-top: 1rem;
}

.team-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1rem;
}

.team-card {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 0.85rem;
  align-items: center;
}

.avatar {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  background: rgba(31, 58, 43, 0.1);
  color: var(--deep-forest);
  display: grid;
  place-items: center;
  font-weight: 800;
  font-size: 1.2rem;
}

.story-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1rem;
}

.story-card {
  position: relative;
  margin: 0;
  overflow: hidden;
  border-radius: 16px;
  box-shadow: 0 18px 40px rgba(31, 58, 43, 0.12);
}

.story-card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.story-card figcaption {
  position: absolute;
  inset: auto 0 0 0;
  padding: 0.75rem 1rem;
  background: linear-gradient(180deg, transparent, rgba(0, 0, 0, 0.45));
  color: #fff;
  font-weight: 700;
}

@media (max-width: 640px) {
  .hero-card {
    grid-template-columns: 1fr;
  }
}
</style>
