import { defineStore } from 'pinia';
import { ref } from 'vue';

import {
  logout as apiLogout,
  login as apiLogin,
} from '@/domains/auth/authService.ts';
import { useUserStore } from '@/domains/user/userStore';
export const useAuthStore = defineStore(
  'auth',
  () => {
    const token = ref<string | undefined>();

    function setToken(t: string | undefined) {
      token.value = t;
    }

    async function login(email: string, password: string) {
      const token = await apiLogin(email, password);
      setToken(token);
    }

    async function logout() {
      const { setUser } = useUserStore();
      await apiLogout();
      setToken(undefined);
      setUser(undefined);
    }

    return {
      token,
      setToken,
      logout,
      login,
    };
  },
  {
    persist: {
      storage: localStorage,
    },
  }
);
