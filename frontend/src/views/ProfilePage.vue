<template>
  <div class="page">
    <div class="section-heading">
      <p class="tag">{{ t("nav.profile") }}</p>
      <h1>{{ t("profile.title") }}</h1>
    </div>
    <div class="card profile-card">
      <div v-if="auth.state.loadingMe" class="skeleton">
        <div class="line"></div>
        <div class="line short"></div>
        <div class="line"></div>
      </div>
      <div v-else class="profile-info">
        <div>
          <p class="tag">{{ t("profile.dataTitle") }}</p>
          <h3>{{ auth.state.user?.name || t("profile.profileFallback") }}</h3>
          <p class="muted">{{ t("profile.email") }}: {{ auth.state.user?.email || "—" }}</p>
          <p class="muted">{{ t("profile.phone") }}: {{ auth.state.user?.phone || "—" }}</p>
          <p class="muted">{{ t("profile.role") }}: {{ roleLabel(auth.state.user?.role) }}</p>
        </div>
        <button class="cta secondary" type="button" @click="handleLogout">
          {{ t("nav.logout") }}
        </button>
      </div>
    </div>
    <div v-if="auth.state.user?.role === 'master'" class="card admin-card">
      <div>
        <p class="tag">Мастер</p>
        <h3>Управление своими услугами</h3>
        <p class="muted">Добавляйте и редактируйте услуги, а также ведите переписку с клиентами.</p>
      </div>
      <router-link class="cta primary" :to="{ path: '/profile', query: { tab: 'master-services' } }">
        Мои услуги
      </router-link>
    </div>
    <div v-if="auth.state.user?.role === 'client'" class="card plan-card">
      <div>
        <p class="tag">{{ t("nav.plan") }}</p>
        <h3>{{ t("profile.planTitle") }}</h3>
        <p class="muted">{{ t("profile.planText") }}</p>
      </div>
      <router-link class="cta secondary" to="/plan">{{ t("profile.openPlan") }}</router-link>
    </div>
    <ProfileLayout />
  </div>
</template>

<script setup>
import ProfileLayout from "@/components/profile/ProfileLayout.vue";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";
import { usePlanStore } from "@/stores/plan";
import { useI18n } from "vue-i18n";

const auth = useAuthStore();
const plan = usePlanStore();
const router = useRouter();
const { t } = useI18n();

const handleLogout = () => {
  auth.logout();
  plan.reset();
  router.push("/");
};

const roleLabel = (role) => {
  if (role === "admin") return t("profile.admin");
  if (role === "master") return t("profile.master");
  if (role === "client") return t("profile.client");
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

@media (max-width: 768px) {
  .page {
    gap: 0.8rem;
  }

  .profile-card {
    flex-direction: column;
    align-items: flex-start;
  }

  .profile-info {
    flex-direction: column;
    align-items: flex-start;
  }

  .admin-card,
  .plan-card {
    flex-direction: column;
    align-items: flex-start;
  }

  .profile-card .cta,
  .admin-card .cta,
  .plan-card .cta {
    width: 100%;
    min-height: 44px;
  }
}
</style>
