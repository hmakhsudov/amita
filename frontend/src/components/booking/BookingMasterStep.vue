<script setup>
import { useReveal } from "@/composables/useReveal";
import fallbackAvatar from "@/assets/salon-5.jpg";

const props = defineProps({
  masters: { type: Array, default: () => [] },
  selectedId: { type: Number, default: null },
  hasService: { type: Boolean, default: false },
});

const emit = defineEmits(["select"]);
const { revealRef } = useReveal();
</script>

<template>
  <section class="card reveal" :ref="revealRef">
    <div class="section-heading">
      <p class="tag">Мастер</p>
      <h3>Выберите мастера</h3>
      <p class="muted">Запись возможна только при выборе специалиста.</p>
    </div>
    <p v-if="!masters.length" class="muted">
      {{ hasService ? "Нет доступных мастеров для выбранной услуги." : "Сначала выберите услугу." }}
    </p>
    <div class="grid">
      <article
        v-for="master in masters"
        :key="master.id"
        class="master"
        :class="{ chosen: master.id === selectedId }"
        @click="emit('select', master)"
      >
        <img :src="master.avatar_url || fallbackAvatar" :alt="master.name" />
        <div>
          <h4>{{ master.name }}</h4>
          <p class="muted">{{ master.phone || "Мастер салона BIZU" }}</p>
        </div>
      </article>
    </div>
  </section>
</template>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 0.8rem;
}

.master {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 0.75rem;
  align-items: center;
  padding: 0.9rem;
  border-radius: 16px;
  background: #fff;
  border: 1px solid rgba(52, 95, 32, 0.12);
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
  cursor: pointer;
}

.master:hover {
  transform: translateY(-2px);
  box-shadow: 0 14px 28px rgba(52, 95, 32, 0.12);
}

.master.chosen {
  border-color: var(--color-matcha);
  box-shadow: 0 18px 32px rgba(52, 95, 32, 0.14);
}

.master img {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  object-fit: cover;
}

.small {
  font-size: 0.9rem;
}
</style>
