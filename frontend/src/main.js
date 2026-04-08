import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import { useAuthStore } from "./stores/auth";
import { usePlanStore } from "./stores/plan";
import { i18n } from "./i18n";
import "./style.css";

const app = createApp(App);
app.use(router);
app.use(i18n);

// Автовосстановление сессии до отрисовки хедера
const init = async () => {
  const auth = useAuthStore();
  const plan = usePlanStore();
  await auth.initAuth();
  if (auth.isAuthenticated.value && auth.state.user?.role === "client") {
    try {
      await plan.fetchPlan();
    } catch (error) {
      // ignore plan errors on init
    }
  } else {
    plan.reset();
  }
  if (auth.isAuthenticated.value && auth.state.user?.role === "admin" && !window.location.pathname.startsWith("/admin")) {
    await router.replace({ name: "admin-dashboard" });
  }
  app.mount("#app");
};

init();
