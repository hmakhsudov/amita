<script setup>
const props = defineProps({
  tabs: { type: Array, default: () => [] },
  active: { type: String, default: "" },
});

const emit = defineEmits(["change"]);
</script>

<template>
  <aside class="sidebar card">
    <nav class="menu">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        class="item"
        :class="{ active: tab.key === active }"
        type="button"
        @click="emit('change', tab.key)"
      >
        {{ tab.label }}
      </button>
    </nav>
  </aside>
</template>

<style scoped>
.sidebar {
  position: sticky;
  top: 80px;
  padding: 1rem;
}

.menu {
  display: grid;
  gap: 0.5rem;
}

.item {
  text-align: left;
  border: 1px solid rgba(52, 95, 32, 0.18);
  background: #fff;
  padding: 0.7rem 0.9rem;
  border-radius: 12px;
  color: var(--text-body);
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
}

.item:hover {
  box-shadow: 0 12px 24px rgba(52, 95, 32, 0.12);
}

.item.active {
  border-color: var(--color-matcha);
  box-shadow: 0 14px 28px rgba(52, 95, 32, 0.14);
}

@media (max-width: 768px) {
  .sidebar {
    position: static;
    top: auto;
    padding: 0.8rem;
  }
  .menu {
    display: flex;
    gap: 0.6rem;
    overflow-x: auto;
    padding-bottom: 0.3rem;
  }
  .item {
    white-space: nowrap;
    flex: 0 0 auto;
  }
}
</style>
