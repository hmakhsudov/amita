<script setup>
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import { useReveal } from "@/composables/useReveal";

const props = defineProps({
  categories: { type: Array, default: () => [] },
  services: { type: Array, default: () => [] },
  selectedCategory: { type: String, default: "all" },
  selectedServiceId: { type: Number, default: null },
});

const emit = defineEmits(["update:category", "select"]);
const { revealRef } = useReveal();
const { t } = useI18n();

const filtered = computed(() => {
  if (props.selectedCategory === "all") return props.services;
  return props.services.filter((s) => s.category === props.selectedCategory);
});
</script>

<template>
  <section class="card reveal" :ref="revealRef">
    <div class="header">
      <div>
        <p class="tag">{{ t("booking.stepService") }}</p>
        <h3>{{ t("services.filterLabel") }}</h3>
        <p class="muted">{{ t("booking.serviceHint") }}</p>
      </div>
      <div class="categories">
        <button
          v-for="cat in categories"
          :key="cat.value"
          class="chip"
          :class="{ active: cat.value === selectedCategory }"
          type="button"
          @click="emit('update:category', cat.value)"
        >
          {{ cat.label }}
        </button>
      </div>
    </div>
    <div class="services">
      <article
        v-for="service in filtered"
        :key="service.id"
        class="service"
        :class="{ chosen: service.id === selectedServiceId }"
        @click="emit('select', service)"
      >
        <div>
          <p class="tag">{{ service.category }}</p>
          <h4>{{ service.name }}</h4>
          <p class="muted">{{ service.description }}</p>
        </div>
        <div class="meta">
          <span class="pill">{{ service.duration }} {{ t("common.minutesShort") }}</span>
          <strong>{{ service.price }} €</strong>
          <button class="cta secondary" type="button">{{ t("booking.choose") }}</button>
        </div>
      </article>
    </div>
  </section>
</template>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
}

.categories {
  display: flex;
  gap: 0.6rem;
  flex-wrap: wrap;
}

.chip {
  border: 1px solid rgba(52, 95, 32, 0.2);
  background: #fff;
  color: var(--color-avocado);
  padding: 0.5rem 0.85rem;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 700;
  transition: all 0.2s ease;
}

.chip.active {
  border-color: var(--color-matcha);
  box-shadow: 0 10px 24px rgba(52, 95, 32, 0.12);
}

.services {
  display: grid;
  gap: 0.8rem;
  margin-top: 1rem;
}

.service {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
  padding: 1rem;
  border-radius: 16px;
  border: 1px solid rgba(52, 95, 32, 0.12);
  background: #fff;
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
  cursor: pointer;
}

.service:hover {
  transform: translateY(-2px);
  box-shadow: 0 16px 32px rgba(52, 95, 32, 0.12);
}

.service.chosen {
  border-color: var(--color-matcha);
  box-shadow: 0 18px 36px rgba(52, 95, 32, 0.14);
}

.meta {
  display: grid;
  gap: 0.35rem;
  justify-items: end;
  min-width: 160px;
}

@media (max-width: 768px) {
  .service {
    flex-direction: column;
    align-items: flex-start;
  }
  .meta {
    justify-items: start;
  }
}

@media (max-width: 768px) {
  .meta .cta {
    width: 100%;
    min-height: 44px;
  }
}
</style>
