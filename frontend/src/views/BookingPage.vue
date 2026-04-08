<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import BookingCalendar from "@/components/booking/BookingCalendar.vue";
import BookingForm from "@/components/booking/BookingForm.vue";
import BookingMasterStep from "@/components/booking/BookingMasterStep.vue";
import BookingServiceStep from "@/components/booking/BookingServiceStep.vue";
import BookingSummary from "@/components/booking/BookingSummary.vue";
import { useReveal } from "@/composables/useReveal";
import { fetchServices } from "@/api/services";
import { fetchAvailability } from "@/api/bookings";
import { useAuthStore } from "@/stores/auth";
import { useBookingsStore } from "@/stores/bookings";
import { useRoute, useRouter } from "vue-router";

const categoryNames = ref([]);
const services = ref([]);
const servicesLoading = ref(false);
const servicesError = ref("");

const slots = ref([]);
const slotsLoading = ref(false);
const slotsError = ref("");
const toast = ref("");

const state = ref({
  category: "all",
  serviceId: null,
  masterId: null,
  date: "",
  slot: "",
  form: { name: "", phone: "", email: "", comment: "" },
  confirmed: false,
});

const { revealRef } = useReveal();
const auth = useAuthStore();
const bookings = useBookingsStore();
const router = useRouter();
const route = useRoute();
const { t, locale } = useI18n();

const categories = computed(() => [
  { value: "all", label: t("services.all") },
  ...categoryNames.value.map((name) => ({ value: name, label: name })),
]);

const today = () => new Date().toISOString().slice(0, 10);
state.value.date = today();

const chosenService = computed(
  () => services.value.find((s) => s.id === state.value.serviceId) || null
);
const masters = computed(() => chosenService.value?.masters || []);
const chosenMaster = computed(
  () => masters.value.find((m) => m.id === state.value.masterId) || null
);
const selectedSlotLabel = computed(() => {
  const match = slots.value.find((slot) => slot.value === state.value.slot);
  return match?.label || "";
});

const formatTime = (iso) => {
  const date = new Date(iso);
  return date.toLocaleTimeString(locale.value, { hour: "2-digit", minute: "2-digit" });
};

const formatDateLabel = (iso) => {
  const date = new Date(iso);
  return date.toLocaleDateString(locale.value, {
    day: "2-digit",
    month: "long",
  });
};

const loadServices = async () => {
  servicesLoading.value = true;
  servicesError.value = "";
  try {
    const data = await fetchServices();
    services.value = Array.isArray(data)
      ? data.map((item) => ({
          id: item.id,
          name: item.name,
          category: item.category?.name || item.category_name || t("services.uncategorized"),
          description: item.description || t("services.descFallback"),
          duration: item.duration_minutes || 60,
          price: item.price,
          masters: Array.isArray(item.masters) ? item.masters : [],
        }))
      : [];
    categoryNames.value = [...new Set(services.value.map((service) => service.category))];
    const preselectId = Number(route.query.serviceId);
    if (preselectId && !state.value.serviceId) {
      const preselected = services.value.find((service) => service.id === preselectId);
      if (preselected) {
        state.value.serviceId = preselected.id;
        state.value.category = preselected.category;
      }
    }
  } catch (error) {
    servicesError.value = t("services.loadError");
  } finally {
    servicesLoading.value = false;
  }
};

const loadAvailability = async () => {
  slotsError.value = "";
  slots.value = [];
  state.value.slot = "";
  if (!state.value.date || !state.value.serviceId || !state.value.masterId) return;
  slotsLoading.value = true;
  try {
    const data = await fetchAvailability(
      state.value.date,
      state.value.serviceId,
      state.value.masterId
    );
    const list = Array.isArray(data?.slots) ? data.slots : [];
    slots.value = list.map((iso) => ({
      value: iso,
      label: formatTime(iso),
      dateLabel: formatDateLabel(iso),
    }));
  } catch (error) {
    slotsError.value =
      error.response?.data?.detail || t("booking.slotsError");
  } finally {
    slotsLoading.value = false;
  }
};

