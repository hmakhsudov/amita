import { computed, reactive } from "vue";
import api from "@/api/client";
import { clearTokens, getAccessToken, getRefreshToken, setTokens } from "@/utils/authTokens";

const state = reactive({
  accessToken: getAccessToken() || "",
  refreshToken: getRefreshToken() || "",
  user: null,
  loading: false,
  loadingMe: false,
  error: null,
});

const isAuthenticated = computed(() => !!state.accessToken);

const syncTokens = () => {
  state.accessToken = getAccessToken() || "";
  state.refreshToken = getRefreshToken() || "";
};

const fetchMe = async () => {
  state.loadingMe = true;
  state.error = null;
  try {
    const res = await api.get("/api/auth/me/");
    state.user = res.data;
  } catch (error) {
    state.user = null;
    clearTokens();
    syncTokens();
  } finally {
    state.loadingMe = false;
  }
};

const login = async ({ email, password }) => {
  state.loading = true;
  state.error = null;
  try {
    const res = await api.post("/api/auth/token/", { email, password });
    setTokens(res.data.access, res.data.refresh);
    syncTokens();
    await fetchMe();
  } catch (error) {
    state.error = error.response?.data?.detail || "Неверный email или пароль.";
    throw error;
  } finally {
    state.loading = false;
  }
};

const register = async ({ name, phone, email, password, role }) => {
  state.loading = true;
  state.error = null;
  try {
    await api.post("/api/auth/register/", {
      name,
      phone,
      email,
      password,
      role,
    });
    await login({ email, password });
  } catch (error) {
    state.error =
      error.response?.data?.email?.[0] ||
      error.response?.data?.detail ||
      "Не удалось зарегистрироваться. Проверьте данные.";
    throw error;
  } finally {
    state.loading = false;
  }
};

const updateProfile = async (formData) => {
  state.loading = true;
  state.error = null;
  try {
    const res = await api.patch("/api/auth/me/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    state.user = res.data;
  } catch (error) {
    state.error =
      error.response?.data?.detail ||
      "Не удалось обновить профиль. Проверьте данные.";
    throw error;
  } finally {
    state.loading = false;
  }
};

const logout = () => {
  clearTokens();
  syncTokens();
  state.user = null;
};

const initAuth = async () => {
  syncTokens();
  if (state.accessToken) {
    await fetchMe();
  }
};

export const useAuthStore = () => ({
  state,
  isAuthenticated,
  login,
  register,
  fetchMe,
  updateProfile,
  logout,
  initAuth,
});
