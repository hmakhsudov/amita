<script setup>
import { computed, onMounted, ref } from "vue";
import { useReveal } from "@/composables/useReveal";
import { fetchCategories, fetchServices } from "@/api/services";
import { usePlanStore } from "@/stores/plan";
import { useAuthStore } from "@/stores/auth";
import { useFavoritesStore } from "@/stores/favorites";
import { useRouter } from "vue-router";

const services = ref([]);
const categories = ref([]);
const loading = ref(false);
const error = ref("");
const toast = ref("");
const plan = usePlanStore();
const auth = useAuthStore();
const favorites = useFavoritesStore();
const router = useRouter();
const isClient = computed(() => auth.state.user?.role === "client");
const canShowFavorites = computed(
  () => !auth.isAuthenticated.value || auth.state.user?.role === "client"
);

const selectedCategory = ref("Все");
const { revealRef } = useReveal();

const categoryOptions = computed(() => {
  if (categories.value.length) {
    return ["Все", ...categories.value.map((c) => c.name)];
  }
  const uniq = new Set(services.value.map((s) => s.categoryName));
  return ["Все", ...uniq];
});

const filteredServices = computed(() => {
  if (selectedCategory.value === "Все") return services.value;
  return services.value.filter((service) => service.categoryName === selectedCategory.value);
});

const addToPlan = async (service) => {
  if (!auth.isAuthenticated.value) {
    toast.value = "Войдите, чтобы сохранить план.";
    setTimeout(() => {
      toast.value = "";
      router.push("/login");
    }, 1200);
    return;
  }
  try {
    await plan.addToPlan(service.id, 1);
    toast.value = "Добавлено в план.";
  } catch (err) {
    toast.value = plan.state.error || "Не удалось добавить услугу в план.";
  } finally {
    setTimeout(() => {
      toast.value = "";
    }, 1800);
  }
};

const toggleFavorite = async (service) => {
  if (!auth.isAuthenticated.value) {
    toast.value = "Войдите, чтобы добавить в избранное.";
    setTimeout(() => {
      toast.value = "";
      router.push("/login");
    }, 1200);
    return;
  }
  try {
    if (favorites.isFavorite(service.id)) {
      const favId = favorites.findFavoriteId(service.id);
      if (favId) {
        await favorites.removeFavorite(favId);
      }
      toast.value = "Удалено из избранного.";
    } else {
      await favorites.addFavorite(service.id);
      toast.value = "Добавлено в избранное.";
    }
  } catch (err) {
    toast.value = favorites.state.error || "Не удалось обновить избранное.";
  } finally {
    setTimeout(() => {
      toast.value = "";
    }, 1800);
  }
};

const loadData = async () => {
  loading.value = true;
  error.value = "";
  try {
    const [servicesData, categoriesData] = await Promise.all([
      fetchServices(),
      fetchCategories(),
    ]);
    categories.value = Array.isArray(categoriesData) ? categoriesData : [];
    services.value = Array.isArray(servicesData)
      ? servicesData.map((item) => ({
          id: item.id,
          name: item.name,
          description: item.description,
          price: item.price,
          duration_minutes: item.duration_minutes,
          categoryName: item.category?.name || item.category_name || "Без категории",
        }))
      : [];
    if (auth.isAuthenticated.value && isClient.value) {
      try {
        await favorites.fetchFavorites();
      } catch (favError) {
        // errors are stored in the store
      }
    }
  } catch (err) {
    error.value = "Не удалось загрузить услуги. Попробуйте позже.";
  } finally {
    loading.value = false;
  }
};

onMounted(loadData);
</script>

