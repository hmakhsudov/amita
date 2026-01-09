import { nextTick } from "vue";
import { createRouter, createWebHistory } from "vue-router";

import HomeView from "@/views/HomeView.vue";
import ServicesView from "@/views/ServicesView.vue";
import AboutView from "@/views/AboutView.vue";
import BookingPage from "@/views/BookingPage.vue";
import ProfilePage from "@/views/ProfilePage.vue";
import LoginPage from "@/views/LoginPage.vue";
import RegisterPage from "@/views/RegisterPage.vue";
import AdminAddServicePage from "@/views/AdminAddServicePage.vue";
import PlanPage from "@/views/PlanPage.vue";
import AssistantPage from "@/views/AssistantPage.vue";
import MastersPage from "@/views/MastersPage.vue";
import { useAuthStore } from "@/stores/auth";

const router = createRouter({
    history: createWebHistory(),
    scrollBehavior() {
        return { top: 0 };
    },
    routes: [
        { path: "/", name: "home", component: HomeView },
        { path: "/services", name: "services", component: ServicesView },
        { path: "/assistant", name: "assistant", component: AssistantPage },
        { path: "/masters", name: "masters", component: MastersPage },
        { path: "/booking", name: "booking", component: BookingPage, meta: { role: "client" } },
        { path: "/plan", name: "plan", component: PlanPage, meta: { role: "client" } },
        { path: "/profile", name: "profile", component: ProfilePage, meta: { requiresAuth: true } },
        {
            path: "/admin/services/new",
            name: "admin-service-new",
            component: AdminAddServicePage,
            meta: { requiresAuth: true, role: "admin" },
        },
        { path: "/login", name: "login", component: LoginPage },
        { path: "/register", name: "register", component: RegisterPage },
        { path: "/about", name: "about", component: AboutView },
    ],
});

router.beforeEach((to) => {
    const auth = useAuthStore();
    const isAuthed = auth.isAuthenticated.value;
    const role = auth.state.user?.role || "";
    if (to.meta?.requiresAuth && !isAuthed) {
        return { name: "login" };
    }
    if (to.meta?.role && role && to.meta.role !== role) {
        return { name: "profile" };
    }
    if (to.meta?.role === "admin" && !isAuthed) {
        return { name: "login" };
    }
    if ((to.name === "login" || to.name === "register") && isAuthed) {
        return { name: "profile" };
    }
    return true;
});

router.afterEach(async () => {
    await nextTick();
    window.dispatchEvent(new Event("reveal:refresh"));
});

export default router;
