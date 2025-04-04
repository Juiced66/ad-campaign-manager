export interface Campaign {
  id: number;
  name: string;
  description?: string;
  start_date: string;
  end_date: string;
  budget: number;
  is_active: boolean;
}

export interface PaginatedCampaignResponse {
  items: Campaign[];
  total: number;
}

export interface CampaignFilters {
  is_active?: boolean | null;
  start_date?: string | null;
  end_date?: string | null;
  page?: number;
  limit?: number;
}
