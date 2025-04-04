<template>
  <div class="space-y-4">
    <div class="flex justify-end">
      <BaseButton category="default" @click="modalActive = true">
        Create campaign
      </BaseButton>
    </div>

    <!-- Filters -->
    <CampaignFilters @reset="resetFilters" />

    <!-- Table view for sm and up -->
    <div class="hidden sm:block overflow-x-auto rounded-xl shadow-sm bg-white">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50 text-left text-sm text-gray-500">
          <tr>
            <th class="px-6 py-3 text-left">Name</th>
            <th class="px-6 py-3 text-left">Description</th>
            <th class="px-6 py-3 text-left">Status</th>
            <th class="px-6 py-3 text-right">Budget</th>
            <th class="px-6 py-3 text-right">Start Date</th>
            <th class="px-6 py-3 text-right">End Date</th>
            <th class="px-6 py-3 text-right">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100 text-sm">
          <CampaignTableRow
            v-for="campaign in campaigns"
            :key="campaign.id"
            :campaign="campaign"
            @delete="campaignStore.remove"
            @edit="onClickUpdate"
            @duplicate="onClickDuplicate"
            @toggle="loadWithFilters"
          />
        </tbody>
      </table>
    </div>

    <!-- Card view for mobile -->
    <div class="sm:hidden space-y-4">
      <CampaignCard
        v-for="campaign in campaigns"
        :key="campaign.id"
        :campaign="campaign"
        @edit="onClickUpdate"
        @duplicate="onClickDuplicate"
        @delete="campaignStore.remove"
        @toggle="loadWithFilters"
      />
    </div>

    <div
      v-if="!loading && !campaigns.length"
      class="text-center text-sm text-gray-500"
    >
      No campaigns found
    </div>
    <div v-else-if="loading" class="text-center text-sm">Loading ...</div>

    <!-- Pagination -->
    <BasePagination
      v-model:page="filtersStore.page"
      v-model:limit="filtersStore.limit"
      :total="total"
      :disable-next="disableNext"
      @update:page="onPageChange"
      @update:limit="onLimitChange"
    />

    <!-- Modal -->
    <BaseModal v-model="modalActive" @close="closeModal">
      <CampaignForm
        :campaign="selectedCampaign"
        @success="handleSuccess"
        @cancel="closeModal"
      />
    </BaseModal>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue';
import { storeToRefs } from 'pinia';

import BaseButton from '@/shared/components/BaseButton.vue';
import BaseModal from '@/shared/components/BaseModal.vue';
import BasePagination from '@/shared/components/BasePagination.vue';

import { useCampaignStore } from '@/domains/campaign/campaignStore';
import { useCampaignFilters } from '@/domains/campaign/campaignFiltersStore';
import type { Campaign } from '@/domains/campaign/campaignTypes';

import CampaignFilters from '@/domains/campaign/components/CampaignFilters.vue';
import CampaignForm from '@/domains/campaign/components/CampaignForm.vue';
import CampaignCard from '@/domains/campaign/components/CampaignCard.vue';
import CampaignTableRow from '@/domains/campaign/components/CampaignTableRow.vue';

// Stores
const campaignStore = useCampaignStore();
const filtersStore = useCampaignFilters();

// Refs
const { campaigns, loading, total } = storeToRefs(campaignStore);
const modalActive = ref(false);
const selectedCampaign = ref<Campaign | Partial<Campaign> | null>(null);

// Computeds
const maxPage = computed(() => Math.ceil(total.value / filtersStore.limit));
const disableNext = computed(() => filtersStore.page >= maxPage.value);

// Watchers
watch(
  () => [
    filtersStore.is_active,
    filtersStore.start_date,
    filtersStore.end_date,
    filtersStore.limit,
  ],
  () => {
    filtersStore.page = 1;
    loadWithFilters();
  }
);

watch(
  () => filtersStore.page,
  () => {
    loadWithFilters();
  }
);

// Hooks
onMounted(() => {
  loadWithFilters();
});

// Functions
async function loadWithFilters() {
  await campaignStore.load({
    is_active:
      filtersStore.is_active === 'true'
        ? true
        : filtersStore.is_active === 'false'
          ? false
          : null,
    start_date: filtersStore.start_date,
    end_date: filtersStore.end_date,
    page: filtersStore.page,
    limit: filtersStore.limit,
  });
}

function resetFilters() {
  filtersStore.reset();
  loadWithFilters();
}

function onClickUpdate(campaign: Campaign) {
  selectedCampaign.value = campaign;
  modalActive.value = true;
}

function onClickDuplicate(campaign: Campaign) {
  const duplicateCampaign = { ...campaign, id: undefined };
  selectedCampaign.value = duplicateCampaign;
  modalActive.value = true;
}

function closeModal() {
  modalActive.value = false;
  selectedCampaign.value = null;
}

function handleSuccess() {
  closeModal();
  total.value++;
}

function onPageChange(page: number) {
  filtersStore.page = page;
  loadWithFilters();
}

function onLimitChange(limit: number) {
  filtersStore.limit = limit;
  filtersStore.page = 1;
  loadWithFilters();
}
</script>
