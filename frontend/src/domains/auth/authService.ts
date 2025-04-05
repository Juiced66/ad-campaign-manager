import api from '@/shared/composables/useApi';
import type { Token } from './authTypes';

export async function login(email: string, password: string): Promise<Token> {
  const response = await api.post<Token>('/auth/login', { email, password });
  return response.data;
}

export async function logout(refreshTokenValue: string): Promise<{ success: boolean }> {
  try {
    await api.post('/auth/logout', { refresh_token: refreshTokenValue });
  } catch (err) {
    console.error("Logout API call failed:", err);
  } finally {
    return { success: true };
  }
}

export async function refreshToken(currentRefreshToken: string): Promise<Token> {
  const response = await api.post<Token>('/auth/refresh', {
    refresh_token: currentRefreshToken,
  });

  return response.data;
}