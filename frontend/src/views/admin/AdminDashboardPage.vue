<script setup>
import { onMounted, ref } from "vue";
import { fetchAdminDashboard } from "@/api/admin";

const loading = ref(false);
const error = ref("");
const stats = ref({
  total_users: 0,
  total_bookings: 0,
  today_bookings: 0,
  total_revenue: 0,
  popular_services: [],
});

const loadDashboard = async () => {
  loading.value = true;
  error.value = "";
  try {
    const data = await fetchAdminDashboard();
    stats.value = {
      ...stats.value,
      ...data,
      popular_services: Array.isArray(data?.popular_services) ? data.popular_services : [],
    };
  } catch (err) {
    error.value = "Не удалось загрузить статистику.";
  } finally {
    loading.value = false;
  }
};

onMounted(loadDashboard);
</script>

<template>
  <section class="admin-page">
    <div class="section-heading">
      <p class="tag">Статистика</p>
      <h2>Дашборд</h2>
    </div>
    <div v-if="loading" class="card">Загрузка...</div>
    <div v-else-if="error" class="card error">{{ error }}</div>
    <template v-else>
      <div class="stats-grid">
        <article class="card stat">
          <p class="muted">Пользователи</p>
          <h3>{{ stats.total_users }}</h3>
        </article>
        <article class="card stat">
          <p class="muted">Все записи</p>
          <h3>{{ stats.total_bookings }}</h3>
        </article>
        <article class="card stat">
          <p class="muted">Записи сегодня</p>
          <h3>{{ stats.today_bookings }}</h3>
        </article>
        <article class="card stat">
          <p class="muted">Выручка</p>
          <h3>{{ Number(stats.total_revenue || 0).toFixed(2) }} €</h3>
        </article>
      </div>
      <div class="card">
        <h3>Популярные услуги</h3>
        <p v-if="!stats.popular_services.length" class="muted">Пока нет данных.</p>
        <div v-else class="popular-list">
          <article
            v-for="item in stats.popular_services"
            :key="item.service_id"
            class="popular-row"
          >
            <strong>{{ item.name }}</strong>
            <span class="pill">{{ item.bookings_count }} записей</span>
          </article>
        </div>
      </div>
    </template>
  </section>
</template>

<style scoped>
.admin-page {
  display: grid;
  gap: 1rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 0.8rem;
}

.stat h3 {
  margin: 0.2rem 0 0;
}

.popular-list {
  display: grid;
  gap: 0.6rem;
  margin-top: 0.6rem;
}

.popular-row {
  display: flex;
  justify-content: space-between;
  gap: 0.8rem;
  align-items: center;
  padding: 0.7rem;
  border: 1px solid rgba(52, 95, 32, 0.12);
  border-radius: 12px;
}

.error {
  color: #8a1a1a;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
    gap: 0.6rem;
  }

  .popular-row {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
