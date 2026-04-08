<script setup>
import { ref } from "vue";
import { useI18n } from "vue-i18n";
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
});
const submitted = ref(false);
const error = ref("");
const { revealRef } = useReveal();
const auth = useAuthStore();
const plan = usePlanStore();
const router = useRouter();
const { t } = useI18n();

const submit = async () => {
  error.value = "";
  if (form.value.password.length < 8) {
    error.value = t("auth.passwordShort");
    return;
  }
  if (form.value.password !== form.value.confirm) {
    error.value = t("auth.passwordMismatch");
    return;
  }
  try {
    await auth.register({
      name: form.value.name,
      phone: form.value.phone,
      email: form.value.email,
      password: form.value.password,
      role: "client",
    });
    if (auth.state.user?.role === "client") {
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
    error.value = auth.state.error || t("auth.registerError");
  }
};
</script>

<template>
  <section class="page">
    <div class="card auth-card reveal" :ref="revealRef">
      <p class="tag">{{ t("auth.registerTitle") }}</p>
      <h1>{{ t("auth.registerTitle") }}</h1>
      <form class="form" @submit.prevent="submit">
        <label>
          <span>{{ t("auth.name") }}</span>
          <input v-model="form.name" type="text" :placeholder="t('booking.namePlaceholder')" required />
        </label>
        <label>
          <span>{{ t("auth.phone") }}</span>
          <input v-model="form.phone" type="tel" :placeholder="t('booking.phonePlaceholder')" required />
        </label>
        <label>
          <span>{{ t("auth.email") }}</span>
          <input v-model="form.email" type="email" :placeholder="t('auth.emailPlaceholder')" required />
        </label>
        <label>
          <span>{{ t("auth.password") }}</span>
          <input v-model="form.password" type="password" :placeholder="t('auth.passwordPlaceholder')" required />
        </label>
        <label>
          <span>{{ t("auth.passwordConfirm") }}</span>
          <input v-model="form.confirm" type="password" :placeholder="t('auth.passwordPlaceholder')" required />
        </label>
        <p v-if="error" class="error">{{ error }}</p>
        <button class="cta primary" type="submit" :disabled="auth.state.loading">
          {{ auth.state.loading ? t("auth.loadingRegister") : t("auth.registerBtn") }}
        </button>
      </form>
      <div class="links">
        <router-link to="/login">{{ t("auth.haveAccount") }}</router-link>
      </div>
      <div v-if="submitted" class="after">
        <p class="muted">{{ t("auth.registerSuccess") }}</p>
        <router-link class="cta secondary" to="/profile">{{ t("auth.toProfile") }}</router-link>
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

@media (max-width: 768px) {
  .page {
    padding: 1rem 0;
  }

  .auth-card {
    max-width: 100%;
  }

  .form .cta {
    width: 100%;
    min-height: 44px;
  }

  .after .cta {
    width: 100%;
    min-height: 44px;
  }
}
</style>
