<template>
  <form class="space-y-6" @submit.prevent="onSubmit">
    <BaseInput id="email" v-model="form.email" label="Email" type="email" />

    <BaseInput
      id="new-password"
      v-model="form.password"
      label="Password"
      type="password"
    />
    <BaseInput
      id="confirm-password"
      v-model="form.confirmPassword"
      label="Confirm Password"
      type="password"
    />

    <p v-if="error" class="text-sm text-red-500">{{ error }}</p>

    <BaseButton category="pill" :disabled="loading" type="submit">
      {{ loading ? loadingText : submitText }}
    </BaseButton>
  </form>
</template>

<script setup lang="ts">
import { reactive, ref, watch } from 'vue';

import BaseButton from '@/shared/components/BaseButton.vue';
import BaseInput from '@/shared/components/BaseInput.vue';

// Types
interface Props {
  modelValue?: {
    email?: string;
  };
  submitText?: string;
  loadingText?: string;
  loading?: boolean;
}

// Props
const props = defineProps<Props>();

// Emits
const emit = defineEmits<{
  (e: 'submit', data: { email: string; password?: string }): void;
}>();

// Refs
const form = reactive({
  email: props.modelValue?.email || '',
  password: '',
  confirmPassword: '',
});
const error = ref('');

// Watchers
watch(
  () => props.modelValue,
  (val) => {
    if (val?.email) form.email = val.email;
  }
);

// Functions
function onSubmit() {
  error.value = '';
  if (form.password && form.password !== form.confirmPassword) {
    error.value = 'Passwords do not match.';
    return;
  }

  emit('submit', {
    email: form.email,
    password: form.password || undefined,
  });
}
</script>
