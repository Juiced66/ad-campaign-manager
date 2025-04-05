<template>
  <div class="flex flex-col gap-1">
    <label v-if="label" :for="id" class="text-sm font-medium text-gray-700">
      {{ label }}
    </label>

    <input
      :id="id"
      v-bind="$attrs"
      v-model="internalValue"
      :type="type"
      class="px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 disabled:opacity-50"
    />

    <p v-if="error" class="text-sm text-red-500 mt-1">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

// Props
const props = defineProps<{
  id?: string;
  label?: string;
  error?: string;
  modelValue?: string | number | null;
  type?: string;
}>();

// Emits
const emit = defineEmits(['update:modelValue']);

// Computeds
const internalValue = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val),
});
</script>
