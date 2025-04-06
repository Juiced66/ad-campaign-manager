import { useAuthStore } from '@/domains/auth/authStore';
import axios, { type InternalAxiosRequestConfig } from 'axios'; // Import specific types

let isRefreshing = false;
/* eslint-disable  @typescript-eslint/no-explicit-any */
let failedQueue: {
  resolve: (value: any) => void;
  reject: (reason?: any) => void;
}[] = [];
const processQueue = (error: any, token: string | null = null) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  failedQueue = [];
};

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
});

// --- Request Interceptor ---
api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore();
    const token = authStore.token;

    const noAuthUrls = ['/auth/login', '/auth/refresh'];
    if (token && !noAuthUrls.some((url) => config.url?.includes(url))) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// --- Response Interceptor ---
api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & {
      _retry?: boolean;
    }; // Type assertion
    const authStore = useAuthStore();

    if (
      error.response?.status === 401 &&
      originalRequest.url !== '/auth/refresh'
    ) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        })
          .then((newToken) => {
            if (newToken) {
              originalRequest.headers['Authorization'] = `Bearer ${newToken}`;
              return api(originalRequest);
            }
            return Promise.reject(error);
          })
          .catch((err) => {
            return Promise.reject(err);
          });
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        const newAccessToken = await authStore.refreshAccessToken();

        if (newAccessToken) {
          console.log(
            'Refresh successful, retrying original request and processing queue.'
          );
          api.defaults.headers.common['Authorization'] =
            `Bearer ${newAccessToken}`;
          originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;
          processQueue(null, newAccessToken);
          return api(originalRequest);
        } else {
          console.log(
            'Refresh failed (or user logged out during refresh), rejecting original request.'
          );
          processQueue(error, null);
          return Promise.reject(error);
        }
      } catch (refreshError) {
        console.error('Caught error during refresh process:', refreshError);
        processQueue(refreshError, null);
        await authStore.logout();
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }
    return Promise.reject(error);
  }
);

export default api;
