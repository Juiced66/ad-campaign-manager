/// <reference types="vitest" />
import { defineConfig } from 'vite';
import tailwindcss from '@tailwindcss/vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';

export default defineConfig({
  plugins: [tailwindcss(), vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  test: {
    globals: true,
    environment: 'jsdom',
    server: {
      deps: {
        inline: ['@vue', '@vueuse', 'vue-demi'],
      },
    },
    deps: {
      optimizer: {
        web: {
          include: ['@vue', '@vueuse', 'vue-demi'],
        },
      },
    },
  },
});