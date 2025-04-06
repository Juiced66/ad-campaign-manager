<template>
  <button
    title="Toggle status"
    :class="[
      'relative inline-flex h-5 w-9 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2',
      modelValue ? 'bg-blue-600' : 'bg-gray-300',
    ]"
    @click="toggle"
  >
    <span
      :class="[
        'inline-block h-3 w-3 transform rounded-full bg-white transition-transform',
        modelValue ? 'translate-x-5' : 'translate-x-1',
      ]"
    />
  </button>
</template>

<script setup lang="ts">
// Props
interface Props {
  modelValue: boolean;
}

const props = defineProps<Props>();

// Emits
const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void;
}>();

// Functions
function toggle() {
  emit('update:modelValue', !props.modelValue);
}
</script>
