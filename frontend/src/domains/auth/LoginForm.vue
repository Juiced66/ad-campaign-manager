<template>
  <form
    class="max-w-sm mx-auto sm:mt-40 mt-20 bg-white p-6 rounded-md shadow-md space-y-4"
    @submit.prevent="submit"
  >
    <h2 class="text-xl font-semibold mb-2">Login</h2>

    <BaseInput
      id="email"
      v-model="form.email"
      label="Email"
      type="email"
      :error="errors.email"
    />
    <BaseInput
      id="password"
      v-model="form.password"
      label="Password"
      type="password"
      :error="errors.password"
    />

    <BaseButton :loading="loading" class="w-full">Log In</BaseButton>
    <div class="flex justify-between">
      <em> Not an AdPulse user yet ?</em>
      <BaseButton category="pill" @click="router.push({ name: 'Signup' })"
        >Signup</BaseButton
      >
    </div>
    <p v-if="errorMessage" class="text-red-600 text-sm mt-2 text-center">
      {{ errorMessage }}
    </p>
  </form>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/domains/auth/authStore.ts';
import BaseInput from '@/shared/components/BaseInput.vue';
import BaseButton from '@/shared/components/BaseButton.vue';

// Stores
const authStore = useAuthStore();

// Refs
const errors = ref<{ email?: string; password?: string }>({});
const errorMessage = ref('');
const form = ref({
  email: '',
  password: '',
});
const loading = ref(false);

// Composables
const router = useRouter();

// Functions
async function submit() {
  errors.value = {};
  errorMessage.value = '';

  if (!form.value.email) errors.value.email = 'Email required';
  if (!form.value.password) errors.value.password = 'Password required';
  if (Object.keys(errors.value).length) return;

  loading.value = true;
  try {
    await authStore.login(form.value.email, form.value.password);
    router.push('/campaigns');
  } catch (err: any) {
    console.error('Login failed:', err);
    if (err.response && err.response.status === 401) {
      errorMessage.value = 'Invalid credentials';
    } else {
      errorMessage.value = 'Login failed. Please try again.';
    }
  } finally {
    loading.value = false;
  }
}
</script>
