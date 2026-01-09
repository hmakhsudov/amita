<script setup>
import { ref } from "vue";
import { useReveal } from "@/composables/useReveal";
import { useAuthStore } from "@/stores/auth";
import { usePlanStore } from "@/stores/plan";
import { useRouter } from "vue-router";

const form = ref({ email: "", password: "" });
const submitted = ref(false);
const error = ref("");
const { revealRef } = useReveal();
const auth = useAuthStore();
const plan = usePlanStore();
const router = useRouter();

const submit = async () => {
  error.value = "";
  try {
    await auth.login({ email: form.value.email, password: form.value.password });
    if (auth.state.user?.role !== "admin") {
      try {
        await plan.fetchPlan();
      } catch (planError) {
        // plan errors should not block login
      }
    } else {
      plan.reset();
    }
    submitted.value = true;
    router.push("/profile");
  } catch (err) {
    error.value = auth.state.error || "Не удалось войти. Проверьте данные.";
  }
};
</script>

<template>
  <section class="page">
    <div class="card auth-card reveal" :ref="revealRef">
      <p class="tag">Вход</p>
      <h1>Вход в аккаунт</h1>
      <p class="muted">Используйте email или телефон и пароль, чтобы продолжить.</p>
      <form class="form" @submit.prevent="submit">
        <label>
          <span>Email</span>
          <input v-model="form.email" type="email" placeholder="you@example.com" required />
        </label>
        <label>
          <span>Пароль</span>
          <input v-model="form.password" type="password" placeholder="••••••••" required />
        </label>
        <p v-if="error" class="error">{{ error }}</p>
        <button class="cta primary" type="submit" :disabled="auth.state.loading">
          {{ auth.state.loading ? "Вход..." : "Войти" }}
        </button>
      </form>
      <div class="links">
        <router-link to="/register">Нет аккаунта? Зарегистрироваться</router-link>
      </div>
      <div v-if="submitted" class="after">
        <p class="muted">Авторизация успешна.</p>
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
  max-width: 420px;
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
