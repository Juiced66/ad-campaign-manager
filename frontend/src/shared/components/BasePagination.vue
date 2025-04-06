<template>
  <div class="flex items-center justify-between gap-4 mt-4">
    <!-- Limit selector -->
    <div class="flex items-center gap-2 text-sm">
      <label for="limit" class="text-gray-600">Rows per page:</label>
      <select
        id="limit"
        class="border rounded px-2 py-1"
        :value="limit"
        @change="
          $emit('update:limit', +($event.target as HTMLSelectElement).value)
        "
      >
        <option :value="5">5</option>
        <option :value="10">10</option>
        <option :value="25">25</option>
        <option :value="50">50</option>
      </select>
      Total : {{ total }}
    </div>

    <!-- Pagination buttons -->
    <div class="flex items-center gap-2 text-sm">
      <BaseButton
        :disabled="page <= 1"
        category="pill"
        @click="$emit('update:page', page - 1)"
      >
        Prev
      </BaseButton>
      <span>Page {{ page }}</span>
      <BaseButton
        :disabled="disableNext"
        category="pill"
        @click="$emit('update:page', page + 1)"
      >
        Next
      </BaseButton>
    </div>
  </div>
</template>

<script setup lang="ts">
import BaseButton from './BaseButton.vue';
// Props
interface Props {
  page: number;
  limit: number;
  total: number;
  disableNext: boolean;
}

defineProps<Props>();

// Emits
defineEmits<{
  (e: 'update:page', value: number): void;
  (e: 'update:limit', value: number): void;
}>();
</script>
