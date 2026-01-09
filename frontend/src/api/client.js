import axios from "axios";
import { clearTokens, getAccessToken, getRefreshToken, setTokens } from "@/utils/authTokens";

const baseURL =
  import.meta.env.VITE_API_BASE_URL ||
  import.meta.env.VITE_API_URL ||
  "/api";

const api = axios.create({
  baseURL,
});

api.interceptors.request.use((config) => {
  const token = getAccessToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config;
    if (original?.url?.includes("/api/auth/token/refresh/")) {
      clearTokens();
      window.location.href = "/login";
      return Promise.reject(error);
    }
    if (error.response?.status === 401 && !original._retry) {
      original._retry = true;
      const refresh = getRefreshToken();
      if (refresh) {
        try {
          const res = await axios.post(`${baseURL}/auth/token/refresh/`, { refresh });
          setTokens(res.data.access, refresh);
          original.headers.Authorization = `Bearer ${res.data.access}`;
          return api(original);
        } catch (refreshError) {
          clearTokens();
          window.location.href = "/login";
          return Promise.reject(refreshError);
        }
      }
      clearTokens();
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export default api;
