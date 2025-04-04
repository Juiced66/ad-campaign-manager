import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useCampaignFilters = defineStore(
  'campaignFilters',
  () => {
    const is_active = ref<string | null>(null);
    const start_date = ref<string | null>(null);
    const end_date = ref<string | null>(null);
    const page = ref(1);
    const limit = ref(10);

    function reset() {
      is_active.value = null;
      start_date.value = null;
      end_date.value = null;
      page.value = 1;
      limit.value = 10;
    }

    return { is_active, start_date, end_date, page, limit, reset };
  },
  {
    persist: true,
  }
);
