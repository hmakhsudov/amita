import api from "@/api/client";

export const fetchAdminDashboard = async () => {
  const res = await api.get("/admin/dashboard/");
  return res.data;
};

export const fetchAdminBookings = async () => {
  const res = await api.get("/admin/bookings/");
  return res.data;
};

export const updateAdminBookingStatus = async (bookingId, status) => {
  const res = await api.patch(`/admin/bookings/${bookingId}/status/`, { status });
  return res.data;
};

export const fetchAdminUsers = async () => {
  const res = await api.get("/admin/users/");
  return res.data;
};

export const createMasterUser = async (payload) => {
  const res = await api.post("/admin/users/", payload);
  return res.data;
};
