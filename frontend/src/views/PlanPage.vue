<script setup>
import { computed, onMounted } from "vue";
import { useI18n } from "vue-i18n";
import { usePlanStore } from "@/stores/plan";
import { useAuthStore } from "@/stores/auth";

const plan = usePlanStore();
const auth = useAuthStore();
const isAuthorized = computed(() => auth.isAuthenticated.value);
const { t } = useI18n();

const loadPlan = async () => {
  if (!isAuthorized.value) return;
  try {
    await plan.fetchPlan();
  } catch (error) {
    // errors are stored in the plan state
  }
};

onMounted(loadPlan);

const removeItem = async (id) => {
  try {
    await plan.removeItem(id);
  } catch (error) {
    // errors are stored in the plan state
  }
};

const clearAll = async () => {
  try {
    await plan.clearPlan();
  } catch (error) {
    // errors are stored in the plan state
  }
};
</script>

<template>
  <section class="section">
    <div class="section-heading">
      <p class="tag">{{ t("plan.title") }}</p>
      <h1>{{ t("plan.title") }}</h1>
      <p class="muted">{{ t("plan.subtitle") }}</p>
    </div>

    <div v-if="!isAuthorized" class="card empty">
      <p class="muted">{{ t("plan.loginHint") }}</p>
      <router-link class="cta secondary" to="/login">{{ t("nav.login") }}</router-link>
    </div>

    <div v-else-if="plan.state.loading" class="card plan-card">
      <div class="items">
        <div v-for="n in 3" :key="n" class="plan-item skeleton"></div>
      </div>
    </div>

    <div v-else-if="plan.state.error" class="card empty">
      <p class="error">{{ plan.state.error }}</p>
      <button class="cta secondary" type="button" @click="loadPlan">
        {{ t("common.retry") }}
      </button>
    </div>

    <div v-else-if="!plan.state.items.length" class="card empty">
      <p class="muted">{{ t("plan.empty") }}</p>
      <router-link class="cta secondary" to="/services">{{ t("plan.toServices") }}</router-link>
    </div>

    <div v-else class="card plan-card">
      <div class="items">
        <article v-for="item in plan.state.items" :key="item.id" class="plan-item">
          <div>
            <h3>{{ item.service?.name }}</h3>
            <p class="muted">{{ item.service?.category?.name || t("services.uncategorized") }}</p>
            <p class="muted">{{ t("plan.qty") }}: {{ item.qty }}</p>
          </div>
          <div class="price">
            <strong>{{ item.service?.price }} €</strong>
            <button class="cta secondary" type="button" @click="removeItem(item.id)">
              {{ t("favorites.remove") }}
            </button>
          </div>
        </article>
      </div>
      <div class="footer">
        <div>
          <p class="muted">{{ t("plan.total") }}</p>
          <strong>{{ plan.total.value.toFixed(2) }} €</strong>
        </div>
        <div class="actions">
          <button class="cta secondary" type="button" @click="clearAll">
            {{ t("plan.clear") }}
          </button>
          <router-link class="cta primary" to="/booking">{{ t("plan.toBooking") }}</router-link>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.plan-card {
  display: grid;
  gap: 1rem;
}

.items {
  display: grid;
  gap: 0.8rem;
}

.plan-item {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.9rem;
  border-radius: 14px;
  border: 1px solid rgba(52, 95, 32, 0.12);
  background: #fff;
}

.skeleton {
  min-height: 90px;
  background: linear-gradient(90deg, #f1ead8, #ffffff, #f1ead8);
  background-size: 200% 100%;
  animation: shimmer 1.4s infinite;
}

.price {
  display: grid;
  gap: 0.4rem;
  text-align: right;
}

.footer {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
  padding-top: 0.6rem;
  border-top: 1px solid rgba(52, 95, 32, 0.08);
}

.actions {
  display: flex;
  gap: 0.6rem;
  flex-wrap: wrap;
}

.empty {
  display: grid;
  gap: 0.8rem;
  justify-items: start;
}

.error {
  color: #8a1a1a;
  font-weight: 600;
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
  .plan-item {
    flex-direction: column;
    align-items: flex-start;
  }
  .price {
    text-align: left;
  }
}

@media (max-width: 768px) {
  .actions {
    width: 100%;
  }
  .actions .cta {
    width: 100%;
    min-height: 44px;
  }
}
</style>
