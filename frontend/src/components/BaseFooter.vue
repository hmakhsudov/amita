<script setup>
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import fruitPattern from "@/assets/fruit-pattern.svg";
import ruFlag from "@/assets/flags/ru.svg";
import deFlag from "@/assets/flags/de.svg";

const { locale, t } = useI18n();
const current = computed(() => locale.value);

const switchLang = (next) => {
  locale.value = next;
  localStorage.setItem("lang", next);
};
</script>

<template>
  <footer class="footer">
    <div class="texture">
      <img :src="fruitPattern" alt="" aria-hidden="true" />
    </div>
    <div class="footer-inner">
      <div>
        <h4>{{ t("footer.title") }}</h4>
        <p class="muted">{{ t("footer.subtitle") }}</p>
      </div>
      <div class="contacts">
        <p><strong>{{ t("footer.contacts") }}</strong></p>
        <p>+436767460828</p>
        <p>bizu2305@gmail.com</p>
      </div>
      <div class="social">
        <p><strong>{{ t("footer.nearby") }}</strong></p>
        <p>{{ t("footer.social") }}</p>
      </div>
      <div class="lang-switch">
        <p><strong>{{ t("footer.language") }}</strong></p>
        <div class="flags">
          <button
            type="button"
            class="flag"
            :class="{ active: current === 'ru' }"
            aria-label="Русский"
            @click="switchLang('ru')"
          >
            <img :src="ruFlag" alt="Русский" />
          </button>
          <button
            type="button"
            class="flag"
            :class="{ active: current === 'de' }"
            aria-label="Deutsch"
            @click="switchLang('de')"
          >
            <img :src="deFlag" alt="Deutsch" />
          </button>
        </div>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  position: relative;
  overflow: hidden;
  border-top: 1px solid rgba(52, 95, 32, 0.12);
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(8px);
}

.texture {
  position: absolute;
  inset: 0;
  opacity: 0.08;
  pointer-events: none;
}

.texture img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.footer-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1.5rem 1.25rem 2rem;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1rem;
  align-items: start;
}

.footer h4 {
  font-family: "Playfair Display", "Times New Roman", serif;
  margin-bottom: 0.35rem;
}

.footer p {
  margin: 0.2rem 0;
  color: rgba(47, 54, 47, 0.85);
}

.lang-switch {
  display: grid;
  gap: 0.5rem;
}

.flags {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.flag {
  border: 1px solid rgba(52, 95, 32, 0.18);
  background: #fff;
  border-radius: 10px;
  padding: 0.25rem;
  width: 44px;
  height: 32px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  opacity: 0.6;
  cursor: pointer;
  transition: opacity 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}

.flag.active {
  opacity: 1;
  border-color: var(--color-matcha);
  box-shadow: 0 10px 18px rgba(52, 95, 32, 0.12);
}

.flag img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 6px;
}

@media (max-width: 768px) {
  .footer-inner {
    padding: 1.2rem 1rem 1.5rem;
    grid-template-columns: 1fr;
    gap: 0.8rem;
  }

  .flags {
    gap: 0.4rem;
  }

  .flag {
    width: 40px;
    height: 30px;
  }
}
</style>
