import api from '@/shared/composables/useApi';
import type { Campaign, PaginatedCampaignResponse } from './campaignTypes';

const API = '/campaigns';

export async function fetchCampaigns(params?: {
  is_active?: boolean | null;
  start_date?: string | null;
  end_date?: string | null;
  page?: number;
  limit?: number;
}): Promise<PaginatedCampaignResponse> {
  const queryParams = new URLSearchParams();

  const page = params?.page ?? 1;
  const limit = params?.limit ?? 10;
  const skip = (page - 1) * limit;

  queryParams.set('skip', skip.toString());
  queryParams.set('limit', limit.toString());

  if (params?.is_active !== null && params?.is_active !== undefined) {
    queryParams.set('is_active', String(params.is_active));
  }
  if (params?.start_date) {
    queryParams.set('start_date', params.start_date);
  }
  if (params?.end_date) {
    queryParams.set('end_date', params.end_date);
  }

  const response = await api.get(`/campaigns?${queryParams.toString()}`);
  return response.data;
}

export async function createCampaign(
  payload: Partial<Campaign>
): Promise<Campaign> {
  const { data: campaign } = await api.post(API, payload);
  return campaign;
}

export async function updateCampaign(
  id: number,
  payload: Partial<Campaign>
): Promise<Campaign> {
  const { data: campaign } = await api.put(`${API}/${id}`, payload);
  return campaign;
}

export async function deleteCampaign(id: number): Promise<void> {
  await api.delete(`${API}/${id}`);
}

export async function toggleCampaign(
  id: number,
  currentStatus: boolean
): Promise<Campaign> {
  return updateCampaign(id, { is_active: !currentStatus });
}
