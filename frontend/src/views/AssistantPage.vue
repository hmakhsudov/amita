<script setup>
import { computed, nextTick, onMounted, ref } from "vue";
import { useI18n } from "vue-i18n";
import { useAuthStore } from "@/stores/auth";
import { usePlanStore } from "@/stores/plan";
import { useRouter } from "vue-router";
import { sendAiMessage } from "@/api/assistant";

const auth = useAuthStore();
const plan = usePlanStore();
const router = useRouter();

const input = ref("");
const messages = ref([]);
const sending = ref(false);
const error = ref("");
const conversationId = ref(localStorage.getItem("assistantConversationId") || "");
const messagesRef = ref(null);
const { t } = useI18n();

const isClient = computed(() => auth.state.user?.role === "client");
const canShowPlanAction = computed(
  () => !auth.isAuthenticated.value || auth.state.user?.role === "client"
);
const canShowBookingAction = computed(() => !auth.isAuthenticated.value || isClient.value);

const pushUserMessage = (text) => {
  messages.value.push({
    role: "user",
    content: text,
  });
};

const pushAssistantMessage = (payload) => {
  messages.value.push({
    role: "assistant",
    content: payload.assistant_message,
    safety_note: payload.safety_note,
    follow_up_questions: payload.follow_up_questions || [],
    recommended_services: payload.recommended_services || [],
  });
};

const scrollToBottom = async () => {
  await nextTick();
  if (messagesRef.value) {
    messagesRef.value.scrollTop = messagesRef.value.scrollHeight;
  }
};

const sendMessage = async (text) => {
  const message = (text ?? input.value).trim();
  if (!message || sending.value) return;
  error.value = "";
  pushUserMessage(message);
  input.value = "";
  await scrollToBottom();
  sending.value = true;
  try {
    const payload = await sendAiMessage({
      message,
      conversation_id: conversationId.value || undefined,
      context: {},
    });
    if (payload.conversation_id) {
      conversationId.value = payload.conversation_id;
      localStorage.setItem("assistantConversationId", payload.conversation_id);
    }
    pushAssistantMessage(payload);
    await scrollToBottom();
  } catch (err) {
    error.value = t("assistant.error");
  } finally {
    sending.value = false;
  }
};

const sendFollowUp = (question) => {
  const text = getFollowUpReply(question);
  sendMessage(text);
};

const addToPlan = async (serviceId) => {
  if (!auth.isAuthenticated.value) {
    error.value = t("assistant.loginToPlan");
    setTimeout(() => {
      error.value = "";
      router.push("/login");
    }, 1200);
    return;
  }
  try {
    await plan.addToPlan(serviceId, 1);
  } catch (err) {
    error.value = plan.state.error || t("assistant.planError");
    setTimeout(() => {
      error.value = "";
    }, 1600);
  }
};

onMounted(() => {
  messages.value = [
    {
      role: "assistant",
      content: t("assistant.welcome"),
      safety_note: t("assistant.safety"),
      follow_up_questions: [t("assistant.followUpGoal"), t("assistant.followUpConstraints")],
      recommended_services: [],
    },
  ];
});

const getFollowUpReply = (text) => {
  const trimmed = text.trim();
  if (!trimmed.endsWith("?")) return trimmed;
  const lower = trimmed.toLowerCase();
  if (lower.includes("цель") || lower.includes("ziel")) return t("assistant.replyGoal");
  if (lower.includes("бюджет") || lower.includes("budget")) return t("assistant.replyBudget");
  if (lower.includes("врем") || lower.includes("zeit")) return t("assistant.replyTime");
  if (lower.includes("мастер") || lower.includes("experte")) return t("assistant.replyMaster");
  if (lower.includes("беспокоит") || lower.includes("состояние")) {
    return t("assistant.replyConcern");
  }
  return t("assistant.replyDefault");
};
</script>

