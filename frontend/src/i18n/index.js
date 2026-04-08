import { createI18n } from "vue-i18n";

import ru from "./locales/ru.json";
import de from "./locales/de.json";

const saved = localStorage.getItem("lang") || "ru";

export const i18n = createI18n({
  legacy: false,
  globalInjection: true,
  locale: saved,
  fallbackLocale: "ru",
  messages: { ru, de },
});

export const setLocale = (locale) => {
  i18n.global.locale.value = locale;
  localStorage.setItem("lang", locale);
};
