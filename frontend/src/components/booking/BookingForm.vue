<script setup>
import { useI18n } from "vue-i18n";
import { useReveal } from "@/composables/useReveal";

const props = defineProps({
  form: {
    type: Object,
    default: () => ({ name: "", phone: "", email: "", comment: "" }),
  },
});

const emit = defineEmits(["update:form"]);
const { revealRef } = useReveal();
const { t } = useI18n();

const update = (key, value) => {
  emit("update:form", { ...props.form, [key]: value });
};
</script>

<template>
  <section class="card reveal" :ref="revealRef">
    <div class="section-heading">
      <p class="tag">{{ t("booking.stepContact") }}</p>
      <h3>{{ t("booking.contactTitle") }}</h3>
    </div>
    <div class="form-grid">
      <label>
        <span>{{ t("booking.name") }}</span>
        <input
          type="text"
          :value="form.name"
          :placeholder="t('booking.namePlaceholder')"
          @input="update('name', $event.target.value)"
        />
      </label>
      <label>
        <span>{{ t("booking.phone") }}</span>
        <input
          type="tel"
          :value="form.phone"
          :placeholder="t('booking.phonePlaceholder')"
          @input="update('phone', $event.target.value)"
        />
      </label>
      <label>
        <span>{{ t("booking.email") }}</span>
        <input
          type="email"
          :value="form.email"
          :placeholder="t('booking.emailPlaceholder')"
          @input="update('email', $event.target.value)"
        />
      </label>
      <label class="full">
        <span>{{ t("booking.comment") }}</span>
        <textarea
          :value="form.comment"
          :placeholder="t('booking.commentPlaceholder')"
          rows="3"
          @input="update('comment', $event.target.value)"
        ></textarea>
      </label>
    </div>
  </section>
</template>

<style scoped>
.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 0.9rem;
}

label {
  display: grid;
  gap: 0.35rem;
  color: var(--text-body);
}

span {
  font-weight: 700;
}

input,
textarea {
  border: 1px solid rgba(52, 95, 32, 0.18);
  background: #fff;
  border-radius: 12px;
  padding: 0.75rem 0.9rem;
  font-family: "Inter", sans-serif;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

input:focus,
textarea:focus {
  outline: none;
  border-color: var(--color-matcha);
  box-shadow: 0 10px 24px rgba(52, 95, 32, 0.12);
}

.full {
  grid-column: 1 / -1;
}

@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }
}
</style>
