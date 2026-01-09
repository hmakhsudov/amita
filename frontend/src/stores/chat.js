import { computed, reactive } from "vue";
import {
  createConversation as apiCreateConversation,
  fetchConversations as apiFetchConversations,
  fetchMessages as apiFetchMessages,
  fetchUnreadTotal as apiFetchUnreadTotal,
  markRead as apiMarkRead,
  sendMessage as apiSendMessage,
} from "@/api/chat";

const state = reactive({
  conversations: [],
  activeConversationId: "",
  messagesByConversation: {},
  loadingConversations: false,
  loadingMessages: false,
  sending: false,
  error: "",
  unreadTotal: 0,
});

const setConversations = (items) => {
  state.conversations = Array.isArray(items) ? items : [];
};

const fetchConversations = async () => {
  state.loadingConversations = true;
  state.error = "";
  try {
    const data = await apiFetchConversations();
    setConversations(data);
    state.unreadTotal = data.reduce((sum, item) => sum + (item.unread_count || 0), 0);
  } catch (error) {
    state.error = "Не удалось загрузить сообщения.";
    throw error;
  } finally {
    state.loadingConversations = false;
  }
};

const fetchUnreadTotal = async () => {
  try {
    const data = await apiFetchUnreadTotal();
    state.unreadTotal = data?.unread_count || 0;
  } catch (error) {
    // ignore badge errors
  }
};

const openConversation = async (counterpartUserId) => {
  state.error = "";
  try {
    const conv = await apiCreateConversation(counterpartUserId);
    const existing = state.conversations.find((item) => item.id === conv.id);
    if (!existing) {
      state.conversations = [conv, ...state.conversations];
    } else {
      state.conversations = state.conversations.map((item) =>
        item.id === conv.id ? { ...item, ...conv } : item
      );
    }
    state.activeConversationId = conv.id;
    await fetchMessages(conv.id);
    await markRead(conv.id);
    return conv;
  } catch (error) {
    state.error = "Не удалось открыть диалог.";
    throw error;
  }
};

const fetchMessages = async (conversationId, params = {}) => {
  state.loadingMessages = true;
  state.error = "";
  try {
    const data = await apiFetchMessages(conversationId, params);
    state.messagesByConversation[conversationId] = Array.isArray(data) ? data : [];
  } catch (error) {
    state.error = "Не удалось загрузить сообщения.";
    throw error;
  } finally {
    state.loadingMessages = false;
  }
};

const sendMessage = async (conversationId, body) => {
  const text = (body || "").trim();
  if (!text) return;
  state.sending = true;
  state.error = "";
  try {
    const data = await apiSendMessage(conversationId, text);
    const current = state.messagesByConversation[conversationId] || [];
    state.messagesByConversation[conversationId] = [...current, data];
    state.conversations = state.conversations.map((item) =>
      item.id === conversationId
        ? {
            ...item,
            last_message_preview: text.slice(0, 120),
            last_message_at: data.created_at,
          }
        : item
    );
    return data;
  } catch (error) {
    state.error = "Не удалось отправить сообщение.";
    throw error;
  } finally {
    state.sending = false;
  }
};

const markRead = async (conversationId) => {
  try {
    await apiMarkRead(conversationId);
    state.conversations = state.conversations.map((item) =>
      item.id === conversationId ? { ...item, unread_count: 0 } : item
    );
    state.unreadTotal = state.conversations.reduce(
      (sum, item) => sum + (item.unread_count || 0),
      0
    );
  } catch (error) {
    // ignore
  }
};

const activeConversation = computed(() =>
  state.conversations.find((item) => item.id === state.activeConversationId) || null
);

const activeMessages = computed(
  () => state.messagesByConversation[state.activeConversationId] || []
);

export const useChatStore = () => ({
  state,
  activeConversation,
  activeMessages,
  fetchConversations,
  fetchUnreadTotal,
  openConversation,
  fetchMessages,
  sendMessage,
  markRead,
});
