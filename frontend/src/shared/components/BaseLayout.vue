<template>
  <div class="flex h-screen bg-gray-50 text-gray-800">
    <!-- Overlay for mobile when sidebar is open -->
    <div
      v-if="sidebarOpen"
      class="fixed inset-0 bg-transparent bg-opacity-30 z-40 sm:hidden"
      @click="sidebarOpen = false"
    />

    <!-- Sidebar -->
    <aside
      :class="[
        'bg-gray-100 z-50 flex-col p-6 transition-transform duration-300 ease-in-out sm:static sm:translate-x-0 sm:flex',
        'fixed h-full w-64',
        sidebarOpen ? 'translate-x-0' : '-translate-x-full',
      ]"
    >
      <!-- Close button for mobile -->
      <div class="sm:hidden flex justify-end mb-4">
        <button
          class="text-2xl focus:outline-none"
          @click="sidebarOpen = false"
        >
          ✕
        </button>
      </div>

      <!-- Logo + Title -->
      <div class="flex items-center justify-between mb-6">
        <img
          src="@/assets/svg_adpulse.svg"
          alt="AdPulse Logo"
          class="h-16 w-16"
        />
        <h3 class="text-xl font-semibold">AdPulse</h3>
      </div>

      <!-- Nav links -->
      <nav v-if="isAuthenticated" class="flex-1 space-y-2">
        <RouterLink
          to="/campaigns"
          class="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-200 transition"
          @click="sidebarOpen = false"
        >
          <FontAwesomeIcon :icon="['fas', 'table']" /> <span>Campaigns</span>
        </RouterLink>
        <RouterLink
          to="/settings"
          class="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-200 transition"
          @click="sidebarOpen = false"
        >
          <FontAwesomeIcon :icon="['fas', 'cog']" /> <span>Settings</span>
        </RouterLink>
        <RouterLink
          to="/logout"
          class="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-200 transition"
          @click="sidebarOpen = false"
        >
          <FontAwesomeIcon :icon="['fas', 'sign-out-alt']" />
          <span>Logout</span>
        </RouterLink>
      </nav>
    </aside>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col min-h-full">
      <!-- Topbar for mobile -->
      <header
        class="sm:hidden flex items-center justify-between bg-white px-4 py-3 border-b"
      >
        <button
          v-if="isAuthenticated"
          class="text-2xl"
          @click="sidebarOpen = true"
        >
          ☰
        </button>
        <div class="ml-2 w-full flex gap-2">
          <img
            src="@/assets/svg_adpulse.svg"
            alt="AdPulse Logo"
            class="h-8 w-8"
          />
          <h1 class="text-lg font-semibold">AdPulse</h1>
          <div class="w-8"></div>
        </div>
      </header>

      <!-- Page content -->
      <main class="flex-1 overflow-y-auto px-4 py-4 sm:px-6 sm:py-6">
        <slot />
      </main>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref } from 'vue';
import { storeToRefs } from 'pinia';

import { useUserStore } from '@/domains/user/userStore';

// Stores
const userStore = useUserStore();

// Refs
const { isAuthenticated } = storeToRefs(userStore);
const sidebarOpen = ref(false);
</script>
