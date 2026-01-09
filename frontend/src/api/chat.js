import api from "@/api/client";

export const fetchConversations = async () => {
  const res = await api.get("/api/conversations/");
  return res.data;
};

export const createConversation = async (counterpartUserId) => {
  const res = await api.post("/api/conversations/", { counterpart_user_id: counterpartUserId });
  return res.data;
};

export const fetchMessages = async (conversationId, params = {}) => {
  const res = await api.get(`/api/conversations/${conversationId}/messages/`, { params });
  return res.data;
};

export const sendMessage = async (conversationId, body) => {
  const res = await api.post(`/api/conversations/${conversationId}/messages/`, { body });
  return res.data;
};

export const markRead = async (conversationId) => {
  const res = await api.post(`/api/conversations/${conversationId}/read/`);
  return res.data;
};

export const fetchUnreadTotal = async () => {
  const res = await api.get("/api/conversations/unread_count/");
  return res.data;
};
