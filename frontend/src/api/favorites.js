import api from "@/api/client";

export const fetchFavorites = async () => {
  const res = await api.get("/favorites/");
  return res.data;
};

export const addFavorite = async (serviceId) => {
  const res = await api.post("/favorites/", { service_id: serviceId });
  return res.data;
};

export const removeFavorite = async (favoriteId) => {
  const res = await api.delete(`/favorites/${favoriteId}/`);
  return res.data;
};
