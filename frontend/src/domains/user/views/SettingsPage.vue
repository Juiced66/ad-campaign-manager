<template>
  <div class="max-w-lg mx-auto sm:mt-40 mt-20">
    <h1 class="text-2xl font-semibold mb-6">Profile Settings</h1>
    <UserForm
      :model-value="{ email }"
      :loading="saving"
      submit-text="Save Changes"
      loading-text="Saving..."
      @submit="save"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useUserStore } from '@/domains/user/userStore';
import UserForm from '@/shared/components/UserForm.vue';

// Stores
const userStore = useUserStore();

// Refs
const email = ref('');
const saving = ref(false);

// Hooks
onMounted(async () => {
  if (!userStore.user) {
    await userStore.fetchMe();
  }
  email.value = userStore.user?.email || '';
});

// Functions
async function save({
  email: newEmail,
  password,
}: {
  email: string;
  password?: string;
}) {
  saving.value = true;
  try {
    await userStore.updateMe({
      email: newEmail,
      password,
    });
  } catch (e) {
  } finally {
    saving.value = false;
  }
}
</script>
