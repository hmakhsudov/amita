import api from "@/api/client";

export const fetchAvailability = async (date, serviceId, masterId) => {
  const res = await api.get("/api/availability/", {
    params: { date, service_id: serviceId, master_id: masterId },
  });
  return res.data;
};

export const createBooking = async (payload) => {
  const res = await api.post("/api/bookings/", payload);
  return res.data;
};

export const fetchMyBookings = async () => {
  const res = await api.get("/api/bookings/");
  return res.data;
};

export const fetchBookingHistory = async () => {
  const res = await api.get("/api/bookings/history/");
  return res.data;
};

export const cancelBooking = async (id) => {
  const res = await api.post(`/api/bookings/${id}/cancel/`);
  return res.data;
};

export const fetchMasterBookings = async () => {
  const res = await api.get("/api/master/bookings/");
  return res.data;
};

export const updateBookingStatus = async (id, status) => {
  const res = await api.patch(`/api/master/bookings/${id}/status/`, { status });
  return res.data;
};
