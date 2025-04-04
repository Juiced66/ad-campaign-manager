<template>
  <div class="bg-white p-4 rounded-xl shadow-sm flex flex-wrap items-end gap-4">
    <div class="w-full sm:w-40">
      <label class="text-sm font-medium text-gray-700 mb-1 block">Status</label>
      <select
        v-model="filters.is_active"
        class="px-3 py-2 border rounded-md shadow-sm w-full focus:outline-none focus:ring-2 focus:ring-indigo-500"
      >
        <option :value="null">All</option>
        <option value="true">Active</option>
        <option value="false">Paused</option>
      </select>
    </div>

    <BaseInput
      id="start-date"
      v-model="filters.start_date"
      label="Start Date"
      type="date"
      class="w-full sm:w-48"
    />
    <BaseInput
      id="end-date"
      v-model="filters.end_date"
      label="End Date"
      type="date"
      class="w-full sm:w-48"
    />

    <BaseButton
      class="mb-2"
      variant="primary"
      category="pill"
      @click="$emit('reset')"
      >Reset</BaseButton
    >
  </div>
</template>

<script setup lang="ts">
import BaseInput from '@/shared/components/BaseInput.vue';
import BaseButton from '@/shared/components/BaseButton.vue';
import { useCampaignFilters } from '@/domains/campaign/campaignFiltersStore';
// Emits
const emit = defineEmits(['reset']);

// Stores
const filters = useCampaignFilters();
</script>
