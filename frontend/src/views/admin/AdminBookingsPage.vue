<script setup>
import { onMounted, ref } from "vue";
import { fetchAdminBookings, updateAdminBookingStatus } from "@/api/admin";

const bookings = ref([]);
const loading = ref(false);
const error = ref("");
const pendingMap = ref({});

const statusOptions = [
  { value: "scheduled", label: "Ожидается" },
  { value: "completed", label: "Выполнено" },
  { value: "cancelled", label: "Отменено" },
];

const statusLabel = (value) =>
  statusOptions.find((item) => item.value === value)?.label || value;

const formatDateTime = (value) => {
  const date = new Date(value);
  return `${date.toLocaleDateString("ru-RU")} ${date.toLocaleTimeString("ru-RU", {
    hour: "2-digit",
    minute: "2-digit",
  })}`;
};

const loadBookings = async () => {
  loading.value = true;
  error.value = "";
  try {
    const data = await fetchAdminBookings();
    bookings.value = Array.isArray(data) ? data : [];
    pendingMap.value = {};
    bookings.value.forEach((item) => {
      pendingMap.value[item.id] = item.status;
    });
  } catch (err) {
    error.value = "Не удалось загрузить записи.";
  } finally {
    loading.value = false;
  }
};

const saveStatus = async (bookingId) => {
  error.value = "";
  try {
    const updated = await updateAdminBookingStatus(bookingId, pendingMap.value[bookingId]);
    bookings.value = bookings.value.map((item) => (item.id === updated.id ? updated : item));
  } catch (err) {
    error.value = err.response?.data?.detail || "Не удалось обновить статус.";
  }
};

onMounted(loadBookings);
</script>

<template>
  <section class="admin-page">
    <div class="section-heading">
      <p class="tag">Записи</p>
      <h2>Все записи</h2>
    </div>
    <div v-if="loading" class="card">Загрузка...</div>
    <div v-else-if="error" class="card error">{{ error }}</div>
    <div v-else-if="!bookings.length" class="card">Записей пока нет.</div>
    <div v-else class="card list">
      <article v-for="item in bookings" :key="item.id" class="row">
        <div class="meta">
          <h4>{{ item.service?.name }}</h4>
          <p class="muted">Клиент: {{ item.client_name }} ({{ item.client_phone || "—" }})</p>
          <p class="muted">Мастер: {{ item.master?.name || "—" }}</p>
          <p class="muted">{{ formatDateTime(item.start_at) }}</p>
          <p class="muted">Текущий статус: {{ statusLabel(item.status) }}</p>
        </div>
        <div class="actions">
          <select v-model="pendingMap[item.id]">
            <option v-for="status in statusOptions" :key="status.value" :value="status.value">
              {{ status.label }}
            </option>
          </select>
          <button class="cta secondary" type="button" @click="saveStatus(item.id)">
            Сохранить статус
          </button>
        </div>
      </article>
    </div>
  </section>
</template>

<style scoped>
.admin-page {
  display: grid;
  gap: 1rem;
}

.list {
  display: grid;
  gap: 0.7rem;
}

.row {
  border: 1px solid rgba(52, 95, 32, 0.12);
  border-radius: 12px;
  padding: 0.8rem;
  display: flex;
  justify-content: space-between;
  gap: 1rem;
}

.meta {
  display: grid;
  gap: 0.2rem;
}

.actions {
  display: grid;
  gap: 0.5rem;
  align-content: start;
  min-width: 180px;
}

select {
  border: 1px solid rgba(52, 95, 32, 0.18);
  border-radius: 12px;
  padding: 0.65rem 0.8rem;
  background: #fff;
}

.error {
  color: #8a1a1a;
}

@media (max-width: 768px) {
  .row {
    flex-direction: column;
  }
}
</style>
