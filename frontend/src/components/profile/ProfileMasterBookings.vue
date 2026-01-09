<script setup>
import { computed } from "vue";

const props = defineProps({
  bookings: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
  error: { type: String, default: "" },
  toast: { type: String, default: "" },
});

const emit = defineEmits(["status", "message"]);

const now = () => new Date();
const upcoming = computed(() =>
  props.bookings
    .filter((item) => item.status === "scheduled" && new Date(item.start_at) > now())
    .sort((a, b) => new Date(a.start_at) - new Date(b.start_at))
);
const past = computed(() =>
  props.bookings
    .filter((item) => item.status !== "scheduled" || new Date(item.start_at) <= now())
    .sort((a, b) => new Date(b.start_at) - new Date(a.start_at))
);

const formatDateTime = (value) => {
  const date = new Date(value);
  const dateLabel = date.toLocaleDateString("ru-RU", {
    day: "2-digit",
    month: "long",
  });
  const timeLabel = date.toLocaleTimeString("ru-RU", { hour: "2-digit", minute: "2-digit" });
  return `${dateLabel} • ${timeLabel}`;
};

const statusLabel = (status) => {
  if (status === "scheduled") return "Ожидается";
  if (status === "cancelled") return "Отменено";
  if (status === "completed") return "Выполнено";
  return "—";
};

const statusClass = (status) => {
  if (status === "scheduled") return "pending";
  if (status === "completed") return "done";
  return "canceled";
};

const changeStatus = (id, status) => {
  emit("status", { id, status });
};

const openMessage = (clientId) => {
  emit("message", clientId);
};
</script>

<template>
  <div class="card">
    <div class="section-heading">
      <p class="tag">Записи ко мне</p>
      <h3>Управление статусами</h3>
    </div>
    <div v-if="loading" class="grid">
      <div v-for="n in 2" :key="n" class="booking skeleton"></div>
    </div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="!bookings.length" class="empty muted">
      Пока нет записей, назначенных вам как мастеру.
    </div>
    <div v-else class="grid">
      <h4 v-if="upcoming.length" class="subheading">Предстоящие</h4>
      <article v-for="item in upcoming" :key="`up-${item.id}`" class="booking">
        <div>
          <h4>{{ item.service?.name }}</h4>
          <p class="muted">
            Клиент: {{ item.client_name || "—" }} • {{ item.client_phone || "—" }}
          </p>
          <p class="muted">{{ formatDateTime(item.start_at) }}</p>
          <p class="status" :class="statusClass(item.status)">{{ statusLabel(item.status) }}</p>
        </div>
        <div class="actions">
          <button class="cta secondary" type="button" @click="changeStatus(item.id, 'completed')">
            Выполнено
          </button>
          <button class="cta secondary" type="button" @click="changeStatus(item.id, 'cancelled')">
            Отменить
          </button>
          <button
            v-if="item.client_id"
            class="cta secondary"
            type="button"
            @click="openMessage(item.client_id)"
          >
            Написать клиенту
          </button>
        </div>
      </article>

      <h4 v-if="past.length" class="subheading">Прошлые</h4>
      <article v-for="item in past" :key="`past-${item.id}`" class="booking">
        <div>
          <h4>{{ item.service?.name }}</h4>
          <p class="muted">{{ formatDateTime(item.start_at) }}</p>
          <p class="status" :class="statusClass(item.status)">{{ statusLabel(item.status) }}</p>
        </div>
        <div class="actions">
          <button
            v-if="item.client_id"
            class="cta secondary"
            type="button"
            @click="openMessage(item.client_id)"
          >
            Написать клиенту
          </button>
        </div>
      </article>
    </div>
    <p v-if="toast" class="toast">{{ toast }}</p>
  </div>
</template>

<style scoped>
.grid {
  display: grid;
  gap: 0.8rem;
}

.booking {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.9rem;
  border-radius: 14px;
  border: 1px solid rgba(52, 95, 32, 0.12);
  background: #fff;
}

.actions {
  display: flex;
  gap: 0.6rem;
  align-items: center;
}

.status {
  display: inline-block;
  padding: 0.2rem 0.6rem;
  border-radius: 999px;
  font-size: 0.85rem;
  font-weight: 700;
}

.pending {
  background: rgba(232, 234, 108, 0.3);
  color: #2b2d12;
}

.done {
  background: rgba(52, 95, 32, 0.12);
  color: var(--color-avocado);
}

.canceled {
  background: rgba(0, 0, 0, 0.05);
  color: #444;
}

.error {
  color: #8a1a1a;
  font-weight: 600;
}

.toast {
  margin-top: 0.7rem;
  display: inline-flex;
  padding: 0.55rem 0.9rem;
  border-radius: 999px;
  background: rgba(232, 234, 108, 0.45);
  color: #2a2d12;
  font-weight: 600;
}

.empty {
  padding: 0.6rem 0;
}

.subheading {
  margin: 0.4rem 0 0.1rem;
  color: var(--color-avocado);
  font-size: 0.95rem;
  letter-spacing: 0.3px;
}

.skeleton {
  min-height: 92px;
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
  .booking {
    flex-direction: column;
    align-items: flex-start;
  }
  .actions {
    width: 100%;
    flex-wrap: wrap;
  }
}

@media (max-width: 768px) {
  .actions .cta {
    width: 100%;
    min-height: 44px;
  }
}
</style>
