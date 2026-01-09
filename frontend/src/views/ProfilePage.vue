<template>
  <div class="page">
    <div class="section-heading">
      <p class="tag">Личный кабинет</p>
      <h1>Ваш профиль BIZU</h1>
    </div>
    <div class="card profile-card">
      <div v-if="auth.state.loadingMe" class="skeleton">
        <div class="line"></div>
        <div class="line short"></div>
        <div class="line"></div>
      </div>
      <div v-else class="profile-info">
        <div>
          <p class="tag">Данные профиля</p>
          <h3>{{ auth.state.user?.name || "Профиль" }}</h3>
          <p class="muted">Email: {{ auth.state.user?.email || "—" }}</p>
          <p class="muted">Телефон: {{ auth.state.user?.phone || "—" }}</p>
          <p class="muted">Роль: {{ roleLabel(auth.state.user?.role) }}</p>
        </div>
        <button class="cta secondary" type="button" @click="handleLogout">Выйти</button>
      </div>
    </div>
    <div v-if="auth.state.user?.role === 'admin'" class="card admin-card">
      <div>
        <p class="tag">Админ</p>
        <h3>Управление услугами</h3>
        <p class="muted">Быстрый доступ к добавлению новых услуг.</p>
      </div>
      <router-link class="cta primary" to="/admin/services/new">Добавить услугу</router-link>
    </div>
    <div v-if="auth.state.user?.role === 'client'" class="card plan-card">
      <div>
        <p class="tag">План</p>
        <h3>Мой план процедур</h3>
        <p class="muted">Список выбранных услуг доступен в любое время.</p>
      </div>
      <router-link class="cta secondary" to="/plan">Открыть план</router-link>
    </div>
    <ProfileLayout />
  </div>
</template>

<script setup>
import ProfileLayout from "@/components/profile/ProfileLayout.vue";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";
import { usePlanStore } from "@/stores/plan";

const auth = useAuthStore();
const plan = usePlanStore();
const router = useRouter();

const handleLogout = () => {
  auth.logout();
  plan.reset();
  router.push("/");
};

const roleLabel = (role) => {
  if (role === "admin") return "Администратор";
  if (role === "client") return "Клиент";
  return "—";
};
</script>

<style scoped>
.page {
  display: grid;
  gap: 1rem;
}

.profile-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.profile-info {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  width: 100%;
  align-items: center;
  flex-wrap: wrap;
}

.admin-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.plan-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.skeleton {
  width: 100%;
  display: grid;
  gap: 0.5rem;
}

.line {
  height: 12px;
  border-radius: 999px;
  background: linear-gradient(90deg, #f1ead8, #ffffff, #f1ead8);
  background-size: 200% 100%;
  animation: shimmer 1.4s infinite;
}

.line.short {
  width: 60%;
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
  .profile-card {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
