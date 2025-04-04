import api from '@/shared/composables/useApi';

export async function login(email: string, password: string): Promise<string> {
  const response = await api.post('/auth/login', { email, password });
  return response.data.access_token;
}

export async function logout() {
  try {
    await api.post('/auth/logout');
  } catch {
    // silent fail
  } finally {
    return { success: true };
  }
}

// async function refresh() {
//   // TODO
// }