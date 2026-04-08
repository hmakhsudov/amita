<script setup>
import { computed, onMounted, ref } from "vue";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import { useReveal } from "@/composables/useReveal";
import { fetchMasters } from "@/api/masters";
import { useAuthStore } from "@/stores/auth";
import { useChatStore } from "@/stores/chat";

const masters = ref([]);
const loading = ref(false);
const error = ref("");
const toast = ref("");
const auth = useAuthStore();
const chat = useChatStore();
const router = useRouter();
const { t } = useI18n();
const isAuthenticated = computed(() => auth.isAuthenticated.value);
const isMaster = computed(() => auth.state.user?.role === "master");
const isStaffAdmin = computed(() => auth.state.user?.role === "admin");
const { revealRef } = useReveal();

const loadMasters = async () => {
  loading.value = true;
  error.value = "";
  try {
    const data = await fetchMasters();
    masters.value = Array.isArray(data) ? data : [];
  } catch (err) {
    error.value = t("masters.loadError");
  } finally {
    loading.value = false;
  }
};

const startChat = async (masterId) => {
  if (isMaster.value || isStaffAdmin.value) return;
  if (!isAuthenticated.value) {
    toast.value = t("masters.loginToMessage");
    setTimeout(() => {
      toast.value = "";
      router.push("/login");
    }, 1200);
    return;
  }
  try {
    await chat.openConversation(masterId);
    router.push({ name: "profile", query: { tab: "messages" } });
  } catch (err) {
    toast.value = t("messages.openError");
    setTimeout(() => {
      toast.value = "";
    }, 1600);
  }
};

const initials = (name) => {
  if (!name) return "B";
  return name.trim()[0]?.toUpperCase() || "B";
};

onMounted(loadMasters);
</script>

<template>
  <div class="page">
    <section class="section">
      <div class="section-heading reveal" :ref="revealRef">
        <p class="tag">{{ t("nav.masters") }}</p>
        <h1>{{ t("masters.title") }}</h1>
        <p class="muted">{{ t("masters.subtitle") }}</p>
      </div>

      <div v-if="loading" class="grid">
        <div v-for="n in 4" :key="n" class="card master-card skeleton"></div>
      </div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else-if="!masters.length" class="card empty">
        <p class="muted">{{ t("masters.empty") }}</p>
      </div>

      <div v-else class="grid">
        <article v-for="master in masters" :key="master.id" class="card master-card reveal" :ref="revealRef">
          <div class="avatar">
            <img v-if="master.avatar_url" :src="master.avatar_url" :alt="master.name" />
            <span v-else>{{ initials(master.name) }}</span>
          </div>
          <div class="info">
            <h3>{{ master.name }}</h3>
            <p class="muted">{{ t("messages.roleMaster") }}</p>
            <p v-if="master.phone" class="muted">{{ master.phone }}</p>
          </div>
          <div v-if="!isMaster && !isStaffAdmin" class="actions">
            <button class="cta primary" type="button" @click="startChat(master.id)">
              {{ t("masters.write") }}
            </button>
          </div>
        </article>
      </div>
      <div v-if="toast" class="toast">{{ toast }}</div>
    </section>
  </div>
</template>

<style scoped>
.page {
  display: grid;
  gap: 1rem;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.master-card {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 0.9rem;
  align-items: center;
}

.avatar {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: rgba(52, 95, 32, 0.08);
  display: grid;
  place-items: center;
  color: var(--color-avocado);
  font-weight: 700;
  overflow: hidden;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.info p {
  margin: 0.2rem 0;
}

.actions {
  grid-column: 1 / -1;
}

.error {
  color: #8a1a1a;
  font-weight: 600;
}

.empty {
  margin-top: 1rem;
}

.toast {
  margin-top: 0.8rem;
  padding: 0.6rem 0.9rem;
  border-radius: 999px;
  background: rgba(232, 234, 108, 0.45);
  color: #2a2d12;
  display: inline-flex;
  font-weight: 600;
}

.skeleton {
  min-height: 120px;
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

@media (max-width: 768px) {
  .grid {
    grid-template-columns: 1fr;
  }
  .master-card {
    grid-template-columns: 1fr;
  }
  .actions .cta {
    width: 100%;
    min-height: 44px;
  }
}
</style>
