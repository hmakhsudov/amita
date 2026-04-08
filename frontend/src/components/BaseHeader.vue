<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { usePlanStore } from "@/stores/plan";
import { useChatStore } from "@/stores/chat";

const isOpen = ref(false);
const isScrolled = ref(false);
const route = useRoute();
const router = useRouter();
const auth = useAuthStore();
const plan = usePlanStore();
const chat = useChatStore();
const { t } = useI18n();
const isAuthorized = computed(() => auth.isAuthenticated.value);
const isReady = computed(() => !auth.state.loadingMe);
const isStaffAdmin = computed(() => auth.state.user?.role === "admin");
const isMaster = computed(() => auth.state.user?.role === "master");
const isClient = computed(() => auth.state.user?.role === "client");
const planCount = computed(() =>
  isAuthorized.value && isClient.value ? plan.count.value : 0
);
const unreadTotal = computed(() => chat.state.unreadTotal);
const unreadTimer = ref(null);

const baseLinks = [
  { key: "nav.home", path: "/" },
  { key: "nav.services", path: "/services" },
  { key: "nav.masters", path: "/masters" },
  { key: "nav.assistant", path: "/assistant" },
  { key: "nav.plan", path: "/plan" },
  { key: "nav.about", path: "/about" },
  { key: "nav.booking", path: "/booking" },
];

const navLinks = computed(() => {
  if (isStaffAdmin.value) {
    return [{ path: "/admin/dashboard", label: "Админ-панель" }];
  }
  if (isMaster.value) {
    return baseLinks.filter((link) => !["/plan", "/booking"].includes(link.path));
  }
  return [...baseLinks];
});

const closeMenu = () => {
  isOpen.value = false;
};

const handleScroll = () => {
  isScrolled.value = window.scrollY > 12;
};

onMounted(() => {
  handleScroll();
  window.addEventListener("scroll", handleScroll, { passive: true });
  if (isAuthorized.value) {
    chat.fetchUnreadTotal();
    unreadTimer.value = setInterval(() => {
      chat.fetchUnreadTotal();
    }, 25000);
  }
});

onBeforeUnmount(() => {
  window.removeEventListener("scroll", handleScroll);
  if (unreadTimer.value) {
    clearInterval(unreadTimer.value);
  }
});

watch(
  () => route.fullPath,
  () => {
    isOpen.value = false;
  }
);

watch(
  () => isAuthorized.value,
  (next) => {
    if (!next) {
      chat.state.unreadTotal = 0;
      if (unreadTimer.value) {
        clearInterval(unreadTimer.value);
        unreadTimer.value = null;
      }
      return;
    }
    chat.fetchUnreadTotal();
    if (!unreadTimer.value) {
      unreadTimer.value = setInterval(() => {
        chat.fetchUnreadTotal();
      }, 25000);
    }
  }
);

const closeAndLogout = () => {
  auth.logout();
  plan.reset();
  router.push("/");
  isOpen.value = false;
};
</script>

<template>
  <header class="header" :class="{ scrolled: isScrolled }">
    <div class="inner">
      <router-link class="logo" to="/" @click="closeMenu">
        <img src="@/assets/logo-bizu.svg" :alt="t('common.logoAlt')" />
        <div class="branding">
          <span class="brand">BIZU</span>
        </div>
      </router-link>

      <nav class="desktop-nav">
        <router-link
          v-for="link in navLinks"
          :key="link.path"
          :to="link.path"
          class="nav-link"
          :class="{ active: route.path === link.path }"
        >
          {{ link.label || t(link.key) }}
          <span v-if="link.path === '/plan' && planCount" class="badge">
            {{ planCount }}
          </span>
        </router-link>
      </nav>

      <div class="actions desktop-actions">
        <template v-if="!isReady">
          <span class="loading">...</span>
        </template>
        <template v-else-if="isAuthorized">
          <router-link class="cta secondary" :to="isStaffAdmin ? '/admin/dashboard' : '/profile'">
            {{ isStaffAdmin ? "Админ-панель" : t("nav.profile") }}
            <span v-if="unreadTotal" class="badge">{{ unreadTotal }}</span>
          </router-link>
          <button class="cta primary" type="button" @click="closeAndLogout">
            {{ t("nav.logout") }}
          </button>
        </template>
        <template v-else>
          <router-link class="cta secondary" to="/login">{{ t("nav.login") }}</router-link>
          <router-link class="cta primary" to="/register">{{ t("nav.register") }}</router-link>
        </template>
      </div>

      <button
        class="menu-toggle"
        type="button"
        :aria-label="t('common.menu')"
        @click="isOpen = !isOpen"
      >
        <span :class="{ open: isOpen }"></span>
        <span :class="{ open: isOpen }"></span>
      </button>
    </div>

    <transition name="slide">
      <div v-if="isOpen" class="mobile-menu">
        <router-link
          v-for="link in navLinks"
          :key="link.path"
          :to="link.path"
          class="mobile-link"
          :class="{ active: route.path === link.path }"
          @click="closeMenu"
        >
          {{ link.label || t(link.key) }}
          <span v-if="link.path === '/plan' && planCount" class="badge">
            {{ planCount }}
          </span>
        </router-link>
        <div class="mobile-actions">
          <template v-if="!isReady">
            <span class="loading">...</span>
          </template>
          <template v-else-if="isAuthorized">
            <router-link
              class="cta secondary"
              :to="isStaffAdmin ? '/admin/dashboard' : '/profile'"
              @click="closeMenu"
            >
              {{ isStaffAdmin ? "Админ-панель" : t("nav.profile") }}
              <span v-if="unreadTotal" class="badge">{{ unreadTotal }}</span>
            </router-link>
            <button class="cta primary" type="button" @click="closeAndLogout">
              {{ t("nav.logout") }}
            </button>
          </template>
          <template v-else>
            <router-link class="cta secondary" to="/login" @click="closeMenu">
              {{ t("nav.login") }}
            </router-link>
            <router-link class="cta primary" to="/register" @click="closeMenu">
              {{ t("nav.register") }}
            </router-link>
          </template>
        </div>
      </div>
    </transition>
  </header>
