<script setup>
import { onMounted, ref } from "vue";
import { fetchMasters } from "@/api/masters";
import {
  createService,
  deleteService,
  fetchCategories,
  fetchServices,
  updateService,
} from "@/api/services";

const services = ref([]);
const categories = ref([]);
const masters = ref([]);
const loading = ref(false);
const error = ref("");
const editingId = ref(null);
const form = ref({
  name: "",
  description: "",
  price: "",
  duration_minutes: 60,
  category_id: "",
  masters_ids: [],
});

const resetForm = () => {
  editingId.value = null;
  form.value = {
    name: "",
    description: "",
    price: "",
    duration_minutes: 60,
    category_id: "",
    masters_ids: [],
  };
};

const loadData = async () => {
  loading.value = true;
  error.value = "";
  try {
    const [servicesData, categoriesData, mastersData] = await Promise.all([
      fetchServices(),
      fetchCategories(),
      fetchMasters(),
    ]);
    services.value = Array.isArray(servicesData) ? servicesData : [];
    categories.value = Array.isArray(categoriesData) ? categoriesData : [];
    masters.value = Array.isArray(mastersData) ? mastersData : [];
  } catch (err) {
    error.value = "Не удалось загрузить услуги.";
  } finally {
    loading.value = false;
  }
};

const startEdit = (service) => {
  editingId.value = service.id;
  form.value = {
    name: service.name || "",
    description: service.description || "",
    price: service.price || "",
    duration_minutes: service.duration_minutes || 60,
    category_id: service.category?.id || "",
    masters_ids: Array.isArray(service.masters) ? service.masters.map((m) => m.id) : [],
  };
};

const toggleMaster = (masterId, checked) => {
  if (checked && !form.value.masters_ids.includes(masterId)) {
    form.value.masters_ids.push(masterId);
  } else if (!checked) {
    form.value.masters_ids = form.value.masters_ids.filter((id) => id !== masterId);
  }
};

const saveService = async () => {
  error.value = "";
  const payload = {
    name: form.value.name,
    description: form.value.description,
    price: form.value.price,
    duration_minutes: Number(form.value.duration_minutes || 60),
    category_id: form.value.category_id,
    masters_ids: form.value.masters_ids,
  };
  try {
    if (editingId.value) {
      await updateService(editingId.value, payload);
    } else {
      await createService(payload);
    }
    resetForm();
    await loadData();
  } catch (err) {
    error.value = err.response?.data?.detail || "Не удалось сохранить услугу.";
  }
};

const removeService = async (id) => {
  if (!confirm("Удалить услугу?")) return;
  error.value = "";
  try {
    await deleteService(id);
    await loadData();
  } catch (err) {
    error.value = err.response?.data?.detail || "Не удалось удалить услугу.";
  }
};

const masterNames = (service) => {
  if (!Array.isArray(service?.masters) || !service.masters.length) return "Не назначены";
  return service.masters.map((master) => master.name).join(", ");
};

onMounted(loadData);
</script>

<template>
  <section class="admin-page">
    <div class="section-heading">
      <p class="tag">Услуги</p>
      <h2>Управление услугами</h2>
    </div>

    <div class="card form-card">
      <div class="grid">
        <label>
          <span>Название услуги</span>
          <input v-model="form.name" type="text" placeholder="Введите название" />
        </label>
        <label>
          <span>Категория</span>
          <select v-model="form.category_id">
            <option disabled value="">Выберите категорию</option>
            <option v-for="category in categories" :key="category.id" :value="category.id">
              {{ category.name }}
            </option>
          </select>
        </label>
        <label>
          <span>Цена</span>
          <input v-model="form.price" type="number" min="0" step="0.01" />
        </label>
        <label>
          <span>Длительность (мин)</span>
          <input v-model="form.duration_minutes" type="number" min="10" step="5" />
        </label>
      </div>
      <label>
        <span>Описание</span>
        <textarea v-model="form.description" rows="3" placeholder="Описание услуги"></textarea>
      </label>
      <div class="masters-list">
        <p class="muted">Мастера</p>
        <label v-for="master in masters" :key="master.id" class="check">
          <input
            type="checkbox"
            :checked="form.masters_ids.includes(master.id)"
            @change="toggleMaster(master.id, $event.target.checked)"
          />
          <span>{{ master.name }}</span>
        </label>
      </div>
      <div class="actions">
        <button class="cta primary" type="button" @click="saveService">
          {{ editingId ? "Сохранить" : "Создать" }}
        </button>
        <button v-if="editingId" class="cta secondary" type="button" @click="resetForm">
          Отмена
        </button>
      </div>
    </div>

    <div v-if="loading" class="card">Загрузка...</div>
    <div v-else-if="error" class="card error">{{ error }}</div>
    <div v-else class="card list">
      <article v-for="service in services" :key="service.id" class="row">
        <div>
          <h4>{{ service.name }}</h4>
          <p class="muted">
            {{ service.category?.name || "Без категории" }} • {{ service.duration_minutes }} мин
          </p>
          <p class="muted">{{ service.description || "Без описания" }}</p>
          <p class="muted">Мастера: {{ masterNames(service) }}</p>
        </div>
        <div class="actions">
          <strong>{{ service.price }} €</strong>
          <button class="cta secondary" type="button" @click="startEdit(service)">Изменить</button>
          <button class="cta secondary" type="button" @click="removeService(service.id)">
            Удалить
          </button>
        </div>
      </article>
    </div>
  </section>
</template>

<style scoped>
.admin-page {
  display: grid;
  gap: 1rem;
}

.form-card {
  display: grid;
  gap: 0.7rem;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
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
  border-radius: 12px;
  padding: 0.7rem 0.9rem;
  background: #fff;
}

.masters-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem 0.9rem;
}

.check {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
}

.list {
  display: grid;
  gap: 0.7rem;
}

.row {
  border: 1px solid rgba(52, 95, 32, 0.12);
  border-radius: 12px;
  padding: 0.8rem;
  display: flex;
  justify-content: space-between;
  gap: 1rem;
}

.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
}

.error {
  color: #8a1a1a;
}

@media (max-width: 768px) {
  .row {
    flex-direction: column;
  }
}
</style>