<template>
  <section class="section">
    <div class="header reveal" :ref="revealRef">
      <div>
        <p class="tag">Услуги</p>
        <h1>Мягкие beauty-ритуалы</h1>
        <p class="muted">
          Страница подготовлена для будущей интеграции с системой рекомендаций. Когда API будет
          подключен, карточки автоматически обновятся.
        </p>
      </div>
      <div class="note card">
        <strong>Скоро:</strong>
        <p class="muted">
          • Автоподбор процедур <br />
          • Онлайн-бронирование <br />
          • Напоминания и планы
        </p>
      </div>
    </div>

    <div class="filters card reveal" :ref="revealRef">
      <span class="muted">Фильтр по категориям:</span>
      <div class="filter-pills">
        <button
          v-for="cat in categoryOptions"
          :key="cat"
          class="filter"
          :class="{ active: cat === selectedCategory }"
          type="button"
          @click="selectedCategory = cat"
        >
          {{ cat }}
        </button>
      </div>
    </div>

    <div v-if="loading" class="service-grid">
      <div v-for="n in 3" :key="n" class="card service-card skeleton-card"></div>
    </div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <div v-else-if="!filteredServices.length" class="card empty">
      <p class="muted">Пока нет услуг в этой категории.</p>
    </div>

    <div v-else class="service-grid">
      <article
        v-for="service in filteredServices"
        :key="service.id"
        class="card service-card reveal"
        :ref="revealRef"
      >
        <div class="service-head">
          <div>
            <p class="tag">{{ service.categoryName }}</p>
            <h3>{{ service.name }}</h3>
          </div>
          <div class="price">
            <strong>{{ service.price }} ₽</strong>
            <span class="muted">{{ service.duration_minutes }} мин</span>
          </div>
        </div>
        <p class="muted">
          {{ service.description || "Описание услуги появится после подключения полного описания." }}
        </p>
        <button
          v-if="canShowFavorites"
          class="cta secondary"
          type="button"
          @click="toggleFavorite(service)"
        >
          {{ favorites.isFavorite(service.id) ? "Убрать из избранного" : "В избранное" }}
        </button>
        <button class="cta primary" type="button" @click="addToPlan(service)">
          {{
            auth.isAuthenticated.value && plan.has(service.id)
              ? "Добавить еще"
              : "Добавить в план"
          }}
        </button>
      </article>
    </div>
    <div v-if="toast" class="toast">{{ toast }}</div>
  </section>
</template>

<style scoped>
.header {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
  align-items: start;
}

.note {
  background: rgba(255, 255, 255, 0.94);
}

.filters {
  margin: 1.5rem 0;
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  align-items: center;
}

.filter-pills {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.filter {
  background: rgba(52, 95, 32, 0.08);
  color: var(--color-avocado);
  border: 1px solid transparent;
  border-radius: 12px;
  padding: 0.55rem 0.9rem;
  cursor: pointer;
  font-weight: 700;
  transition: all 0.2s ease;
}

.filter.active {
  background: var(--color-avocado);
  color: var(--card);
  border-color: rgba(52, 95, 32, 0.4);
}

.service-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1rem;
}

.service-card {
  display: grid;
  gap: 0.8rem;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.service-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 24px 48px rgba(31, 58, 43, 0.12);
}

.service-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}

.price {
  text-align: right;
}

.error {
  padding: 1rem;
  color: #8a1a1a;
  font-weight: 600;
}

.toast {
  margin-top: 1rem;
  display: inline-flex;
  padding: 0.6rem 1rem;
  border-radius: 999px;
  background: rgba(232, 234, 108, 0.45);
  color: #2a2d12;
  font-weight: 600;
}

.empty {
  display: grid;
  gap: 0.5rem;
  justify-items: start;
}

.skeleton-card {
  min-height: 180px;
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
  .service-head {
    flex-direction: column;
    align-items: flex-start;
  }
  .price {
    text-align: left;
  }
}

@media (max-width: 768px) {
  .filters {
    flex-direction: column;
    align-items: flex-start;
  }
  .filter-pills {
    width: 100%;
    overflow-x: auto;
    flex-wrap: nowrap;
    padding-bottom: 0.2rem;
  }
  .filter {
    white-space: nowrap;
  }
  .service-card .cta {
    width: 100%;
    min-height: 44px;
  }
  .service-card .cta + .cta {
    margin-top: 0.5rem;
  }
}
</style>
