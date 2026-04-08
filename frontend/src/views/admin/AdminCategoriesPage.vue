<script setup>
import { onMounted, ref } from "vue";
import {
  createCategory,
  deleteCategory,
  fetchCategories,
  updateCategory,
} from "@/api/services";

const categories = ref([]);
const loading = ref(false);
const error = ref("");
const editingId = ref(null);
const form = ref({ name: "", description: "" });

const resetForm = () => {
  editingId.value = null;
  form.value = { name: "", description: "" };
};

const loadCategories = async () => {
  loading.value = true;
  error.value = "";
  try {
    const data = await fetchCategories();
    categories.value = Array.isArray(data) ? data : [];
  } catch (err) {
    error.value = "Не удалось загрузить категории.";
  } finally {
    loading.value = false;
  }
};

const startEdit = (category) => {
  editingId.value = category.id;
  form.value = {
    name: category.name || "",
    description: category.description || "",
  };
};

const saveCategory = async () => {
  error.value = "";
  try {
    if (editingId.value) {
      await updateCategory(editingId.value, { ...form.value });
    } else {
      await createCategory({ ...form.value });
    }
    resetForm();
    await loadCategories();
  } catch (err) {
    error.value = err.response?.data?.detail || "Не удалось сохранить категорию.";
  }
};

const removeCategory = async (id) => {
  if (!confirm("Удалить категорию?")) return;
  error.value = "";
  try {
    await deleteCategory(id);
    await loadCategories();
  } catch (err) {
    error.value = err.response?.data?.detail || "Не удалось удалить категорию.";
  }
};

onMounted(loadCategories);
</script>

<template>
  <section class="admin-page">
    <div class="section-heading">
      <p class="tag">Категории</p>
      <h2>Управление категориями</h2>
    </div>
    <div class="card form-card">
      <label>
        <span>Название</span>
        <input v-model="form.name" type="text" placeholder="Например, Уход за лицом" />
      </label>
      <label>
        <span>Описание</span>
        <textarea v-model="form.description" rows="3" placeholder="Короткое описание"></textarea>
      </label>
      <div class="actions">
        <button class="cta primary" type="button" @click="saveCategory">
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
      <article v-for="item in categories" :key="item.id" class="row">
        <div>
          <strong>{{ item.name }}</strong>
          <p class="muted">{{ item.description || "Без описания" }}</p>
        </div>
        <div class="actions">
          <button class="cta secondary" type="button" @click="startEdit(item)">Изменить</button>
          <button class="cta secondary" type="button" @click="removeCategory(item.id)">
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
  gap: 0.6rem;
}

label {
  display: grid;
  gap: 0.3rem;
}

input,
textarea {
  border: 1px solid rgba(52, 95, 32, 0.18);
  border-radius: 12px;
  padding: 0.7rem 0.9rem;
  background: #fff;
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
  gap: 0.5rem;
  flex-wrap: wrap;
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
