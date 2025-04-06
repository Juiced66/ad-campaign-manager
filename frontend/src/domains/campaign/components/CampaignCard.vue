<template>
  <div class="bg-white shadow rounded-lg p-4">
    <div class="flex justify-between items-center mb-2">
      <h3 class="font-semibold text-gray-900">{{ campaign.name }}</h3>
      <span
        class="text-xs font-medium px-2 py-1 rounded-full"
        :class="{
          'bg-green-100 text-green-700': campaign.is_active,
          'bg-gray-100 text-gray-500': !campaign.is_active,
        }"
      >
        {{ campaign.is_active ? 'Active' : 'Paused' }}
      </span>
    </div>

    <p class="text-sm text-gray-600 mb-1">
      <strong>Description:</strong> {{ campaign.description }}
    </p>
    <p class="text-sm text-gray-600 mb-1">
      <strong>Budget:</strong> {{ campaign.budget }}€
    </p>
    <p class="text-sm text-gray-600 mb-1">
      <strong>Start:</strong> {{ formatDate(campaign.start_date) }}
    </p>
    <p class="text-sm text-gray-600">
      <strong>End:</strong> {{ formatDate(campaign.end_date) }}
    </p>

    <div class="flex justify-end gap-2 mt-4">
      <BaseSwitch
        :model-value="campaign.is_active"
        title="Toggle status"
        @update:model-value="() => onToggleStatus(campaign.id)"
      />
      <BaseButton
        category="icon"
        variant="link"
        title="Edit"
        @click="$emit('edit', campaign)"
        ><FontAwesomeIcon :icon="['fas', 'pencil-alt']"
      /></BaseButton>
      <BaseButton
        category="icon"
        variant="link"
        title="Duplicate"
        @click="$emit('duplicate', campaign)"
        ><FontAwesomeIcon :icon="['fas', 'copy']"
      /></BaseButton>
      <BaseButton
        category="icon"
        variant="link"
        title="Delete"
        @click="$emit('delete', campaign.id)"
        ><FontAwesomeIcon :icon="['fas', 'trash-alt']"
      /></BaseButton>
    </div>
  </div>
</template>

<script setup lang="ts">
import { formatDate } from '@/shared/utils/formatters';
import type { Campaign } from '../campaignTypes';
import BaseSwitch from '@/shared/components/BaseSwitch.vue';
import BaseButton from '@/shared/components/BaseButton.vue';
import { useCampaignStore } from '../campaignStore';
// Props
interface Props {
  campaign: Campaign;
}

defineProps<Props>();

// Emits
const emit = defineEmits<{
  (e: 'edit', campaign: Campaign): void;
  (e: 'duplicate', campaign: Campaign): void;
  (e: 'delete', id: number): void;
  (e: 'toggle'): void;
}>();

// Stores
const campaignStore = useCampaignStore();

// Functions
function onToggleStatus(id: number): void {
  campaignStore.toggle(id);
  emit('toggle');
}
</script>
