<template>
  <form class="space-y-4 opacity-100" @submit.prevent="handleSubmit">
    <BaseInput
      v-for="field in inputFields"
      :id="field.id"
      :key="field.id"
      v-model="form[field.model]"
      :label="field.label"
      :type="field.type"
      :error="errors[field.errorField ?? field.model]"
    />

    <div class="flex justify-end gap-2 pt-4">
      <BaseButton type="button" variant="secondary" @click="handleCancel">
        Cancel
      </BaseButton>
      <BaseButton type="submit" :loading="isSubmitting">
        {{ form.id ? 'Update' : 'Create' }}
      </BaseButton>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref, watchEffect } from 'vue';
import BaseInput from '@/shared/components/BaseInput.vue';
import BaseButton from '@/shared/components/BaseButton.vue';
import { useCampaignStore } from '@/domains/campaign/campaignStore.ts';
import type { Campaign } from '@/domains/campaign/campaignTypes.ts';

// Types
type CampaignField = keyof Campaign;

type FieldConfig = {
  id: string;
  label: string;
  model: CampaignField;
  type?: string;
  errorField?: CampaignField;
};

// Constants
const BASE_FORM_VALUE: Partial<Campaign> = {
  id: undefined,
  name: '',
  description: '',
  start_date: '',
  end_date: '',
  budget: 0,
};

// Props
interface Props {
  campaign?: Campaign | Partial<Campaign> | null;
}

const props = defineProps<Props>();

// Emits
const emit = defineEmits<{
  (e: 'success'): void;
  (e: 'cancel'): void;
}>();

// Constants
const inputFields: FieldConfig[] = [
  { id: 'name', label: 'Name', model: 'name' },
  { id: 'description', label: 'Description', model: 'description' },
  { id: 'start-date', label: 'Start Date', model: 'start_date', type: 'date' },
  { id: 'end-date', label: 'End Date', model: 'end_date', type: 'date' },
  { id: 'budget', label: 'Budget (€)', model: 'budget', type: 'number' },
];

// Stores
const campaignStore = useCampaignStore();

// Refs
const isSubmitting = ref(false);
const form = ref<Partial<Record<CampaignField, any>>>({ ...BASE_FORM_VALUE });
const errors = ref<Partial<Record<CampaignField, string>>>({});

// Watchers
watchEffect(() => {
  if (props.campaign) {
    form.value = { ...props.campaign };
  }
});

// Functions
function validate(): boolean {
  errors.value = {};

  if (!form.value.name) errors.value.name = 'Name is required';
  if (!form.value.start_date)
    errors.value.start_date = 'Start date is required';
  if (!form.value.end_date) errors.value.end_date = 'End date is required';
  if (
    form.value.start_date &&
    form.value.end_date &&
    form.value.end_date < form.value.start_date
  ) {
    errors.value.end_date = 'End date must be after start date';
  }
  if (!form.value.budget || Number(form.value.budget) <= 0) {
    errors.value.budget = 'Budget must be positive';
  }

  return Object.keys(errors.value).length === 0;
}

function resetForm() {
  form.value = { ...BASE_FORM_VALUE };
}

async function handleSubmit() {
  if (!validate()) return;
  isSubmitting.value = true;

  try {
    if (form.value.id !== undefined) {
      await campaignStore.update(form.value.id, form.value);
    } else {
      await campaignStore.create(form.value);
    }
    resetForm();
    emit('success');
  } finally {
    isSubmitting.value = false;
  }
}

function handleCancel() {
  resetForm();
  emit('cancel');
}
</script>
