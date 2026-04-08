<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import { useChatStore } from "@/stores/chat";
import { useAuthStore } from "@/stores/auth";

const chat = useChatStore();
const auth = useAuthStore();
const { t } = useI18n();
const messageInput = ref("");
const listRef = ref(null);
const pollTimer = ref(null);
let mediaQuery;
let syncMobile = () => {};
const isMobile = ref(false);
const mobileChatOpen = ref(false);

const showList = computed(() => !isMobile.value || !mobileChatOpen.value);
const showChat = computed(() => !isMobile.value || mobileChatOpen.value);

const formatTime = (value) => {
  if (!value) return "";
  const date = new Date(value);
  return date.toLocaleTimeString("ru-RU", { hour: "2-digit", minute: "2-digit" });
};

const formatDate = (value) => {
  if (!value) return "";
  const date = new Date(value);
  return date.toLocaleDateString("ru-RU", { day: "2-digit", month: "short" });
};

const roleLabel = (role) => (role === "master" ? t("messages.roleMaster") : t("messages.roleClient"));

const openConversation = async (conversationId) => {
  chat.state.activeConversationId = conversationId;
  await chat.fetchMessages(conversationId);
  await chat.markRead(conversationId);
  await nextTick();
  scrollToBottom();
  if (isMobile.value) {
    mobileChatOpen.value = true;
  }
};

const send = async () => {
  if (!chat.state.activeConversationId) return;
  await chat.sendMessage(chat.state.activeConversationId, messageInput.value);
  messageInput.value = "";
  await nextTick();
  scrollToBottom();
};

const scrollToBottom = () => {
  if (listRef.value) {
    listRef.value.scrollTop = listRef.value.scrollHeight;
  }
};

const startPolling = () => {
  if (pollTimer.value) return;
  pollTimer.value = setInterval(async () => {
    await chat.fetchConversations();
    if (chat.state.activeConversationId) {
      await chat.fetchMessages(chat.state.activeConversationId);
      await chat.markRead(chat.state.activeConversationId);
    }
  }, 6000);
};

const stopPolling = () => {
  if (pollTimer.value) {
    clearInterval(pollTimer.value);
    pollTimer.value = null;
  }
};

watch(
  () => chat.activeMessages.value.length,
  async () => {
    await nextTick();
    scrollToBottom();
  }
);

onMounted(async () => {
  mediaQuery = window.matchMedia("(max-width: 768px)");
  syncMobile = () => {
    isMobile.value = mediaQuery.matches;
    if (!mediaQuery.matches) {
      mobileChatOpen.value = false;
    }
  };
  syncMobile();
  mediaQuery.addEventListener("change", syncMobile);

  await chat.fetchConversations();
  if (chat.state.activeConversationId) {
    try {
      await openConversation(chat.state.activeConversationId);
    } catch (error) {
      if (!isMobile.value && chat.state.conversations.length) {
        await openConversation(chat.state.conversations[0].id);
      }
    }
  } else if (!isMobile.value && chat.state.conversations.length) {
    await openConversation(chat.state.conversations[0].id);
  }
  startPolling();
});

onBeforeUnmount(() => {
  stopPolling();
  if (mediaQuery) {
    mediaQuery.removeEventListener("change", syncMobile);
  }
});
</script>

<template>
  <div class="messages-layout">
    <div v-if="showList" class="card inbox">
      <div class="section-heading">
        <p class="tag">{{ t("messages.title") }}</p>
        <h3>{{ t("messages.dialogs") }}</h3>
      </div>
      <div v-if="chat.state.loadingConversations" class="muted">{{ t("common.loading") }}</div>
      <div v-else-if="!chat.state.conversations.length" class="empty muted">
        {{ t("messages.empty") }}
      </div>
      <div v-else class="list">
        <button
          v-for="conv in chat.state.conversations"
          :key="conv.id"
          class="item"
          :class="{ active: conv.id === chat.state.activeConversationId }"
          type="button"
          @click="openConversation(conv.id)"
        >
          <div class="avatar">
            <img v-if="conv.counterpart?.avatar_url" :src="conv.counterpart.avatar_url" alt="" />
            <span v-else>{{ conv.counterpart?.name?.[0] || "B" }}</span>
          </div>
          <div class="meta">
            <div class="name-row">
              <strong>{{ conv.counterpart?.name }}</strong>
              <span class="role">{{ roleLabel(conv.counterpart?.role) }}</span>
            </div>
            <p class="muted">{{ conv.last_message_preview || t("messages.noMessages") }}</p>
          </div>
          <div class="side">
            <span class="time">{{ formatTime(conv.last_message_at) }}</span>
            <span v-if="conv.unread_count" class="badge">{{ conv.unread_count }}</span>
          </div>
        </button>
      </div>
    </div>

    <div v-if="showChat" class="card chat">
      <div v-if="!chat.state.activeConversationId" class="empty muted">
        {{ t("messages.selectDialog") }}
      </div>
      <template v-else>
        <div class="chat-header">
          <button v-if="isMobile" type="button" class="back" @click="mobileChatOpen = false">
            {{ t("messages.back") }}
          </button>
          <div class="header-main">
            <div class="avatar">
              <img
                v-if="chat.activeConversation.value?.counterpart?.avatar_url"
                :src="chat.activeConversation.value?.counterpart?.avatar_url"
                alt=""
              />
              <span v-else>{{ chat.activeConversation.value?.counterpart?.name?.[0] || "B" }}</span>
            </div>
            <div>
              <h4>{{ chat.activeConversation.value?.counterpart?.name }}</h4>
              <p class="muted">{{ roleLabel(chat.activeConversation.value?.counterpart?.role) }}</p>
            </div>
          </div>
        </div>
        <div ref="listRef" class="messages">
          <div
            v-for="msg in chat.activeMessages.value"
            :key="msg.id"
            class="bubble"
            :class="{ own: msg.sender_id === auth.state.user?.id }"
          >
            <p>{{ msg.body }}</p>
            <span class="time">{{ formatTime(msg.created_at) }} · {{ formatDate(msg.created_at) }}</span>
          </div>
        </div>
        <form class="composer" @submit.prevent="send">
          <input
            v-model="messageInput"
            type="text"
            :placeholder="t('messages.placeholder')"
            :disabled="chat.state.sending"
          />
          <button class="cta primary" type="submit" :disabled="!messageInput.trim()">
            {{ t("messages.send") }}
          </button>
        </form>
      </template>
    </div>
  </div>
