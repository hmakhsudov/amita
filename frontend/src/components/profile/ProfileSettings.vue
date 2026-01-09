<script setup>
const props = defineProps({
  settings: {
    type: Object,
    default: () => ({
      theme: "light",
      notifications: true,
    }),
  },
});

const emit = defineEmits(["update:settings"]);

const toggle = (key, value) => {
  emit("update:settings", { ...props.settings, [key]: value });
};
</script>

<template>
  <div class="card">
    <div class="section-heading">
      <p class="tag">Настройки</p>
      <h3>Персонализация</h3>
    </div>
    <div class="grid">
      <label class="block">
        <span>Тема</span>
        <select :value="settings.theme" @change="toggle('theme', $event.target.value)">
          <option value="light">Светлая</option>
          <option value="dark">Тёмная</option>
        </select>
      </label>
      <label class="toggle block">
        <span>Уведомления</span>
        <input
          type="checkbox"
          :checked="settings.notifications"
          @change="toggle('notifications', $event.target.checked)"
        />
      </label>
    </div>
    <button class="cta secondary danger" type="button">Удалить аккаунт</button>
  </div>
</template>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 0.9rem;
  margin-bottom: 1rem;
}

.block {
  display: grid;
  gap: 0.35rem;
}

select {
  border: 1px solid rgba(52, 95, 32, 0.18);
  background: #fff;
  border-radius: 12px;
  padding: 0.6rem 0.8rem;
}

input[type="checkbox"] {
  width: 18px;
  height: 18px;
}

.danger {
  border-color: rgba(200, 40, 40, 0.4);
  color: #8a1a1a;
}
</style>
