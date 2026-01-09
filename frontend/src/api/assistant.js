import api from "@/api/client";

export const sendAiMessage = async (payload) => {
  const res = await api.post("/api/ai/chat/", payload);
  return res.data;
};
