import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { Campaign, CampaignFilters } from './campaignTypes';
import {
  fetchCampaigns,
  createCampaign,
  updateCampaign,
  deleteCampaign,
  toggleCampaign,
} from './campaignService';

export const useCampaignStore = defineStore('campaigns', () => {
  const campaigns = ref<Campaign[]>([]);
  const total = ref(0);
  const loading = ref(true);

  async function load(filters: CampaignFilters) {
    loading.value = true;
    try {
      const res = await fetchCampaigns(filters);
      campaigns.value = res.items;
      total.value = res.total;
    } finally {
      loading.value = false;
    }
  }

  async function create(payload: Partial<Campaign>) {
    loading.value = true;
    try {
      const created = await createCampaign(payload);
      campaigns.value.push(created);
    } catch (e) {
      console.error('Failed to create campaign:', e);
    } finally {
      loading.value = false;
    }
  }

  async function update(id: number, payload: Partial<Campaign>) {
    loading.value = true;
    try {
      const updated = await updateCampaign(id, payload);
      const index = campaigns.value.findIndex((c) => c.id === id);
      if (index !== -1) campaigns.value[index] = updated;
    } catch (e) {
      console.error(`Failed to update campaign with id ${id}:`, e);
    } finally {
      loading.value = false;
    }
  }

  async function remove(id: number) {
    loading.value = true;
    try {
      await deleteCampaign(id);
      campaigns.value = campaigns.value.filter((c) => c.id !== id);
    } catch (e) {
      console.error(`Failed to delete campaign with id ${id}:`, e);
    } finally {
      loading.value = false;
    }
  }

  async function toggle(id: number) {
    loading.value = true;
    try {
      const campaign = campaigns.value.find((c) => c.id === id);
      if (!campaign) return;
      const updated = await toggleCampaign(id, campaign.is_active);
      campaign.is_active = updated.is_active;
    } catch (e) {
      console.error(`Failed to toggle campaign with id ${id}:`, e);
    } finally {
      loading.value = false;
    }
  }

  return { campaigns, loading, total, load, create, update, remove, toggle };
});
