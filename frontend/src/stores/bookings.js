import { reactive } from "vue";
import {
  cancelBooking as apiCancelBooking,
  createBooking as apiCreateBooking,
  fetchBookingHistory as apiFetchBookingHistory,
  fetchMasterBookings as apiFetchMasterBookings,
  fetchMyBookings as apiFetchMyBookings,
  updateBookingStatus as apiUpdateBookingStatus,
} from "@/api/bookings";

const state = reactive({
  items: [],
  loading: false,
  error: "",
  historyItems: [],
  historyLoading: false,
  historyError: "",
});

const fetchMyBookings = async () => {
  state.loading = true;
  state.error = "";
  try {
    const data = await apiFetchMyBookings();
    state.items = Array.isArray(data) ? data : [];
  } catch (error) {
    state.error = "Не удалось загрузить записи.";
    throw error;
  } finally {
    state.loading = false;
  }
};

const fetchHistory = async () => {
  state.historyLoading = true;
  state.historyError = "";
  try {
    const data = await apiFetchBookingHistory();
    state.historyItems = Array.isArray(data) ? data : [];
  } catch (error) {
    state.historyError = "Не удалось загрузить историю посещений.";
    throw error;
  } finally {
    state.historyLoading = false;
  }
};

const createBooking = async (payload) => {
  state.error = "";
  try {
    const data = await apiCreateBooking(payload);
    state.items = [data, ...state.items];
    return data;
  } catch (error) {
    state.error =
      error.response?.data?.detail || "Не удалось создать запись. Попробуйте позже.";
    throw error;
  }
};

const cancelBooking = async (id) => {
  state.error = "";
  try {
    const data = await apiCancelBooking(id);
    state.items = state.items.map((item) => (item.id === data.id ? data : item));
    return data;
  } catch (error) {
    state.error = error.response?.data?.detail || "Не удалось отменить запись.";
    throw error;
  }
};

const fetchMasterBookings = async () => {
  state.loading = true;
  state.error = "";
  try {
    const data = await apiFetchMasterBookings();
    state.items = Array.isArray(data) ? data : [];
  } catch (error) {
    state.error = "Не удалось загрузить записи мастера.";
    throw error;
  } finally {
    state.loading = false;
  }
};

const updateStatus = async (id, status) => {
  state.error = "";
  try {
    const data = await apiUpdateBookingStatus(id, status);
    state.items = state.items.map((item) => (item.id === data.id ? data : item));
    return data;
  } catch (error) {
    state.error = error.response?.data?.detail || "Не удалось обновить статус.";
    throw error;
  }
};

export const useBookingsStore = () => ({
  state,
  fetchMyBookings,
  fetchHistory,
  createBooking,
  cancelBooking,
  fetchMasterBookings,
  updateStatus,
});
