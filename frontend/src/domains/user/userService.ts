import api from '@/shared/composables/useApi';
import type {
  User,
  CreateUserPayload,
  UpdateUserPayload,
} from '@/domains/user/userTypes';

export async function me() {
  const { data: user } = await api.get<User>('/users/me');
  return user;
}

export async function signup(payload: CreateUserPayload) {
  const { data: user } = await api.post<User>('/users/', payload);
  return user;
}

export async function updateMe(payload: UpdateUserPayload) {
  const { data: user } = await api.put<User>('/users/me', payload);

  return user;
}
