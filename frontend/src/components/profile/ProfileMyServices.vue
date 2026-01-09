<script setup>
import { onMounted, ref } from "vue";
import { fetchCategories, fetchServices, updateService } from "@/api/services";
import { useAuthStore } from "@/stores/auth";

const auth = useAuthStore();
const services = ref([]);
const categories = ref([]);
const loading = ref(false);
const error = ref("");
const success = ref("");
const editingId = ref(null);
const form = ref({
  name: "",
  description: "",
  price: "",
  category_id: "",
  masters: [],
});

const loadData = async () => {
  loading.value = true;
  error.value = "";
  try {
    const masterId = auth.state.user?.id;
    if (!masterId) {
      services.value = [];
      return;
    }
    const [servicesData, categoriesData] = await Promise.all([
      fetchServices({ master: masterId }),
      fetchCategories(),
    ]);
    services.value = Array.isArray(servicesData) ? servicesData : [];
    categories.value = Array.isArray(categoriesData) ? categoriesData : [];
  } catch (err) {
    error.value = "Не удалось загрузить услуги.";
  } finally {
    loading.value = false;
  }
};

const startEdit = (service) => {
  editingId.value = service.id;
  form.value = {
    name: service.name,
    description: service.description || "",
    price: service.price,
    category_id: service.category?.id || "",
    masters: Array.isArray(service.masters) ? service.masters.map((m) => m.id) : [],
  };
  success.value = "";
};

const toggleSelf = (checked) => {
  const id = auth.state.user?.id;
  if (!id) return;
  if (checked && !form.value.masters.includes(id)) {
    form.value.masters.push(id);
  }
  if (!checked) {
    form.value.masters = form.value.masters.filter((masterId) => masterId !== id);
  }
};

const save = async () => {
  if (!editingId.value) return;
  error.value = "";
  success.value = "";
  try {
    const payload = {
      name: form.value.name,
      description: form.value.description,
      price: form.value.price,
      category_id: form.value.category_id,
      masters_ids: form.value.masters,
    };
    const updated = await updateService(editingId.value, payload);
    const stillAssigned = updated.masters?.some(
      (master) => master.id === auth.state.user?.id
    );
    if (!stillAssigned) {
      services.value = services.value.filter((service) => service.id !== updated.id);
    } else {
      services.value = services.value.map((service) =>
        service.id === updated.id ? updated : service
      );
    }
    success.value = "Изменения сохранены.";
    editingId.value = null;
  } catch (err) {
    error.value = err.response?.data?.detail || "Не удалось сохранить изменения.";
  }
};

const cancelEdit = () => {
  editingId.value = null;
};

onMounted(loadData);
</script>

<template>
  <div class="card">
    <div class="section-heading">
      <p class="tag">Мои услуги</p>
      <h3>Управление услугами</h3>
    </div>

    <div v-if="loading" class="grid">
      <div v-for="n in 2" :key="n" class="service skeleton"></div>
    </div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="!services.length" class="empty muted">
      Пока у вас нет услуг. Добавьте услугу в админ‑форме.
    </div>

    <div v-else class="grid">
      <article v-for="service in services" :key="service.id" class="service">
        <div v-if="editingId !== service.id">
          <h4>{{ service.name }}</h4>
          <p class="muted">{{ service.category?.name || "Без категории" }}</p>
          <p class="muted">{{ service.description || "Описание отсутствует." }}</p>
          <p class="muted">Цена: {{ service.price }} ₽</p>
          <button class="cta secondary" type="button" @click="startEdit(service)">
            Редактировать
          </button>
        </div>

        <div v-else class="form">
          <label>
            <span>Название</span>
            <input v-model="form.name" type="text" />
          </label>
          <label>
            <span>Описание</span>
            <textarea v-model="form.description" rows="3"></textarea>
          </label>
          <label>
            <span>Цена</span>
            <input v-model="form.price" type="number" step="0.01" />
          </label>
          <label>
            <span>Категория</span>
            <select v-model="form.category_id">
              <option disabled value="">Выберите категорию</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                {{ cat.name }}
              </option>
            </select>
          </label>
          <label class="inline">
            <input
              type="checkbox"
              :checked="form.masters.includes(auth.state.user?.id)"
              @change="toggleSelf($event.target.checked)"
            />
            <span>Я оказываю эту услугу</span>
          </label>
          <div class="actions">
            <button class="cta primary" type="button" @click="save">Сохранить</button>
            <button class="cta secondary" type="button" @click="cancelEdit">Отмена</button>
          </div>
        </div>
      </article>
    </div>
    <p v-if="success" class="success">{{ success }}</p>
  </div>
</template>

<style scoped>
.grid {
  display: grid;
  gap: 0.8rem;
}

.service {
  padding: 0.9rem;
  border-radius: 14px;
  border: 1px solid rgba(52, 95, 32, 0.12);
  background: #fff;
  display: grid;
  gap: 0.6rem;
}

.form {
  display: grid;
  gap: 0.6rem;
}

label {
  display: grid;
  gap: 0.3rem;
}

input,
textarea,
select {
  border: 1px solid rgba(52, 95, 32, 0.18);
  background: #fff;
  border-radius: 12px;
  padding: 0.7rem 0.9rem;
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
}

.error {
  color: #8a1a1a;
  font-weight: 600;
}

.success {
  color: #345f20;
  font-weight: 600;
  margin-top: 0.6rem;
}

.empty {
  padding: 0.6rem 0;
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
</style>
