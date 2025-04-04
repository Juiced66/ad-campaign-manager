<template>
  <div class="max-w-lg mx-auto sm:mt-40 mt-20">
    <h1 class="text-2xl font-semibold mb-6">Profile creation</h1>
    <UserForm
      :loading="creating"
      submit-text="Create account"
      loading-text="Creating..."
      @submit="($event) => signup($event as CreateUserPayload)"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

import { useUserStore } from '@/domains/user/userStore';
import type { CreateUserPayload } from '@/domains/user/userTypes';
import UserForm from '@/shared/components/UserForm.vue';

// Stores
const userStore = useUserStore();

// Refs
const creating = ref(false);

// Composables
const router = useRouter();

// Functions
async function signup({ email, password }: CreateUserPayload) {
  creating.value = true;
  try {
    await userStore.signup({ email, password });
    router.push({ name: 'CampaignList' });
  } catch (e) {
    console.error('Error while creating user: ', e);
  } finally {
    creating.value = false;
  }
}
</script>
