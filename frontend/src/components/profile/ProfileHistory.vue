<script setup>
const props = defineProps({
  history: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
  error: { type: String, default: "" },
});

const formatDateTime = (value) => {
  const date = new Date(value);
  const dateLabel = date.toLocaleDateString("ru-RU", {
    day: "2-digit",
    month: "long",
  });
  const timeLabel = date.toLocaleTimeString("ru-RU", { hour: "2-digit", minute: "2-digit" });
  return `${dateLabel} • ${timeLabel}`;
};
</script>

<template>
  <div class="card">
    <div class="section-heading">
      <p class="tag">История</p>
      <h3>Прошедшие визиты</h3>
    </div>

    <div v-if="loading" class="list">
      <div v-for="n in 2" :key="n" class="row skeleton"></div>
    </div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="!history.length" class="empty muted">
      Пока нет завершённых посещений.
    </div>
    <div v-else class="list">
      <article v-for="item in history" :key="item.id" class="row">
        <div>
          <h4>{{ item.service?.name }}</h4>
          <p class="muted">
            {{ formatDateTime(item.start_at) }} •
            {{ item.master?.name || "Мастер салона" }}
          </p>
          <p class="muted">Стоимость: {{ item.service?.price }} ₽</p>
          <p class="status done">Выполнено</p>
        </div>
        <button class="cta secondary" type="button">Оставить отзыв</button>
      </article>
    </div>
  </div>
</template>

<style scoped>
.list {
  display: grid;
  gap: 0.8rem;
}

.row {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.85rem;
  border-radius: 14px;
  border: 1px solid rgba(52, 95, 32, 0.12);
  background: #fff;
}

.status {
  display: inline-block;
  padding: 0.2rem 0.6rem;
  border-radius: 999px;
  font-size: 0.85rem;
  font-weight: 700;
}

.done {
  background: rgba(52, 95, 32, 0.12);
  color: var(--color-avocado);
}

.empty {
  padding: 0.6rem 0;
}

.error {
  color: #8a1a1a;
  font-weight: 600;
}

.skeleton {
  min-height: 90px;
  background: linear-gradient(90deg, #f1ead8, #ffffff, #f1ead8);
  background-size: 200% 100%;
  animation: shimmer 1.4s infinite;
}

@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

@media (max-width: 640px) {
  .row {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
