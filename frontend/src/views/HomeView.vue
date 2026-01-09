<script setup>
import AboutBrand from "@/components/AboutBrand.vue";
import BenefitsSection from "@/components/BenefitsSection.vue";
import GallerySection from "@/components/GallerySection.vue";
import HeroSection from "@/components/HeroSection.vue";
import RecommendationSection from "@/components/RecommendationSection.vue";
import { useReveal } from "@/composables/useReveal";

const { revealRef } = useReveal();
</script>

<template>
  <div>
    <HeroSection />
    <BenefitsSection />
    <GallerySection />
    <RecommendationSection />
    <AboutBrand />

    <section class="section contact">
      <div class="contact-card card reveal" :ref="revealRef">
        <div>
          <p class="tag">Контакты</p>
          <h3>Приезжайте в BIZU</h3>

          <div class="contact-details">
            <p><strong>Телефон:</strong>+436767460828</p>
            <p><strong>Email:</strong> bizu2305@gmail.com</p>
            <p><strong>Часы:</strong> 09:00 - 20:00 ежедневно</p>
            <p><strong>Адрес:</strong> Austria, 1030, Vienna, Modecenterstraße,20/1/2</p>
          </div>
        </div>
        <div class="map-placeholder">
          <span class="pill">Карта</span>
          <div class="map-frame">
            <iframe
              src="https://yandex.ru/map-widget/v1/?um=constructor%3A7377667564c81b856068bf4eb7d235a8cc3de9818826f14977277e45b9fa5605&amp;source=constructor"
              width="500"
              height="500"
              frameborder="0"
            ></iframe>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.contact-card {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1rem;
  align-items: center;
  overflow: hidden;
}

.contact-details {
  display: grid;
  gap: 0.35rem;
}

.map-placeholder {
  border: 1px dashed rgba(52, 95, 32, 0.22);
  border-radius: 14px;
  padding: 1rem;
  min-height: 160px;
  display: grid;
  gap: 0.4rem;
  align-items: center;
  justify-items: start;
  background-size: 220px;
}

.map-frame {
  width: 100%;
}

.map-placeholder iframe {
  width: 100%;
  height: 260px;
  border: 0;
  display: block;
}

@media (max-width: 768px) {
  .contact-card {
    grid-template-columns: 1fr;
  }
  .map-placeholder iframe {
    height: 220px;
  }
}
</style>