<template>
  <section class="section assistant">
    <div class="section-heading">
      <p class="tag">{{ t("assistant.tag") }}</p>
      <h1>{{ t("assistant.title") }}</h1>
      <p class="muted">{{ t("assistant.subtitle") }}</p>
    </div>

    <div class="card chat">
      <div ref="messagesRef" class="messages">
        <article
          v-for="(msg, index) in messages"
          :key="index"
          class="bubble"
          :class="msg.role"
        >
          <div class="text">{{ msg.content }}</div>
          <p v-if="msg.safety_note" class="safety-note">{{ msg.safety_note }}</p>

          <div v-if="msg.recommended_services?.length" class="recommendations">
            <h4>{{ t("assistant.recommendations") }}</h4>
            <div class="cards">
              <article
                v-for="service in msg.recommended_services"
                :key="service.service_id"
                class="service-card"
              >
                <div>
                  <p class="tag">{{ service.category }}</p>
                  <h3>{{ service.name }}</h3>
                  <p class="muted">
                    {{ service.duration_minutes }} {{ t("common.minutesShort") }} •
                    {{ service.price }} €
                  </p>
                  <p class="muted">{{ service.reason }}</p>
                </div>
                <div class="actions">
                  <router-link
                    v-if="canShowBookingAction"
                    class="cta secondary"
                    :to="{ path: '/booking', query: { serviceId: service.service_id } }"
                  >
                    {{ t("assistant.book") }}
                  </router-link>
                  <button
                    v-if="canShowPlanAction"
                    class="cta primary"
                    type="button"
                    @click="addToPlan(service.service_id)"
                  >
                    {{ t("assistant.addToPlan") }}
                  </button>
                </div>
              </article>
            </div>
          </div>

          <div v-if="msg.follow_up_questions?.length" class="follow-ups">
            <p class="muted">{{ t("assistant.quickReplies") }}</p>
            <div class="chips">
              <button
                v-for="question in msg.follow_up_questions"
                :key="question"
                class="chip"
                type="button"
                @click="sendFollowUp(question)"
              >
                {{ question }}
              </button>
            </div>
          </div>
        </article>

        <div v-if="sending" class="typing muted">{{ t("assistant.typing") }}</div>
      </div>

      <form class="input" @submit.prevent="sendMessage">
        <input
          v-model="input"
          type="text"
          :placeholder="t('assistant.placeholder')"
          :disabled="sending"
          @keydown.enter.exact.prevent="sendMessage"
        />
        <button class="cta primary" type="submit" :disabled="sending || !input.trim()">
          {{ t("assistant.send") }}
        </button>
      </form>
      <p v-if="error" class="error">{{ error }}</p>
    </div>
  </section>
</template>

<style scoped>
.assistant {
  display: grid;
  gap: 1.2rem;
}

.chat {
  display: grid;
  gap: 1rem;
}

.messages {
  display: grid;
  gap: 1rem;
}

.bubble {
  padding: 0.9rem;
  border-radius: 16px;
  border: 1px solid rgba(52, 95, 32, 0.12);
  background: #fff;
}

.bubble.user {
  background: rgba(232, 234, 108, 0.18);
  border-color: rgba(52, 95, 32, 0.08);
}

.text {
  font-weight: 600;
}

.safety-note {
  margin-top: 0.5rem;
  font-size: 0.85rem;
  color: rgba(52, 95, 32, 0.75);
}

.recommendations {
  margin-top: 0.8rem;
  display: grid;
  gap: 0.7rem;
}

.cards {
  display: grid;
  gap: 0.7rem;
}

.service-card {
  display: grid;
  gap: 0.5rem;
  padding: 0.8rem;
  border-radius: 14px;
  border: 1px solid rgba(52, 95, 32, 0.12);
  background: #fff;
}

.actions {
  display: flex;
  gap: 0.6rem;
  flex-wrap: wrap;
}

.follow-ups {
  margin-top: 0.7rem;
  display: grid;
  gap: 0.4rem;
}

.chips {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.chip {
  border: 1px solid rgba(52, 95, 32, 0.18);
  background: #fff;
  border-radius: 999px;
  padding: 0.4rem 0.8rem;
  cursor: pointer;
  font-weight: 600;
  color: var(--color-avocado);
}

.typing {
  font-size: 0.9rem;
}

.input {
  display: flex;
  gap: 0.6rem;
  flex-wrap: wrap;
  align-items: center;
}

.input input {
  flex: 1;
  min-width: 220px;
  border: 1px solid rgba(52, 95, 32, 0.18);
  background: #fff;
  border-radius: 12px;
  padding: 0.75rem 0.9rem;
}

.error {
  color: #8a1a1a;
  font-weight: 600;
}

@media (max-width: 768px) {
  .chat {
    min-height: 70vh;
  }
  .messages {
    padding-bottom: 0.8rem;
  }
  .bubble {
    max-width: 100%;
  }
  .input {
    position: sticky;
    bottom: 0;
    background: var(--card);
    padding-bottom: calc(0.6rem + env(safe-area-inset-bottom));
  }
  .input input,
  .input .cta {
    width: 100%;
    min-height: 44px;
  }
  .actions {
    flex-direction: column;
  }
  .actions .cta {
    width: 100%;
    min-height: 44px;
  }
}
</style>
