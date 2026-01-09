<script setup>
import { onMounted, ref } from "vue";
import { useReveal } from "@/composables/useReveal";

// TODO: заменить на фото из брендбука (девушки с напитками, стр. 1)
import heroImage from "@/assets/hero-main.jpg";
import fruitPattern from "@/assets/fruit-pattern.svg";

const textRef = ref(null);
const { revealRef } = useReveal();

onMounted(() => {
  // Connect the text block to the reveal animation
  if (textRef.value) revealRef(textRef.value);
});
</script>

<template>
  <section class="hero">
    <div class="hero-bg">
      <img :src="heroImage" alt="Герой — девушки с напитками" />
      <div class="overlay"></div>
      <div class="grain"></div>
      <img class="pattern" :src="fruitPattern" alt="" aria-hidden="true" />
    </div>
    <div class="hero-content reveal" ref="textRef">
      <p class="pill">Натуральная красота и здоровый ритм</p>
      <h1>BIZU — салон красоты и здорового образа жизни</h1>
      <p class="lead">
        Салон красоты и здорового образа жизни с мягкими avocado/matcha акцентами. Технологии
        рекомендаций + заботливые мастера.
      </p>
      <div class="actions">
        <router-link class="cta primary" to="/booking">Записаться онлайн</router-link>
      </div>
    </div>
  </section>
</template>

<style scoped>
.hero {
  position: relative;
  min-height: 72vh;
  border-radius: 24px;
  overflow: hidden;
  margin-top: 1.5rem;
  background: var(--eggshell);
  background: var(--color-eggshell);
}

.hero-bg {
  position: absolute;
  inset: 0;
}

.hero-bg img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: saturate(0.92);
}

.overlay {
  position: absolute;
  inset: 0;
  background: radial-gradient(85% 80% at 20% 20%, rgba(244, 238, 224, 0.6), rgba(0, 0, 0, 0.35)),
    linear-gradient(180deg, rgba(0, 0, 0, 0.35), rgba(0, 0, 0, 0.05));
}

.grain {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.15), transparent);
}

.pattern {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 380px;
  opacity: 0.12;
}

.hero-content {
  position: relative;
  max-width: 520px;
  padding: 3rem 2.5rem;
  color: var(--color-eggshell);
}

.lead {
  color: #f7f2e6;
  max-width: 460px;
}

.actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin-top: 1.2rem;
}

.ghost {
  border-style: dashed;
}

@media (max-width: 768px) {
  .hero {
    min-height: 65vh;
  }
  .hero-content {
    padding: 2.4rem 1.4rem;
    max-width: 100%;
  }
  .pattern {
    width: 240px;
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
