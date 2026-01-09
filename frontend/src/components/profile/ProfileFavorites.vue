<script setup>
import fallbackPhoto from "@/assets/salon-6.jpg";

const props = defineProps({
  favorites: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
  error: { type: String, default: "" },
});

const emit = defineEmits(["remove"]);
</script>

<template>
  <div class="card">
    <div class="section-heading">
      <p class="tag">Избранное</p>
      <h3>Любимые услуги</h3>
    </div>

    <div v-if="loading" class="grid">
      <div v-for="n in 2" :key="n" class="fav skeleton"></div>
    </div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="!favorites.length" class="empty muted">
      Пока нет избранных услуг.
    </div>

    <div v-else class="grid">
      <article v-for="item in favorites" :key="item.id" class="fav">
        <div>
          <h4>{{ item.service?.name }}</h4>
          <p class="muted">{{ item.service?.category?.name || "Без категории" }}</p>
          <p class="muted">{{ item.service?.price }} ₽</p>
          <div class="actions">
            <router-link
              class="cta secondary"
              :to="{ path: '/booking', query: { serviceId: item.service?.id } }"
            >
              Записаться
            </router-link>
            <button class="cta secondary" type="button" @click="emit('remove', item.id)">
              Удалить
            </button>
          </div>
        </div>
      </article>
    </div>
  </div>
</template>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 0.8rem;
}

.fav {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 0.8rem;
  align-items: center;
  padding: 0.9rem;
  border-radius: 14px;
  border: 1px solid rgba(52, 95, 32, 0.12);
  background: #fff;
}

.fav img {
  width: 64px;
  height: 64px;
  border-radius: 12px;
  object-fit: cover;
}

.actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-top: 0.4rem;
}

.empty {
  padding: 0.6rem 0;
}

.error {
  color: #8a1a1a;
  font-weight: 600;
}

.skeleton {
  min-height: 90px;
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
  .fav {
    grid-template-columns: 1fr;
  }
  .actions {
    width: 100%;
  }
  .actions .cta {
    width: 100%;
    min-height: 44px;
  }
}
</style>
