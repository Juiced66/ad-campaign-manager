import { defineStore } from 'pinia';
import { useToast } from 'vue-toastification';
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
  const toast = useToast();

  function setUser(u: User | undefined) {
    user.value = u;
  }

  async function signup(payload: CreateUserPayload) {
    try {
      await apiSignup(payload);
      const authStore = useAuthStore();
      await authStore.login(payload.email, payload.password);
      toast.success('Account created successfully!');
    } catch (err) {
      console.error('Signup failed:', err);
      toast.error('Failed to create account.');
      throw err;
    }
  }

  async function fetchMe() {
    loading.value = true;
    try {
      const fetchedUser = await apiMe();
      setUser(fetchedUser);
    } catch (err) {
      console.error('Failed to fetch user details:', err);
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function updateMe(payload: Partial<User> & { password?: string }) {
    loading.value = true;
    try {
      const u = await apiUpdateMe(payload);
      user.value = u;
      toast.success('Profile updated successfully!');
    } catch (err) {
      console.error('Failed to update profile:', err);
      toast.error('Failed to update profile.');
      throw err;
    } finally {
      loading.value = false;
    }
  }

  const isAuthenticated = computed(() => {
    return !!user.value;
  });
  return {
    // State
    user,
    loading,
    isAuthenticated,
    // Actions
    fetchMe,
    updateMe,
    setUser,
    signup,
  };
});
