import { useAuthStore } from '@/domains/auth/authStore';
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
});

api.interceptors.request.use((config) => {
  const { token } = useAuthStore();

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

export default api;
