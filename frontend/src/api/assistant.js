import api from "@/api/client";

export const sendAiMessage = async (payload) => {
  const res = await api.post("/ai/chat/", payload);
  return res.data;
};
