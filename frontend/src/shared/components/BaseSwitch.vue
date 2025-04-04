<template>
  <button
    title="Toggle status"
    :class="[
      'relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2',
      modelValue ? 'bg-blue-600' : 'bg-gray-300',
    ]"
    @click="toggle"
  >
    <span
      :class="[
        'inline-block h-4 w-4 transform rounded-full bg-white transition-transform',
        modelValue ? 'translate-x-6' : 'translate-x-1',
      ]"
    />
  </button>
</template>

<script setup>
import { computed } from 'vue';
// Props
const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
});

// Emits
const emit = defineEmits(['update:modelValue']);

// Computeds
const isOn = computed(() => props.modelValue);

// Functions
function toggle() {
  emit('update:modelValue', !props.modelValue);
}

</script>