const confirmBooking = async () => {
  if (!auth.isAuthenticated.value) {
    toast.value = t("booking.loginToBook");
    setTimeout(() => {
      toast.value = "";
      router.push("/login");
    }, 1200);
    return;
  }
  if (!chosenService.value || !state.value.masterId || !state.value.slot) {
    toast.value = t("booking.selectAll");
    setTimeout(() => {
      toast.value = "";
    }, 1600);
    return;
  }
  try {
    await bookings.createBooking({
      service_id: chosenService.value.id,
      master_id: state.value.masterId,
      start_at: state.value.slot,
      comment: state.value.form.comment,
      client_name: state.value.form.name,
      client_phone: state.value.form.phone,
      client_email: state.value.form.email,
    });
    state.value.confirmed = true;
    toast.value = t("booking.created");
    setTimeout(() => {
      toast.value = "";
      router.push({ path: "/profile", query: { tab: "bookings" } });
    }, 1200);
  } catch (error) {
    toast.value = bookings.state.error || t("booking.createError");
    setTimeout(() => {
      toast.value = "";
    }, 2000);
  }
};

const updateFormFromProfile = () => {
  if (!auth.state.user) return;
  state.value.form = {
    ...state.value.form,
    name: auth.state.user.name || state.value.form.name,
    phone: auth.state.user.phone || state.value.form.phone,
    email: auth.state.user.email || state.value.form.email,
  };
};

watch(
  () => auth.state.user,
  () => updateFormFromProfile(),
  { immediate: true }
);

watch(
  () => state.value.serviceId,
  () => {
    state.value.masterId = null;
    state.value.slot = "";
    slots.value = [];
  }
);

watch(
  () => [state.value.serviceId, state.value.masterId, state.value.date],
  () => {
    loadAvailability();
  }
);

onMounted(loadServices);
</script>

<template>
  <div class="page">
    <div class="top reveal" :ref="revealRef">
      <div>
        <p class="tag">{{ t("nav.booking") }}</p>
        <h1>{{ t("booking.title") }}</h1>
        <p class="muted">{{ t("booking.subtitle") }}</p>
      </div>
      <div class="card note">
        <strong>{{ t("home.howTitle") }}</strong>
        <p class="muted">{{ t("booking.flow") }}</p>
      </div>
    </div>

    <div class="grid-2">
      <div class="stack">
        <BookingServiceStep
          :categories="categories"
          :services="services"
          :selected-category="state.category"
          :selected-service-id="state.serviceId"
          @update:category="state.category = $event"
          @select="(svc) => (state.serviceId = svc.id)"
        />
        <div v-if="servicesLoading" class="card note">{{ t("common.loading") }}</div>
        <div v-else-if="servicesError" class="card note error">{{ servicesError }}</div>
        <BookingMasterStep
          :masters="masters"
          :selected-id="state.masterId"
          :has-service="Boolean(state.serviceId)"
          @select="(m) => (state.masterId = m.id)"
        />
      </div>
      <div class="stack">
        <BookingCalendar
          :selected-date="state.date"
          :min-date="today()"
          :slots="slots"
          :selected-slot="state.slot"
          :loading="slotsLoading"
          :disabled="!state.serviceId || !state.masterId"
          :empty-label="
            slotsError ||
            (state.serviceId && state.masterId
              ? t('booking.noSlots')
              : t('booking.selectServiceMaster'))
          "
          @update:date="state.date = $event"
          @select="(slot) => (state.slot = slot)"
        />
        <BookingForm :form="state.form" @update:form="(f) => (state.form = f)" />
        <BookingSummary
          :service="chosenService"
          :master="chosenMaster"
          :slot="state.slot"
          :slot-label="
            selectedSlotLabel
              ? `${selectedSlotLabel} • ${formatDateLabel(state.slot)}`
              : ''
          "
          :form="state.form"
          @confirm="confirmBooking"
        />
        <div v-if="toast" class="toast">{{ toast }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page {
  display: grid;
  gap: 1.25rem;
}

.top {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1rem;
  align-items: start;
}

.note {
  background: linear-gradient(135deg, #ffffff, #f8f4e8);
}

.grid-2 {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 1rem;
  align-items: start;
}

.stack {
  display: grid;
  gap: 1rem;
}

.error {
  color: #8a1a1a;
  font-weight: 600;
}

.toast {
  display: inline-flex;
  padding: 0.6rem 1rem;
  border-radius: 999px;
  background: rgba(232, 234, 108, 0.45);
  color: #2a2d12;
  font-weight: 600;
  width: fit-content;
}

@media (max-width: 768px) {
  .top {
    grid-template-columns: 1fr;
  }
  .grid-2 {
    grid-template-columns: 1fr;
  }
}
</style>
