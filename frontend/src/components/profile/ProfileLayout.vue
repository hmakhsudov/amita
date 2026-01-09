<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue";
import ProfileDashboard from "./ProfileDashboard.vue";
import ProfileFavorites from "./ProfileFavorites.vue";
import ProfileHistory from "./ProfileHistory.vue";
import ProfileSettings from "./ProfileSettings.vue";
import ProfileSidebar from "./ProfileSidebar.vue";
import ProfileProfile from "./ProfileProfile.vue";
import ProfileMasterBookings from "./ProfileMasterBookings.vue";
import ProfileMyServices from "./ProfileMyServices.vue";
import ProfileMessages from "./ProfileMessages.vue";
import { useAuthStore } from "@/stores/auth";
import { useBookingsStore } from "@/stores/bookings";
import { useFavoritesStore } from "@/stores/favorites";
import { useChatStore } from "@/stores/chat";
import { useRoute } from "vue-router";

// TODO: заменить заглушки данными из API профиля
const clientTabs = [
  { key: "bookings", label: "Мои записи" },
  { key: "messages", label: "Сообщения" },
  { key: "favorites", label: "Избранные услуги" },
  { key: "history", label: "История посещений" },
  { key: "profile", label: "Профиль" },
  // { key: "settings", label: "Настройки" }, НАСТРОЙКИ ВКЛАДКА НАСТРОЕК
];
const masterTabs = [
  { key: "profile", label: "Профиль" },
  { key: "master-bookings", label: "Записи ко мне" },
  { key: "master-services", label: "Мои услуги" },
  { key: "messages", label: "Сообщения" },
];

const route = useRoute();
const auth = useAuthStore();
const bookingsStore = useBookingsStore();
const favoritesStore = useFavoritesStore();
const chatStore = useChatStore();

const isMaster = computed(() => auth.state.user?.role === "admin");
const tabs = computed(() => (isMaster.value ? masterTabs : clientTabs));
const allowedTabs = computed(() => tabs.value.map((tab) => tab.key));
const defaultTab = computed(() => (isMaster.value ? "master-bookings" : "bookings"));
const active = ref(defaultTab.value);
const statusToast = ref("");

const settings = ref({ theme: "light", notifications: true });

const activeComponent = computed(() => {
  switch (active.value) {
    case "bookings":
      return {
        component: ProfileDashboard,
        props: {
          bookings: bookingsStore.state.items,
          loading: bookingsStore.state.loading,
          error: bookingsStore.state.error,
        },
      };
    case "favorites":
      return {
        component: ProfileFavorites,
        props: {
          favorites: favoritesStore.state.favorites,
          loading: favoritesStore.state.loading,
          error: favoritesStore.state.error,
        },
      };
    case "history":
      return {
        component: ProfileHistory,
        props: {
          history: bookingsStore.state.historyItems,
          loading: bookingsStore.state.historyLoading,
          error: bookingsStore.state.historyError,
        },
      };
    case "messages":
      return { component: ProfileMessages, props: {} };
    case "profile":
      return { component: ProfileProfile, props: { user: auth.state.user } };
    case "master-bookings":
      return {
        component: ProfileMasterBookings,
        props: {
          bookings: bookingsStore.state.items,
          loading: bookingsStore.state.loading,
          error: bookingsStore.state.error,
          toast: statusToast.value,
        },
      };
    case "master-services":
      return { component: ProfileMyServices, props: {} };
    case "settings":
      return { component: ProfileSettings, props: { settings: settings.value } };
    default:
      return {
        component: ProfileDashboard,
        props: {
          bookings: bookingsStore.state.items,
          loading: bookingsStore.state.loading,
          error: bookingsStore.state.error,
        },
      };
  }
});

const updateSettings = (next) => {
  settings.value = next;
};

const loadBookings = async () => {
  try {
    await bookingsStore.fetchMyBookings();
  } catch (error) {
    // errors are stored in the store
  }
};

const loadMasterBookings = async () => {
  try {
    await bookingsStore.fetchMasterBookings();
  } catch (error) {
    // errors are stored in the store
  }
};

const handleCancel = async (id) => {
  try {
    await bookingsStore.cancelBooking(id);
  } catch (error) {
    // errors are stored in the store
  }
};

const handleStatus = async ({ id, status }) => {
  try {
    await bookingsStore.updateStatus(id, status);
    const label =
      status === "completed"
        ? "Выполнено"
        : status === "cancelled"
          ? "Отменено"
          : "Ожидается";
    statusToast.value = `Статус изменён: ${label}`;
    setTimeout(() => {
      statusToast.value = "";
    }, 2000);
  } catch (error) {
    // errors are stored in the store
  }
};

const handleMessage = async (counterpartId) => {
  active.value = "messages";
  if (counterpartId) {
    try {
      await chatStore.openConversation(counterpartId);
    } catch (error) {
      // errors are stored in the store
    }
  }
};

const loadFavorites = async () => {
  try {
    await favoritesStore.fetchFavorites();
  } catch (error) {
    // errors are stored in the store
  }
};

const loadHistory = async () => {
  try {
    await bookingsStore.fetchHistory();
  } catch (error) {
    // errors are stored in the store
  }
};

const handleRemoveFavorite = async (favoriteId) => {
  try {
    await favoritesStore.removeFavorite(favoriteId);
  } catch (error) {
    // errors are stored in the store
  }
};

const syncActiveTab = () => {
  const requested = typeof route.query.tab === "string" ? route.query.tab : "";
  if (requested && allowedTabs.value.includes(requested)) {
    active.value = requested;
    return;
  }
  active.value = allowedTabs.value.includes(defaultTab.value)
    ? defaultTab.value
    : allowedTabs.value[0] || "profile";
};

const handleVisibility = () => {
  if (document.visibilityState !== "visible") return;
  if (active.value === "bookings") {
    loadBookings();
  }
  if (active.value === "history") {
    loadHistory();
  }
  if (active.value === "favorites") {
    loadFavorites();
  }
};

watch(
  () => active.value,
  (next) => {
    if (next === "bookings") {
      loadBookings();
    }
    if (next === "history") {
      loadHistory();
    }
    if (next === "favorites") {
      loadFavorites();
    }
    if (next === "master-bookings") {
      loadMasterBookings();
    }
  },
  { immediate: true }
);

watch([() => route.query.tab, tabs], syncActiveTab, { immediate: true });

onMounted(() => {
  syncActiveTab();
  document.addEventListener("visibilitychange", handleVisibility);
});

onBeforeUnmount(() => {
  document.removeEventListener("visibilitychange", handleVisibility);
});
</script>

<template>
  <div class="layout">
    <ProfileSidebar :tabs="tabs" :active="active" @change="(k) => (active = k)" />
    <div class="content">
      <Transition name="page" mode="out-in">
        <component
          :is="activeComponent.component"
          v-bind="activeComponent.props"
          :key="active"
          @update:settings="updateSettings"
          @cancel="handleCancel"
          @status="handleStatus"
          @remove="handleRemoveFavorite"
          @message="handleMessage"
        />
      </Transition>
    </div>
  </div>
</template>

<style scoped>
.layout {
  display: grid;
  grid-template-columns: 260px 1fr;
  gap: 1rem;
}

@media (max-width: 960px) {
  .layout {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .layout {
    gap: 0.8rem;
  }
}
</style>
