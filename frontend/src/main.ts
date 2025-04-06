import { library } from '@fortawesome/fontawesome-svg-core';
import {
    faTable,
    faPencilAlt,
    faCopy,
    faTrashAlt,
    faCog,
    faSignOutAlt
  } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { createPinia } from 'pinia';
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';

import { createApp } from 'vue';
import './app/style.css';
import App from '@/app/App.vue';
import router from '@/router';

const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);
library.add(faTable, faPencilAlt, faCopy, faTrashAlt, faCog, faSignOutAlt);

const app = createApp(App);
app.component('FontAwesomeIcon', FontAwesomeIcon);
app.use(pinia);
app.use(router);
app.mount('#app');
