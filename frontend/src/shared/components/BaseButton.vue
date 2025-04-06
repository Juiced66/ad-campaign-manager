<template>
  <button
    :type="type"
    :disabled="disabled || loading"
    :class="buttonClasses"
    :title="title"
    class="inline-flex items-center justify-center transition focus:outline-none"
  >
    <svg
      v-if="loading"
      class="animate-spin h-4 w-4 text-white"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle
        class="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        stroke-width="4"
      />
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
    </svg>
    <slot />
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue';

// Props
interface Props {
  type?: 'button' | 'submit' | 'reset';
  variant?: 'primary' | 'secondary' | 'danger' | 'link';
  category?: 'default' | 'icon' | 'pill';
  title?: string;
  loading?: boolean;
  disabled?: boolean;
}

const props = defineProps<Props>();

// Computeds
const buttonClasses = computed(() => {
  const variant = props.variant ?? 'primary';
  const category = props.category ?? 'default';

  const base = {
    default: 'px-3 py-1.5 text-sm font-medium rounded-md gap-2',
    icon: 'p-1 text-sm rounded-full w-8 h-8 justify-center',
    pill: 'px-3 py-1 text-sm font-medium rounded-full',
  };

  const variantClasses: Record<string, string> = {
    primary: 'bg-indigo-600 hover:bg-indigo-700 text-white',
    secondary:
      'bg-gray-100 hover:bg-gray-200 text-gray-800 border border-gray-300',
    danger: 'bg-red-600 hover:bg-red-700 text-white',
    link: '',
  };

  const disabledStyle = 'opacity-50 cursor-not-allowed';

  return [
    'inline-flex items-center transition cursor-pointer',
    base[category],
    variantClasses[variant],
    props.disabled || props.loading ? disabledStyle : '',
    'focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500',
  ].join(' ');
});
</script>
