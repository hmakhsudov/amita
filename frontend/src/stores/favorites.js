import { computed, reactive } from "vue";
import { addFavorite as apiAddFavorite, fetchFavorites as apiFetchFavorites, removeFavorite as apiRemoveFavorite } from "@/api/favorites";
import { i18n } from "@/i18n";

const state = reactive({
  favorites: [],
  loading: false,
  error: "",
});

const fetchFavorites = async () => {
  state.loading = true;
  state.error = "";
  try {
    const data = await apiFetchFavorites();
    state.favorites = Array.isArray(data) ? data : [];
  } catch (error) {
    state.error = i18n.global.t("favorites.loadError");
    throw error;
  } finally {
    state.loading = false;
  }
};

const addFavorite = async (serviceId) => {
  state.error = "";
  try {
    const data = await apiAddFavorite(serviceId);
    if (!state.favorites.find((item) => item.id === data.id)) {
      state.favorites = [data, ...state.favorites];
    }
    return data;
  } catch (error) {
    state.error = i18n.global.t("favorites.addError");
    throw error;
  }
};

const removeFavorite = async (favoriteId) => {
  state.error = "";
  try {
    await apiRemoveFavorite(favoriteId);
    state.favorites = state.favorites.filter((item) => item.id !== favoriteId);
  } catch (error) {
    state.error = i18n.global.t("favorites.removeError");
    throw error;
  }
};

const isFavorite = (serviceId) =>
  state.favorites.some((item) => item.service?.id === serviceId);

const findFavoriteId = (serviceId) =>
  state.favorites.find((item) => item.service?.id === serviceId)?.id || null;

const count = computed(() => state.favorites.length);

export const useFavoritesStore = () => ({
  state,
  fetchFavorites,
  addFavorite,
  removeFavorite,
  isFavorite,
  findFavoriteId,
  count,
});
