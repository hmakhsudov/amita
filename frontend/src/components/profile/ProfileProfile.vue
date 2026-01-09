<script setup>
import { computed, onBeforeUnmount, ref, watch } from "vue";
import { useAuthStore } from "@/stores/auth";

const props = defineProps({
  user: {
    type: Object,
    default: () => ({ name: "", email: "", phone: "", role: "" }),
  },
});

const auth = useAuthStore();
const isEditing = ref(false);
const error = ref("");
const success = ref("");
const avatarFile = ref(null);
const previewUrl = ref("");
const form = ref({
  name: "",
  phone: "",
  email: "",
});

const avatarSrc = computed(() => previewUrl.value || props.user?.avatar_url || "");
const avatarLetter = computed(() => {
  const name = props.user?.name || "";
  return name ? name.trim().charAt(0).toUpperCase() : "B";
});

const syncForm = () => {
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value);
  }
  form.value = {
    name: props.user?.name || "",
    phone: props.user?.phone || "",
    email: props.user?.email || "",
  };
  avatarFile.value = null;
  previewUrl.value = "";
};

watch(
  () => props.user,
  () => syncForm(),
  { immediate: true }
);

const toggleEdit = () => {
  isEditing.value = !isEditing.value;
  error.value = "";
  success.value = "";
  if (!isEditing.value) {
    syncForm();
  }
};

const onAvatarChange = (event) => {
  const file = event.target.files?.[0];
  if (!file) return;
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value);
  }
  avatarFile.value = file;
  previewUrl.value = URL.createObjectURL(file);
};

onBeforeUnmount(() => {
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value);
  }
});

const save = async () => {
  error.value = "";
  success.value = "";
  const payload = new FormData();
  payload.append("name", form.value.name);
  payload.append("phone", form.value.phone);
  payload.append("email", form.value.email);
  if (avatarFile.value) {
    payload.append("avatar", avatarFile.value);
  }
  try {
    await auth.updateProfile(payload);
    success.value = "Профиль обновлён.";
    isEditing.value = false;
  } catch (err) {
    error.value = auth.state.error || "Не удалось сохранить изменения.";
  }
};
</script>

<template>
  <div class="card">
    <div class="section-heading">
      <p class="tag">Профиль</p>
      <h3>Личные данные</h3>
    </div>
    <div class="profile">
      <div class="avatar">
        <div v-if="avatarSrc" class="avatar-img">
          <img :src="avatarSrc" alt="Аватар" />
        </div>
        <div v-else class="avatar-placeholder">{{ avatarLetter }}</div>
        <label v-if="isEditing" class="upload">
          <span>Загрузить фото</span>
          <input type="file" accept="image/*" @change="onAvatarChange" />
        </label>
      </div>
      <div class="grid">
        <label>
          <span>Имя</span>
          <input v-model="form.name" type="text" :readonly="!isEditing" />
        </label>
        <label>
          <span>Телефон</span>
          <input v-model="form.phone" type="text" :readonly="!isEditing" />
        </label>
        <label>
          <span>Email</span>
          <input v-model="form.email" type="email" :readonly="!isEditing" />
        </label>
      </div>
    </div>
    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="success" class="success">{{ success }}</p>
    <div class="actions">
      <button v-if="!isEditing" class="cta secondary" type="button" @click="toggleEdit">
        Редактировать
      </button>
      <button v-else class="cta primary" type="button" @click="save">Сохранить</button>
      <button v-if="isEditing" class="cta secondary" type="button" @click="toggleEdit">
        Отмена
      </button>
    </div>
  </div>
</template>

<style scoped>
.profile {
  display: grid;
  gap: 1rem;
  grid-template-columns: auto 1fr;
  align-items: start;
}

.avatar {
  display: grid;
  gap: 0.6rem;
  justify-items: center;
}

.avatar-img,
.avatar-placeholder {
  width: 96px;
  height: 96px;
  border-radius: 50%;
  overflow: hidden;
  background: rgba(52, 95, 32, 0.08);
  display: grid;
  place-items: center;
  font-weight: 700;
  color: var(--color-avocado);
}

.avatar-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.upload {
  font-size: 0.85rem;
  color: var(--color-avocado);
  cursor: pointer;
}

.upload input {
  display: none;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 0.8rem;
  margin-bottom: 1rem;
}

label {
  display: grid;
  gap: 0.3rem;
}

input,
select {
  border: 1px solid rgba(52, 95, 32, 0.18);
  background: #fff;
  border-radius: 12px;
  padding: 0.7rem 0.9rem;
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

@media (max-width: 640px) {
  .profile {
    grid-template-columns: 1fr;
  }
}
</style>
