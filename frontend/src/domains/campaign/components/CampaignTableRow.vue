<template>
  <tr class="hover:bg-gray-50">
    <td class="px-6 py-4 font-medium text-gray-900">{{ campaign.name }}</td>
    <td>{{ campaign.description }}</td>
    <td class="px-6 py-4">
      <span
        class="inline-block text-xs font-semibold px-2 py-1 rounded-full"
        :class="{
          'bg-green-100 text-green-700': campaign.is_active,
          'bg-gray-100 text-gray-500': !campaign.is_active,
        }"
      >
        {{ campaign.is_active ? 'Active' : 'Paused' }}
      </span>
    </td>
    <td class="px-6 py-4 text-right">{{ campaign.budget }}€</td>
    <td class="px-6 py-4 text-right">{{ formatDate(campaign.start_date) }}</td>
    <td class="px-6 py-4 text-right">{{ formatDate(campaign.end_date) }}</td>
    <td class="px-6 py-4 ml-auto text-right">
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
      <BaseSwitch
        :model-value="campaign.is_active"
        @update:model-value="() => onToggleStatus(campaign.id)"
      />
    </td>
  </tr>
</template>

<script setup lang="ts">
import type { Campaign } from '@/domains/campaign/campaignTypes';
import { useCampaignStore } from '@/domains/campaign/campaignStore';
import { formatDate } from '@/shared/utils/formatters';

import BaseButton from '@/shared/components/BaseButton.vue';
import BaseSwitch from '@/shared/components/BaseSwitch.vue';
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
