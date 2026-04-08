<script setup>
import { computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { usePlanStore } from "@/stores/plan";

const route = useRoute();
const router = useRouter();
const auth = useAuthStore();
const plan = usePlanStore();

const links = [
  { name: "admin-dashboard", label: "Дашборд" },
  { name: "admin-services", label: "Услуги" },
  { name: "admin-categories", label: "Категории" },
  { name: "admin-bookings", label: "Записи" },
  { name: "admin-users", label: "Пользователи" },
];

const currentUser = computed(() => auth.state.user || null);

const logout = () => {
  auth.logout();
  plan.reset();
  router.push("/");
};
</script>

<template>
  <div class="admin-shell">
    <aside class="admin-sidebar card">
      <div class="brand">
        <p class="tag">BIZU</p>
        <h2>Панель персонала</h2>
      </div>
      <nav class="admin-nav">
        <router-link
          v-for="link in links"
          :key="link.name"
          :to="{ name: link.name }"
          class="admin-link"
          :class="{ active: route.name === link.name }"
        >
          {{ link.label }}
        </router-link>
      </nav>
      <div class="sidebar-footer">
        <p class="muted">{{ currentUser?.name || currentUser?.email }}</p>
        <button class="cta secondary" type="button" @click="logout">Выйти</button>
      </div>
    </aside>
    <section class="admin-content">
      <header class="admin-top card">
        <h1>Админ-панель</h1>
      </header>
      <router-view />
    </section>
  </div>
</template>

<style scoped>
.admin-shell {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 1rem;
  min-height: calc(100vh - 2rem);
  padding: 1rem;
  background: var(--color-eggshell);
}

.admin-sidebar {
  display: grid;
  grid-template-rows: auto 1fr auto;
  gap: 1rem;
  position: sticky;
  top: 1rem;
  height: fit-content;
}

.brand h2 {
  margin: 0.2rem 0 0;
}

.admin-nav {
  display: grid;
  gap: 0.5rem;
}

.admin-link {
  padding: 0.7rem 0.8rem;
  border-radius: 12px;
  border: 1px solid rgba(52, 95, 32, 0.12);
  background: #fff;
  font-weight: 600;
  color: var(--text-body);
}

.admin-link.active {
  border-color: var(--color-matcha);
  box-shadow: 0 10px 22px rgba(52, 95, 32, 0.12);
}

.sidebar-footer {
  display: grid;
  gap: 0.5rem;
}

.admin-content {
  display: grid;
  gap: 1rem;
  align-content: start;
}

.admin-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

@media (max-width: 960px) {
  .admin-shell {
    grid-template-columns: 1fr;
    padding: 0.8rem;
  }

  .admin-sidebar {
    position: static;
  }
}

@media (max-width: 768px) {
  .admin-shell {
    padding: 0.6rem;
    gap: 0.8rem;
  }

  .admin-nav {
    display: flex;
    overflow-x: auto;
    gap: 0.5rem;
    padding-bottom: 0.25rem;
  }

  .admin-link {
    white-space: nowrap;
    flex: 0 0 auto;
  }

  .sidebar-footer .cta {
    width: 100%;
    min-height: 44px;
  }
}
</style>
