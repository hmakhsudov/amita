<script setup>
import { useI18n } from "vue-i18n";
import AboutBrand from "@/components/AboutBrand.vue";
import BenefitsSection from "@/components/BenefitsSection.vue";
import GallerySection from "@/components/GallerySection.vue";
import HeroSection from "@/components/HeroSection.vue";
import RecommendationSection from "@/components/RecommendationSection.vue";
import { useReveal } from "@/composables/useReveal";

const { revealRef } = useReveal();
const { t } = useI18n();
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
          <p class="tag">{{ t("home.contactTag") }}</p>
          <h3>{{ t("home.contactTitle") }}</h3>

          <div class="contact-details">
            <p><strong>{{ t("home.contactPhone") }}</strong>+436767460828</p>
            <p><strong>{{ t("home.contactEmail") }}</strong> bizu2305@gmail.com</p>
            <p>
              <strong>{{ t("home.contactHours") }}</strong> 09:00 - 20:00
              {{ t("home.contactDaily") }}
            </p>
            <p>
              <strong>{{ t("home.contactAddress") }}</strong> Austria, 1030, Vienna,
              Modecenterstraße,20/1/2
            </p>
          </div>
        </div>
        <div class="map-placeholder">
          <span class="pill">{{ t("home.contactMap") }}</span>
          <div class="map-frame">
            <iframe
              src="https://www.google.com/maps?q=Modecenterstra%C3%9Fe%2020%2C%201030%20Wien%2C%20Austria&output=embed"
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
