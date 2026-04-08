<script setup>
import { onMounted, ref } from "vue";
import { createMasterUser, fetchAdminUsers } from "@/api/admin";

const users = ref([]);
const loading = ref(false);
const error = ref("");
const createForm = ref({
  name: "",
  phone: "",
  email: "",
  password: "",
});

const loadUsers = async () => {
  loading.value = true;
  error.value = "";
  try {
    const data = await fetchAdminUsers();
    users.value = Array.isArray(data) ? data : [];
  } catch (err) {
    error.value = "Не удалось загрузить пользователей.";
  } finally {
    loading.value = false;
  }
};

const roleLabel = (role) => {
  if (role === "admin") return "Администратор";
  if (role === "master") return "Мастер";
  return "Клиент";
};

const createMaster = async () => {
  error.value = "";
  try {
    await createMasterUser({ ...createForm.value });
    createForm.value = { name: "", phone: "", email: "", password: "" };
    await loadUsers();
  } catch (err) {
    error.value = err.response?.data?.detail || err.response?.data?.email?.[0] || "Не удалось создать мастера.";
  }
};

onMounted(loadUsers);
</script>

<template>
  <section class="admin-page">
    <div class="section-heading">
      <p class="tag">Пользователи</p>
      <h2>Список пользователей</h2>
    </div>
    <div class="card create-form">
      <h3>Создать аккаунт мастера</h3>
      <div class="form-grid">
        <label>
          <span>Имя</span>
          <input v-model="createForm.name" type="text" />
        </label>
        <label>
          <span>Телефон</span>
          <input v-model="createForm.phone" type="text" />
        </label>
        <label>
          <span>Email</span>
          <input v-model="createForm.email" type="email" />
        </label>
        <label>
          <span>Пароль</span>
          <input v-model="createForm.password" type="password" />
        </label>
      </div>
      <button class="cta primary" type="button" @click="createMaster">Создать мастера</button>
    </div>

    <div v-if="loading" class="card">Загрузка...</div>
    <div v-else-if="error" class="card error">{{ error }}</div>
    <div v-else-if="!users.length" class="card">Пользователи не найдены.</div>
    <div v-else class="card users-list">
      <article v-for="user in users" :key="user.id" class="user-row">
        <div class="avatar">
          <img v-if="user.avatar_url" :src="user.avatar_url" :alt="user.name" />
          <span v-else>{{ user.name?.[0] || "B" }}</span>
        </div>
        <div class="meta">
          <h4>{{ user.name }}</h4>
          <p class="muted">{{ user.email }}</p>
          <p class="muted">Телефон: {{ user.phone || "—" }}</p>
          <p class="muted">Роль: {{ roleLabel(user.role) }}</p>
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

.create-form {
  display: grid;
  gap: 0.7rem;
}

.form-grid {
  display: grid;
  gap: 0.6rem;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
}

.form-grid label {
  display: grid;
  gap: 0.3rem;
}

.form-grid input {
  border: 1px solid rgba(52, 95, 32, 0.18);
  border-radius: 12px;
  padding: 0.65rem 0.8rem;
  background: #fff;
}

.users-list {
  display: grid;
  gap: 0.7rem;
}

.user-row {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 0.8rem;
  align-items: center;
  border: 1px solid rgba(52, 95, 32, 0.12);
  border-radius: 12px;
  padding: 0.75rem;
}

.avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  overflow: hidden;
  background: rgba(52, 95, 32, 0.08);
  display: grid;
  place-items: center;
  color: var(--color-avocado);
  font-weight: 700;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.meta {
  display: grid;
  gap: 0.15rem;
}

.error {
  color: #8a1a1a;
}

@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }

  .create-form .cta {
    width: 100%;
    min-height: 44px;
  }

  .user-row {
    grid-template-columns: 1fr;
    align-items: start;
  }
}
</style>
