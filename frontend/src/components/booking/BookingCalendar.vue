<script setup>
import { useReveal } from "@/composables/useReveal";

const props = defineProps({
  selectedDate: { type: String, default: "" },
  minDate: { type: String, default: "" },
  slots: { type: Array, default: () => [] },
  selectedSlot: { type: String, default: "" },
  loading: { type: Boolean, default: false },
  emptyLabel: { type: String, default: "Выберите услугу и дату." },
  disabled: { type: Boolean, default: false },
});

const emit = defineEmits(["update:date", "select"]);
const { revealRef } = useReveal();

const slotValue = (slot) => (typeof slot === "string" ? slot : slot.value);
const slotLabel = (slot) => (typeof slot === "string" ? slot : slot.label);
</script>

<template>
  <section class="card reveal" :ref="revealRef">
    <div class="section-heading">
      <p class="tag">Дата и время</p>
      <h3>Выберите удобное окно</h3>
      <p class="muted">Календарь и слоты в стиле премиальных сервисов записи.</p>
    </div>
    <div class="date-field">
      <label>
        <span>Дата</span>
        <input
          type="date"
          :value="selectedDate"
          :min="minDate"
          :disabled="disabled"
          @input="emit('update:date', $event.target.value)"
        />
      </label>
    </div>
    <div class="slots">
      <template v-if="loading">
        <span class="muted">Загрузка слотов...</span>
      </template>
      <template v-else-if="!slots.length">
        <span class="muted">{{ emptyLabel }}</span>
      </template>
      <template v-else>
        <button
          v-for="slot in slots"
          :key="slotValue(slot)"
          class="slot"
          :class="{ active: slotValue(slot) === selectedSlot }"
          type="button"
          @click="emit('select', slotValue(slot))"
        >
          {{ slotLabel(slot) }}
        </button>
      </template>
    </div>
  </section>
</template>

<style scoped>
.slots {
  display: flex;
  gap: 0.6rem;
  flex-wrap: wrap;
  margin-top: 0.8rem;
}

.date-field {
  margin-top: 0.8rem;
}

label {
  display: grid;
  gap: 0.35rem;
}

span {
  font-weight: 700;
}

input[type="date"] {
  border: 1px solid rgba(52, 95, 32, 0.18);
  background: #fff;
  border-radius: 12px;
  padding: 0.7rem 0.9rem;
  font-family: "Inter", sans-serif;
  font-weight: 600;
}

input[type="date"]:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.slots {
  margin-top: 1.2rem;
}

.slot {
  border: 1px solid rgba(52, 95, 32, 0.18);
  background: #fff;
  color: var(--color-avocado);
  padding: 0.55rem 0.9rem;
  border-radius: 14px;
  cursor: pointer;
  font-weight: 700;
  transition: all 0.2s ease;
  min-width: 82px;
}

.slot.active {
  background: var(--color-matcha);
  color: #1f260f;
  box-shadow: 0 12px 28px rgba(52, 95, 32, 0.14);
}

@media (max-width: 768px) {
  .slots {
    overflow-x: auto;
    flex-wrap: nowrap;
    padding-bottom: 0.4rem;
  }
  .slot {
    flex: 0 0 auto;
  }
}
</style>
