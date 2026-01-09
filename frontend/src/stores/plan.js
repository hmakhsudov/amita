import { computed, reactive } from "vue";
import api from "@/api/client";

const state = reactive({
  items: [],
  totalCount: 0,
  totalPrice: 0,
  loading: false,
  error: "",
});

const setFromPlan = (payload) => {
  state.items = payload?.items || [];
  state.totalCount = Number(payload?.total_count || 0);
  state.totalPrice = Number(payload?.total_price || 0);
  if (Number.isNaN(state.totalCount)) state.totalCount = 0;
  if (Number.isNaN(state.totalPrice)) state.totalPrice = 0;
};

const fetchPlan = async () => {
  state.loading = true;
  state.error = "";
  try {
    const res = await api.get("/plan/");
    setFromPlan(res.data);
  } catch (error) {
    state.error = "Не удалось загрузить план.";
    throw error;
  } finally {
    state.loading = false;
  }
};

const addToPlan = async (serviceId, qty = 1) => {
  state.error = "";
  try {
    const res = await api.post("/plan/items/", { service_id: serviceId, qty });
    setFromPlan(res.data);
    return res.data;
  } catch (error) {
    state.error = "Не удалось добавить услугу в план.";
    throw error;
  }
};

const updateQty = async (itemId, qty) => {
  state.error = "";
  try {
    const res = await api.patch(`/plan/items/${itemId}/`, { qty });
    setFromPlan(res.data);
  } catch (error) {
    state.error = "Не удалось обновить количество.";
    throw error;
  }
};

const removeItem = async (itemId) => {
  state.error = "";
  try {
    const res = await api.delete(`/plan/items/${itemId}/`);
    setFromPlan(res.data);
  } catch (error) {
    state.error = "Не удалось удалить позицию.";
    throw error;
  }
};

const clearPlan = async () => {
  state.error = "";
  try {
    const res = await api.delete("/plan/clear/");
    setFromPlan(res.data);
  } catch (error) {
    state.error = "Не удалось очистить план.";
    throw error;
  }
};

const reset = () => {
  state.items = [];
  state.totalCount = 0;
  state.totalPrice = 0;
  state.loading = false;
  state.error = "";
};

const count = computed(() => state.totalCount);
const total = computed(() => state.totalPrice);
const has = (serviceId) => state.items.some((item) => item.service?.id === serviceId);

export const usePlanStore = () => ({
  state,
  fetchPlan,
  addToPlan,
  updateQty,
  removeItem,
  clearPlan,
  reset,
  count,
  total,
  has,
});
