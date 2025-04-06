import { defineStore } from 'pinia';
import { useToast } from 'vue-toastification';
import { ref } from 'vue';

import {
  logout as apiLogout,
  login as apiLogin,
  refreshToken as apiRefreshToken,
} from '@/domains/auth/authService.ts';
import { useUserStore } from '@/domains/user/userStore';

export const useAuthStore = defineStore(
  'auth',
  () => {
    const token = ref<string | undefined>();
    const refreshToken = ref<string | undefined>();
    const isRefreshing = ref(false);
    const toast = useToast();

    function setTokens(
      newAccessToken: string | undefined,
      newRefreshTokenValue: string | undefined
    ) {
      token.value = newAccessToken;
      refreshToken.value = newRefreshTokenValue;
      isRefreshing.value = false;
    }

    async function login(email: string, password: string) {
      const { access_token, refresh_token: new_refresh_token } = await apiLogin(
        email,
        password
      );
      setTokens(access_token, new_refresh_token);
      const userStore = useUserStore();
      await userStore.fetchMe();
      toast.success('Logged in successfully!');
    }

    async function logout() {
      const { setUser } = useUserStore();
      const currentRefreshToken = refreshToken.value;

      setTokens(undefined, undefined);
      setUser(undefined);

      if (currentRefreshToken) {
        try {
          await apiLogout(currentRefreshToken);
          console.log('Server-side token revoked.');
        } catch (e) {
          console.warn(
            'Server-side logout/revoke failed, tokens cleared locally.',
            e
          );
          toast.error('Logout failed on server, logged out locally.');
        }
      }
    }

    async function refreshAccessToken(): Promise<string | null> {
      if (!refreshToken.value) {
        await logout();
        return null;
      }
      if (isRefreshing.value) {
        return null;
      }

      isRefreshing.value = true;
      try {
        const {
          access_token: newAccessToken,
          refresh_token: newRefreshTokenValue,
        } = await apiRefreshToken(refreshToken.value);
        setTokens(newAccessToken, newRefreshTokenValue);
        return newAccessToken;
      } catch (error) {
        console.error('Token refresh failed:', error);
        toast.error('Your session expired. Please log in again.');
        await logout();
        return null;
      } finally {
        isRefreshing.value = false;
      }
    }

    return {
      // State
      token,
      refreshToken,
      isRefreshing,
      // Actions
      setTokens,
      logout,
      login,
      refreshAccessToken,
    };
  },
  {
    persist: {
      storage: localStorage,
    },
  }
);
