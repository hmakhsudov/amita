<script setup>
import { RouterView } from "vue-router";
import BaseFooter from "@/components/BaseFooter.vue";
import BaseHeader from "@/components/BaseHeader.vue";
</script>

<template>
  <div class="app-shell">
    <div class="bg-accent">
      <img src="@/assets/hero-bg-pattern.svg" alt="" aria-hidden="true" />
    </div>
    <BaseHeader />
    <main class="page">
      <RouterView v-slot="{ Component, route }">
        <Transition name="page" mode="out-in">
          <component :is="Component" :key="route.fullPath" />
        </Transition>
      </RouterView>
    </main>
    <BaseFooter />
  </div>
</template>

<style scoped>
.app-shell {
  min-height: 100vh;
  background: radial-gradient(120% 120% at 18% 20%, rgba(232, 234, 108, 0.1), transparent),
    var(--color-eggshell);
  color: var(--text-body);
  position: relative;
  overflow-x: hidden;
}

.bg-accent {
  position: absolute;
  inset: 0;
  pointer-events: none;
  opacity: 0.07;
  display: flex;
  justify-content: flex-end;
}

.bg-accent img {
  width: 540px;
  transform: translate(30%, -6%);
  mix-blend-mode: multiply;
}

.page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1.25rem 1.25rem 4rem;
}

.page-enter-active,
.page-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}
.page-enter-from,
.page-leave-to {
  opacity: 0;
  transform: translateY(6px);
}

@media (max-width: 768px) {
  .bg-accent img {
    width: 300px;
    transform: translate(20%, -10%);
  }
  .page {
    padding: 1rem 1rem 3rem;
  }
}
</style>
