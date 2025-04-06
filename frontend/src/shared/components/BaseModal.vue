<template>
  <Teleport to="body">
    <Transition name="fade">
      <div
        v-if="modelValue"
        class="fixed inset-0 z-50 flex items-center justify-center"
        @keydown.esc="$emit('close')"
      >
        <div class="absolute inset-0 bg-white opacity-45"></div>
        <div
          ref="modalRef"
          class="bg-white rounded-xl shadow-lg max-w-lg w-full p-6 relative"
          role="dialog"
          aria-modal="true"
        >
          <button
            class="absolute top-4 right-4 text-gray-400 hover:text-black"
            aria-label="Close modal"
            @click="$emit('close')"
          >
            &times;
          </button>
          <div class="bg-white opacity-100">
            <slot />
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue';

// Props
interface Props {
  modelValue: boolean;
}

const props = defineProps<Props>();

// Emits
defineEmits<{
  (e: 'update:modelValue', value: boolean): void; // Although not emitted directly, good practice
  (e: 'close'): void;
}>();

// Refs
const modalRef = ref<HTMLElement | null>(null);

// Watchers
watch(
  () => props.modelValue,
  (open) => {
    if (open) document.body.style.overflow = 'hidden';
    else document.body.style.overflow = '';
  }
);

// Hooks
onMounted(() => {
  if (modalRef.value) {
    modalRef.value.focus();
  }
});

onUnmounted(() => {
  document.body.style.overflow = '';
});
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