</template>

<style scoped>
.header {
  position: sticky;
  top: 0;
  z-index: 50;
  backdrop-filter: blur(12px);
  background: rgba(244, 238, 224, 0.92);
  border-bottom: 1px solid rgba(52, 95, 32, 0.08);
  transition: padding 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}

.header.scrolled {
  box-shadow: 0 10px 28px rgba(52, 95, 32, 0.08);
  border-color: rgba(52, 95, 32, 0.12);
}

.inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1.25rem;
}

.logo {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  text-decoration: none;
  color: var(--color-avocado);
}

.logo img {
  width: 42px;
  height: 42px;
}

.branding {
  display: flex;
  flex-direction: column;
  line-height: 1.1;
}

.brand {
  font-family: "Oswald", "Inter", sans-serif;
  letter-spacing: 2px;
  font-weight: 700;
}

.sub {
  font-size: 0.82rem;
  color: rgba(52, 95, 32, 0.8);
}

.desktop-nav {
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

.nav-link {
  font-weight: 600;
  color: var(--color-avocado);
  text-decoration: none;
  padding-bottom: 4px;
  border-bottom: 2px solid transparent;
  transition: color 0.2s ease, border-color 0.2s ease;
}

.nav-link:hover,
.nav-link.active {
  color: #2c4c22;
  border-color: var(--color-matcha);
}

.actions {
  display: flex;
  gap: 0.4rem;
  align-items: center;
}

.loading {
  color: rgba(52, 95, 32, 0.65);
  font-weight: 600;
}

.badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 20px;
  height: 20px;
  padding: 0 6px;
  margin-left: 6px;
  border-radius: 999px;
  background: var(--color-matcha);
  color: #1f260f;
  font-size: 0.75rem;
  font-weight: 700;
}

.menu-toggle {
  display: none;
  flex-direction: column;
  gap: 4px;
  background: var(--color-avocado);
  border: none;
  padding: 10px 12px;
  border-radius: 12px;
  cursor: pointer;
}

.menu-toggle span {
  display: block;
  width: 18px;
  height: 2px;
  background: var(--color-eggshell);
  transition: transform 0.2s ease, opacity 0.2s ease;
}

.menu-toggle span.open:nth-child(1) {
  transform: translateY(3px) rotate(45deg);
}
.menu-toggle span.open:nth-child(2) {
  transform: translateY(-3px) rotate(-45deg);
}

.mobile-menu {
  display: none;
  flex-direction: column;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem 1rem;
  background: rgba(244, 238, 224, 0.96);
  border-bottom: 1px solid rgba(52, 95, 32, 0.1);
}

.mobile-link {
  color: var(--color-avocado);
  font-weight: 700;
  text-decoration: none;
  padding: 0.5rem 0;
  border-bottom: 1px dashed rgba(52, 95, 32, 0.14);
}

.mobile-link.active {
  color: #2c4c22;
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.2s ease;
}
.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}

@media (max-width: 768px) {
  .desktop-nav {
    display: none;
  }
  .menu-toggle {
    display: inline-flex;
  }
  .mobile-menu {
    display: flex;
  }
  .desktop-actions {
    display: none;
  }
  .mobile-actions {
    display: grid;
    gap: 0.4rem;
    margin-top: 0.6rem;
  }
}
</style>
