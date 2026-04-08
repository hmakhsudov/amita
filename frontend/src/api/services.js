import api from "@/api/client";

export const fetchCategories = async () => {
  const res = await api.get("/categories/");
  return res.data;
};

export const fetchServices = async (params = {}) => {
  const res = await api.get("/services/", { params });
  return res.data;
};

export const deleteService = async (id) => {
  const res = await api.delete(`/services/${id}/`);
  return res.data;
};

export const createService = async (payload) => {
  const res = await api.post("/services/", payload);
  return res.data;
};

export const fetchService = async (id) => {
  const res = await api.get(`/services/${id}/`);
  return res.data;
};

export const updateService = async (id, payload) => {
  const res = await api.patch(`/services/${id}/`, payload);
  return res.data;
};

export const createCategory = async (payload) => {
  const res = await api.post("/categories/", payload);
  return res.data;
};

export const updateCategory = async (id, payload) => {
  const res = await api.patch(`/categories/${id}/`, payload);
  return res.data;
};

export const deleteCategory = async (id) => {
  const res = await api.delete(`/categories/${id}/`);
  return res.data;
};
