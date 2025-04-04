<template>
  <div class="space-y-6 mt-10 px-5">
    <h1 class="text-2xl font-bold">Campaigns</h1>
    <CampaignTable />
  </div>
</template>

<script setup lang="ts">
import CampaignTable from '@/domains/campaign/components/CampaingTable.vue';
</script>
