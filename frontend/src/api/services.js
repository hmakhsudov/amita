import api from "@/api/client";

export const fetchCategories = async () => {
  const res = await api.get("/api/categories/");
  return res.data;
};

export const fetchServices = async (params = {}) => {
  const res = await api.get("/api/services/", { params });
  return res.data;
};

export const createService = async (payload) => {
  const res = await api.post("/api/services/", payload);
  return res.data;
};

export const fetchService = async (id) => {
  const res = await api.get(`/api/services/${id}/`);
  return res.data;
};

export const updateService = async (id, payload) => {
  const res = await api.patch(`/api/services/${id}/`, payload);
  return res.data;
};
