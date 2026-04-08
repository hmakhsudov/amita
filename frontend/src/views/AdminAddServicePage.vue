<script setup>
import { computed, onMounted, ref } from "vue";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import { fetchCategories, createService } from "@/api/services";
import { useAuthStore } from "@/stores/auth";
import { useReveal } from "@/composables/useReveal";

const router = useRouter();
const auth = useAuthStore();
const { revealRef } = useReveal();
const { t } = useI18n();

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
    error.value = t("admin.categoriesError");
  }
};

const submit = async () => {
  error.value = "";
  success.value = "";
  if (!form.value.name || !form.value.price || !form.value.category_id) {
    error.value = t("admin.requiredFields");
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
    success.value = t("admin.success");
    form.value = { name: "", description: "", price: "", category_id: "", selfAssigned: true };
  } catch (err) {
    if (err.response?.status === 401 || err.response?.status === 403) {
      error.value = t("admin.noAccess");
    } else {
      error.value = t("admin.saveError");
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
        <p class="tag">{{ t("profile.adminTag") }}</p>
        <h1>{{ t("admin.addServiceTitle") }}</h1>
        <p class="muted">{{ t("admin.addServiceHint") }}</p>
      </div>
      <form class="form" @submit.prevent="submit">
        <label>
          <span>{{ t("admin.name") }}</span>
          <input v-model="form.name" type="text" :placeholder="t('admin.namePlaceholder')" required />
        </label>
        <label>
          <span>{{ t("admin.description") }}</span>
          <textarea
            v-model="form.description"
            rows="3"
            :placeholder="t('admin.descriptionPlaceholder')"
          ></textarea>
        </label>
        <label>
          <span>{{ t("admin.price") }} (€)</span>
          <input v-model="form.price" type="number" step="0.01" placeholder="0.00" required />
        </label>
        <label>
          <span>{{ t("admin.category") }}</span>
          <select v-model="form.category_id" required>
            <option disabled value="">{{ t("admin.chooseCategory") }}</option>
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">
              {{ cat.name }}
            </option>
          </select>
        </label>
        <label class="inline">
          <input v-model="form.selfAssigned" type="checkbox" />
          <span>{{ t("admin.selfAssigned") }}</span>
        </label>
        <p v-if="error" class="error">{{ error }}</p>
        <p v-if="success" class="success">{{ success }}</p>
        <div class="actions">
          <button class="cta primary" type="submit" :disabled="loading">
            {{ loading ? t("admin.saving") : t("common.save") }}
          </button>
          <button class="cta secondary" type="button" @click="router.push('/profile')">
            {{ t("admin.cancel") }}
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

@media (max-width: 768px) {
  .page {
    padding: 1rem 0;
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
