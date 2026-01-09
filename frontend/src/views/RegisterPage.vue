<script setup>
import { ref } from "vue";
import { useReveal } from "@/composables/useReveal";
import { useAuthStore } from "@/stores/auth";
import { usePlanStore } from "@/stores/plan";
import { useRouter } from "vue-router";

const form = ref({
  name: "",
  phone: "",
  email: "",
  password: "",
  confirm: "",
  role: "client",
});
const submitted = ref(false);
const error = ref("");
const { revealRef } = useReveal();
const auth = useAuthStore();
const plan = usePlanStore();
const router = useRouter();

const submit = async () => {
  error.value = "";
  if (form.value.password.length < 8) {
    error.value = "Пароль должен быть не короче 8 символов.";
    return;
  }
  if (form.value.password !== form.value.confirm) {
    error.value = "Пароли не совпадают.";
    return;
  }
  try {
    await auth.register({
      name: form.value.name,
      phone: form.value.phone,
      email: form.value.email,
      password: form.value.password,
      role: form.value.role,
    });
    if (auth.state.user?.role !== "admin") {
      try {
        await plan.fetchPlan();
      } catch (planError) {
        // plan errors should not block registration
      }
    } else {
      plan.reset();
    }
    submitted.value = true;
    router.push("/profile");
  } catch (err) {
    error.value = auth.state.error || "Не удалось зарегистрироваться.";
  }
};
</script>

<template>
  <section class="page">
    <div class="card auth-card reveal" :ref="revealRef">
      <p class="tag">Регистрация</p>
      <h1>Создайте аккаунт</h1>
      <form class="form" @submit.prevent="submit">
        <label>
          <span>Имя</span>
          <input v-model="form.name" type="text" placeholder="Ваше имя" required />
        </label>
        <label>
          <span>Телефон</span>
          <input v-model="form.phone" type="tel" placeholder="+43 (___) ___-__-__" required />
        </label>
        <label>
          <span>Email</span>
          <input v-model="form.email" type="email" placeholder="you@example.com" required />
        </label>
        <label class="full">
          <span>Роль</span>
          <div class="roles">
            <label class="radio">
              <input v-model="form.role" type="radio" value="client" />
              <span>Клиент</span>
            </label>
            <label class="radio">
              <input v-model="form.role" type="radio" value="admin" />
              <span>Администратор</span>
            </label>
          </div>
        </label>
        <label>
          <span>Пароль</span>
          <input v-model="form.password" type="password" placeholder="••••••••" required />
        </label>
        <label>
          <span>Подтверждение пароля</span>
          <input v-model="form.confirm" type="password" placeholder="••••••••" required />
        </label>
        <p v-if="error" class="error">{{ error }}</p>
        <button class="cta primary" type="submit" :disabled="auth.state.loading">
          {{ auth.state.loading ? "Создание..." : "Создать аккаунт" }}
        </button>
      </form>
      <div class="links">
        <router-link to="/login">Уже есть аккаунт? Войти</router-link>
      </div>
      <div v-if="submitted" class="after">
        <p class="muted">Регистрация выполнена. Добро пожаловать!</p>
        <router-link class="cta secondary" to="/profile">Перейти в личный кабинет</router-link>
      </div>
    </div>
  </section>
</template>

<style scoped>
.page {
  display: grid;
  place-items: center;
  padding: 2rem 0;
}

.auth-card {
  max-width: 520px;
  width: 100%;
  background: linear-gradient(135deg, #ffffff, #f8f4e8);
}

.form {
  display: grid;
  gap: 0.75rem;
  margin: 1rem 0;
}

label {
  display: grid;
  gap: 0.35rem;
}

input {
  border: 1px solid rgba(52, 95, 32, 0.18);
  background: #fff;
  border-radius: 12px;
  padding: 0.75rem 0.9rem;
}

.roles {
  display: flex;
  gap: 0.8rem;
  flex-wrap: wrap;
}

.radio {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  border: 1px solid rgba(52, 95, 32, 0.18);
  border-radius: 12px;
  padding: 0.5rem 0.8rem;
  background: #fff;
}

.full {
  grid-column: 1 / -1;
}

.error {
  color: #8a1a1a;
  font-weight: 600;
}

.links {
  margin-top: 0.6rem;
}

.after {
  margin-top: 1rem;
  display: grid;
  gap: 0.5rem;
}
</style>
