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
    <td class="px-6 py-4 text-right space-x-2 flex flex-nowrap">
      <BaseSwitch
        :model-value="campaign.is_active"
        @update:model-value="() => onToggleStatus(campaign.id)"
      />
      <BaseButton
        category="icon"
        variant="link"
        title="edit"
        @click="$emit('edit', campaign)"
        >✏️</BaseButton
      >
      <BaseButton
        category="icon"
        variant="link"
        title="Duplicate"
        @click="$emit('duplicate', campaign)"
        >🗐</BaseButton
      >
      <BaseButton
        category="icon"
        variant="link"
        title="Delete"
        @click="$emit('delete', campaign.id)"
        >🗑️</BaseButton
      >
    </td>
  </tr>
</template>

<script setup lang="ts">
import { formatDate } from '@/shared/utils/formatters';
import type { Campaign } from '@/domains/campaign/campaignTypes';
import BaseSwitch from '@/shared/components/BaseSwitch.vue';
import BaseButton from '@/shared/components/BaseButton.vue';
import { useCampaignStore } from '@/domains/campaign/campaignStore';
// Props
defineProps<{ campaign: Campaign }>();

// Emits
const emit = defineEmits(['edit', 'duplicate', 'delete', 'toggle']);

// Stores
const campaignStore = useCampaignStore();

// Functions
function onToggleStatus(id: number): void {
  campaignStore.toggle(id);
  emit('toggle');
}
</script>
