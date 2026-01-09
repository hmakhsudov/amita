<script setup>
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
</script>

<template>
  <section class="card reveal" :ref="revealRef">
    <div class="section-heading">
      <p class="tag">Подтверждение</p>
      <h3>Проверьте детали</h3>
    </div>
    <div class="summary-grid">
      <div class="summary-item">
        <p class="muted">Услуга</p>
        <strong>{{ service?.name || "Не выбрано" }}</strong>
      </div>
      <div class="summary-item">
        <p class="muted">Время</p>
        <strong>{{ slotLabel || slot || "Не выбрано" }}</strong>
      </div>
      <div class="summary-item">
        <p class="muted">Мастер</p>
        <strong>{{ master?.name || "Не выбрано" }}</strong>
      </div>
      <div class="summary-item">
        <p class="muted">Клиент</p>
        <strong>{{ form.name || "Имя клиента" }}</strong>
        <p class="muted">{{ form.phone }}</p>
        <p class="muted">{{ form.email }}</p>
      </div>
    </div>
    <button class="cta primary" type="button" @click="emit('confirm')">Подтвердить запись</button>
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