</template>

<style scoped>
.messages-layout {
  display: grid;
  grid-template-columns: 340px 1fr;
  gap: 1rem;
  min-height: 70vh;
}

.inbox {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  height: 70vh;
  overflow: hidden;
}

.list {
  display: grid;
  gap: 0.5rem;
  overflow-y: auto;
  padding-right: 0.2rem;
}

.item {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 0.6rem;
  align-items: center;
  padding: 0.55rem 0.6rem;
  border-radius: 12px;
  border: 1px solid rgba(52, 95, 32, 0.12);
  background: #fff;
  text-align: left;
  cursor: pointer;
  transition: box-shadow 0.2s ease, border-color 0.2s ease;
}

.item.active {
  border-color: var(--color-matcha);
  box-shadow: 0 12px 26px rgba(52, 95, 32, 0.12);
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(52, 95, 32, 0.08);
  display: grid;
  place-items: center;
  font-weight: 700;
  color: var(--color-avocado);
  overflow: hidden;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.meta p {
  margin: 0.2rem 0 0;
}

.name-row {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  flex-wrap: wrap;
}

.role {
  font-size: 0.75rem;
  color: rgba(47, 54, 47, 0.7);
}

.side {
  text-align: right;
  display: grid;
  gap: 0.2rem;
}

.badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 20px;
  height: 20px;
  border-radius: 999px;
  background: var(--color-matcha);
  color: #1f260f;
  font-weight: 700;
  font-size: 0.75rem;
}

.chat {
  display: grid;
  grid-template-rows: auto 1fr auto;
  gap: 0.6rem;
  height: 70vh;
}

.chat-header {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding-bottom: 0.6rem;
  border-bottom: 1px solid rgba(52, 95, 32, 0.12);
  position: sticky;
  top: 0;
  background: #fff;
  z-index: 2;
}

.header-main {
  display: flex;
  align-items: center;
  gap: 0.7rem;
}

.chat-header .avatar {
  width: 44px;
  height: 44px;
}

.back {
  background: transparent;
  border: none;
  color: var(--color-avocado);
  font-weight: 700;
  cursor: pointer;
  padding: 0.2rem 0.4rem;
}

.messages {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  overflow-y: auto;
  padding-right: 0.2rem;
}

.bubble {
  max-width: 68%;
  padding: 0.55rem 0.75rem;
  border-radius: 14px;
  background: rgba(52, 95, 32, 0.08);
  align-self: flex-start;
  display: inline-flex;
  flex-direction: column;
  gap: 0.3rem;
}

.bubble.own {
  background: rgba(232, 234, 108, 0.35);
  align-self: flex-end;
}

.bubble p {
  margin: 0;
  font-size: 0.95rem;
}

.bubble .time {
  font-size: 0.75rem;
  color: rgba(47, 54, 47, 0.6);
}

.composer {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 0.5rem;
  align-items: center;
  padding-top: 0.6rem;
  border-top: 1px solid rgba(52, 95, 32, 0.12);
  background: #fff;
  position: sticky;
  bottom: 0;
}

.composer input {
  padding: 0.7rem 0.9rem;
  border-radius: 12px;
  border: 1px solid rgba(52, 95, 32, 0.2);
  background: #fff;
}

.empty {
  text-align: center;
  padding: 1.4rem 0;
}

@media (max-width: 960px) {
  .messages-layout {
    grid-template-columns: 300px 1fr;
  }
}

@media (max-width: 768px) {
  .messages-layout {
    grid-template-columns: 1fr;
    min-height: auto;
  }

  .inbox,
  .chat {
    height: auto;
    min-height: calc(100dvh - 260px);
  }

  .item {
    padding: 0.75rem;
  }

  .messages {
    min-height: 45vh;
  }

  .bubble {
    max-width: 100%;
  }

  .composer {
    grid-template-columns: 1fr;
    gap: 0.45rem;
  }

  .composer input {
    min-height: 44px;
  }

  .composer .cta {
    width: 100%;
    min-height: 44px;
  }
}
</style>
