import api from "@/api/client";

export const fetchMasters = async () => {
  const res = await api.get("/masters/");
  return res.data;
};
