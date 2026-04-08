<script setup>
import { useI18n } from "vue-i18n";
import { useReveal } from "@/composables/useReveal";

const props = defineProps({
  service: { type: Object, default: null },
  master: { type: Object, default: null },
  slot: { type: String, default: "" },
  slotLabel: { type: String, default: "" },
  form: { type: Object, default: () => ({}) },
});

const emit = defineEmits(["confirm"]);
const { revealRef } = useReveal();
const { t } = useI18n();
</script>

<template>
  <section class="card reveal" :ref="revealRef">
    <div class="section-heading">
      <p class="tag">{{ t("booking.stepConfirm") }}</p>
      <h3>{{ t("booking.confirmTitle") }}</h3>
    </div>
    <div class="summary-grid">
      <div class="summary-item">
        <p class="muted">{{ t("booking.summaryService") }}</p>
        <strong>{{ service?.name || t("booking.summaryNone") }}</strong>
      </div>
      <div class="summary-item">
        <p class="muted">{{ t("booking.summaryTime") }}</p>
        <strong>{{ slotLabel || slot || t("booking.summaryNone") }}</strong>
      </div>
      <div class="summary-item">
        <p class="muted">{{ t("booking.summaryMaster") }}</p>
        <strong>{{ master?.name || t("booking.summaryNone") }}</strong>
      </div>
      <div class="summary-item">
        <p class="muted">{{ t("booking.summaryClient") }}</p>
        <strong>{{ form.name || t("booking.summaryClientName") }}</strong>
        <p class="muted">{{ form.phone }}</p>
        <p class="muted">{{ form.email }}</p>
      </div>
    </div>
    <button class="cta primary" type="button" @click="emit('confirm')">
      {{ t("booking.confirm") }}
    </button>
  </section>
</template>

<style scoped>
.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 0.9rem;
  margin-bottom: 1rem;
}

.summary-item {
  padding: 0.75rem;
  border-radius: 12px;
  border: 1px solid rgba(52, 95, 32, 0.12);
  background: #fff;
}

@media (max-width: 768px) {
  .cta {
    width: 100%;
    min-height: 44px;
  }
}
</style>
