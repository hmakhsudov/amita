<script setup>
import { computed, onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { fetchCategories, createService } from "@/api/services";
import { useAuthStore } from "@/stores/auth";
import { useReveal } from "@/composables/useReveal";

const router = useRouter();
const auth = useAuthStore();
const { revealRef } = useReveal();

const form = ref({
  name: "",
  description: "",
  price: "",
  category_id: "",
  selfAssigned: true,
});
const categories = ref([]);
const loading = ref(false);
const error = ref("");
const success = ref("");

const isAdmin = computed(() => auth.state.user?.role === "admin");

const loadCategories = async () => {
  try {
    const data = await fetchCategories();
    categories.value = data;
  } catch (err) {
    error.value = "Не удалось загрузить категории.";
  }
};

const submit = async () => {
  error.value = "";
  success.value = "";
  if (!form.value.name || !form.value.price || !form.value.category_id) {
    error.value = "Заполните обязательные поля.";
    return;
  }
  loading.value = true;
  try {
    await createService({
      name: form.value.name,
      description: form.value.description,
      price: form.value.price,
      category_id: form.value.category_id,
      masters_ids: form.value.selfAssigned ? [auth.state.user?.id].filter(Boolean) : [],
    });
    success.value = "Услуга добавлена.";
    form.value = { name: "", description: "", price: "", category_id: "", selfAssigned: true };
  } catch (err) {
    if (err.response?.status === 401 || err.response?.status === 403) {
      error.value = "Недостаточно прав для добавления услуги.";
    } else {
      error.value = "Ошибка сохранения. Проверьте данные.";
    }
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  if (!isAdmin.value) {
    router.push("/profile");
    return;
  }
  await loadCategories();
});
</script>

<template>
  <section class="page">
    <div class="card reveal" :ref="revealRef">
      <div class="section-heading">
        <p class="tag">Админ</p>
        <h1>Добавление услуги</h1>
        <p class="muted">Только для администраторов. Данные отправляются в API.</p>
      </div>
      <form class="form" @submit.prevent="submit">
        <label>
          <span>Название услуги</span>
          <input v-model="form.name" type="text" placeholder="Например, Детокс-уход" required />
        </label>
        <label>
          <span>Описание</span>
          <textarea
            v-model="form.description"
            rows="3"
            placeholder="Краткое описание услуги"
          ></textarea>
        </label>
        <label>
          <span>Цена (₽)</span>
          <input v-model="form.price" type="number" step="0.01" placeholder="0.00" required />
        </label>
        <label>
          <span>Категория</span>
          <select v-model="form.category_id" required>
            <option disabled value="">Выберите категорию</option>
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">
              {{ cat.name }}
            </option>
          </select>
        </label>
        <label class="inline">
          <input v-model="form.selfAssigned" type="checkbox" />
          <span>Я оказываю эту услугу</span>
        </label>
        <p v-if="error" class="error">{{ error }}</p>
        <p v-if="success" class="success">{{ success }}</p>
        <div class="actions">
          <button class="cta primary" type="submit" :disabled="loading">
            {{ loading ? "Сохранение..." : "Сохранить" }}
          </button>
          <button class="cta secondary" type="button" @click="router.push('/profile')">
            Отмена
          </button>
        </div>
      </form>
    </div>
  </section>
</template>

<style scoped>
.page {
  display: grid;
  place-items: center;
  padding: 2rem 0;
}

.form {
  display: grid;
  gap: 0.75rem;
  margin-top: 1rem;
}

label {
  display: grid;
  gap: 0.35rem;
}

input,
textarea,
select {
  border: 1px solid rgba(52, 95, 32, 0.18);
  background: #fff;
  border-radius: 12px;
  padding: 0.75rem 0.9rem;
}

.inline {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.actions {
  display: flex;
  gap: 0.6rem;
  flex-wrap: wrap;
  margin-top: 0.5rem;
}

.error {
  color: #8a1a1a;
  font-weight: 600;
}

.success {
  color: #345f20;
  font-weight: 600;
}
</style>
