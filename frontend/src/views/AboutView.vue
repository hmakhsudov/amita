<script setup>
// TODO: заменить на реальные фото брендовых предметов (стаканы, пакеты, вывески)
import { useI18n } from "vue-i18n";
import heroLogo from "@/assets/logo-bizu.svg";
import salonOne from "@/assets/salon-1.jpg";
import salonThree from "@/assets/salon-3.jpg";
import { useReveal } from "@/composables/useReveal";

const { t } = useI18n();

const team = [
  { name: "Амирa", titleKey: "about.teamLead", focusKey: "about.teamLeadFocus" },
  { name: "Лина", titleKey: "about.teamBody", focusKey: "about.teamBodyFocus" },
  { name: "Кай", titleKey: "about.teamOps", focusKey: "about.teamOpsFocus" },
];

const { revealRef } = useReveal();
</script>

<template>
  <div class="about-page">
    <section class="section">
      <div class="hero-card card reveal" :ref="revealRef">
        <div>
          <p class="tag">{{ t("nav.about") }}</p>
          <h1>{{ t("about.title") }}</h1>
        
          <div class="contact-grid">
            <div>
              <strong>{{ t("about.address") }}</strong>
              <p>Austria, 1030, Vienna, Modecenterstraße,20/1/2</p>
            </div>
            <div>
              <strong>{{ t("about.phone") }}</strong>
              <p>+436767460828</p>
            </div>
            <div>
              <strong>{{ t("about.email") }}</strong>
              <p>bizu2305@gmail.com</p>
            </div>
            <div>
              <strong>{{ t("about.hours") }}</strong>
              <p>09:00 - 20:00 {{ t("about.daily") }}</p>
            </div>
          </div>
        </div>
        <div class="logo-block">
          <img :src="heroLogo" :alt="t('about.logoAlt')" />
          <p class="muted">{{ t("about.logoNote") }}</p>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="section-heading reveal" :ref="revealRef">
        <h2>{{ t("about.teamTitle") }}</h2>
        <p class="muted">{{ t("about.teamText") }}</p>
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
            <p class="muted">{{ t(member.titleKey) }}</p>
            <p>{{ t(member.focusKey) }}</p>
          </div>
        </article>
      </div>
    </section>

    <section class="section brand-story">
      <div class="section-heading reveal" :ref="revealRef">
        <p class="tag">{{ t("about.brandStory") }}</p>
        <h2>{{ t("about.brandStoryTitle") }}</h2>
        <p class="muted">{{ t("about.brandStoryText") }}</p>
      </div>
      <div class="story-grid">
        <figure class="story-card reveal" :ref="revealRef">
          <img :src="salonOne" :alt="t('about.brandDrinkAlt')" />
          <figcaption>{{ t("about.brandDrink") }}</figcaption>
        </figure>
        <figure class="story-card reveal" :ref="revealRef">
          <img :src="salonThree" :alt="t('about.brandInteriorAlt')" />
          <figcaption>{{ t("about.brandInterior") }}</figcaption>
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

@media (max-width: 768px) {
  .hero-card {
    grid-template-columns: 1fr;
  }
}
</style>
