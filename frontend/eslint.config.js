import eslintPluginVue from 'eslint-plugin-vue';
import * as tsParser from '@typescript-eslint/parser';
import tsPlugin from '@typescript-eslint/eslint-plugin';
import eslintConfigPrettier from 'eslint-config-prettier';
import globals from 'globals';

export default [
  // 1. Global Ignores (optional but good practice)
  {
    ignores: [
      'node_modules/',
      'dist/',
      '*.d.ts',
      'public/',
      '*.log',
      '*.lock',
      '*.yml',
      '*.md', 
      'vite.config.ts',
      'tailwind.config.js',
      'postcss.config.js',
      'eslint.config.js', 
      '.prettierrc.json',
      '.prettierignore',
      '**/*.spec.ts',   
      '**/*.test.ts', 
      '**/__tests__/', 
      '**/tests/',
      '**/*.d.ts',
      '**/.vite/**'
    ],
  },

  // 2. Base JS/TS Configuration (Applies to .js, .mjs, .cjs, .ts, .mts, .cts)
  {
    files: ['**/*.{js,mjs,cjs,ts,mts,cts}'],
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      parser: tsParser, // Use TS parser for all JS/TS files
      parserOptions: {
        ecmaFeatures: { jsx: false }, // Assuming no JSX in JS/TS files
      },
      globals: {
        ...globals.browser, // Browser globals like window, document
        ...globals.node, // Node.js globals like process, require
        ...globals.es2021, // ES2021 globals
      },
    },
    plugins: {
      '@typescript-eslint': tsPlugin,
    },
    rules: {
      ...tsPlugin.configs['eslint-recommended'].rules, // Base recommended rules adjusted for TS
      ...tsPlugin.configs.recommended.rules, // TS recommended rules
      // Your custom JS/TS rules
      'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
      'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
      '@typescript-eslint/no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
      // Add other JS/TS rules here
    },
  },

  // 3. Vue Configuration (Applies only to .vue files)
  // Uses eslint-plugin-vue's processor and rules
  ...eslintPluginVue.configs['flat/recommended'], // Use flat config version
  // Override Vue specific rules *after* applying the config
  {
     files: ['**/*.vue'],
     languageOptions: {
        // Ensure parser options for <script> are set if needed (usually inherited)
        parserOptions: {
          parser: tsParser, // Specify TS parser for <script lang="ts">
        },
        globals: {
          // Add setup-compiler-macros equivalents if needed, often handled by plugin
          defineProps: 'readonly',
          defineEmits: 'readonly',
          defineOptions: 'readonly',
          withDefaults: 'readonly',
        }
     },
     rules: {
        // Your custom Vue rules
        'vue/multi-word-component-names': 'warn', // Example: Warn instead of error
        'vue/no-unused-vars': 'warn',
        // You might need to disable the base TS rule for vars used only in template
        '@typescript-eslint/no-unused-vars': 'off',
     }
  },

  // 4. Prettier Configuration (Applies LAST to override formatting rules)
  eslintConfigPrettier, // This is the recommended way now
];