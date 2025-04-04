import { defineStore } from 'pinia';
import { computed, ref } from 'vue';
import type { CreateUserPayload, User } from '@/domains/user/userTypes';
import { useAuthStore } from '../auth';
import {
  signup as apiSignup,
  me as apiMe,
  updateMe as apiUpdateMe,
} from '@/domains/user/userService';

export const useUserStore = defineStore('user', () => {
  const user = ref<User | undefined>();
  const loading = ref(false);

  function setUser(u: User | undefined) {
    user.value = u;
  }

  async function signup(payload: CreateUserPayload) {
    await apiSignup(payload);
    const authStore = useAuthStore();
    await authStore.login(payload.email, payload.password);
  }

  async function fetchMe() {
    loading.value = true;
    try {
      const user = await apiMe();
      setUser(user);
    } finally {
      loading.value = false;
    }
  }

  async function updateMe(payload: Partial<User> & { password?: string }) {
    const u = await apiUpdateMe(payload);
    user.value = u;
  }

  const isAuthenticated = computed(() => {
    return !!user.value;
  });
  return { user, loading, isAuthenticated, fetchMe, updateMe, setUser, signup };
});
