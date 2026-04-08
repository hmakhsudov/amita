<script setup>
import { useI18n } from "vue-i18n";
import { useReveal } from "@/composables/useReveal";

const { t } = useI18n();
const { revealRef } = useReveal();
</script>

<template>
  <section class="section recommend">
    <div class="section-heading reveal" :ref="revealRef">
      <p class="tag">{{ t("home.assistantTag") }}</p>
      <h2>{{ t("home.assistantHeadline") }}</h2>
      <p class="muted">{{ t("home.assistantText") }}</p>
    </div>
    <div class="card recommend-card reveal" :ref="revealRef">
      <div class="top">
        <div>
          <p class="pill">{{ t("home.assistantPill") }}</p>
          <h3>{{ t("home.assistantCardTitle") }}</h3>
          <p class="muted">{{ t("home.assistantCardText") }}</p>
        </div>
        <router-link class="cta secondary" to="/assistant">
          {{ t("home.assistantCardCta") }}
        </router-link>
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

@media (max-width: 768px) {
  .top {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
