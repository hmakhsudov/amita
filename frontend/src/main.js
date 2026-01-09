import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import { useAuthStore } from "./stores/auth";
import { usePlanStore } from "./stores/plan";
import "./style.css";

const app = createApp(App);
app.use(router);

// Автовосстановление сессии до отрисовки хедера
const init = async () => {
  const auth = useAuthStore();
  const plan = usePlanStore();
  await auth.initAuth();
  if (auth.isAuthenticated.value && auth.state.user?.role !== "admin") {
    try {
      await plan.fetchPlan();
    } catch (error) {
      // ignore plan errors on init
    }
  } else {
    plan.reset();
  }
  app.mount("#app");
};

init();
