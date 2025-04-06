import { defineStore } from 'pinia';
import { useToast } from 'vue-toastification';
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
  const toast = useToast();

  async function load(filters: CampaignFilters) {
    loading.value = true;
    try {
      const res = await fetchCampaigns(filters);
      campaigns.value = res.items;
      total.value = res.total;
    } catch (err) {
      console.error('Failed to load campaigns:', err);
      toast.error('Failed to load campaigns.');
    } finally {
      loading.value = false;
    }
  }

  async function create(payload: Partial<Campaign>) {
    loading.value = true;
    try {
      const created = await createCampaign(payload);
      campaigns.value.push(created);
      toast.success('Campaign created successfully!');
    } catch (e) {
      console.error('Failed to create campaign:', e);
      toast.error('Failed to create campaign.');
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
      toast.success('Campaign updated successfully!');
    } catch (e) {
      console.error(`Failed to update campaign with id ${id}:`, e);
      toast.error('Failed to update campaign.');
    } finally {
      loading.value = false;
    }
  }

  async function remove(id: number) {
    loading.value = true;
    try {
      await deleteCampaign(id);
      campaigns.value = campaigns.value.filter((c) => c.id !== id);
      toast.success('Campaign deleted successfully!');
    } catch (e) {
      console.error(`Failed to delete campaign with id ${id}:`, e);
      toast.error('Failed to delete campaign.');
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
      toast.success(`Campaign ${updated.is_active ? 'activated' : 'paused'}!`);
    } catch (e) {
      console.error(`Failed to toggle campaign with id ${id}:`, e);
      toast.error('Failed to update campaign status.');
    } finally {
      loading.value = false;
    }
  }

  return {
    // State
    campaigns,
    loading,
    total,
    // Actions
    load,
    create,
    update,
    remove,
    toggle,
  };
});
