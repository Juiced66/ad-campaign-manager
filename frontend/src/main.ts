import { library } from '@fortawesome/fontawesome-svg-core';
import {
  faTable,
  faPencilAlt,
  faCopy,
  faTrashAlt,
  faCog,
  faSignOutAlt,
} from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { createPinia } from 'pinia';
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';
import Toast, { type PluginOptions, POSITION } from 'vue-toastification';
import { createApp } from 'vue';

import App from '@/app/App.vue';
import router from '@/router';

import './app/style.css';
import 'vue-toastification/dist/index.css';

const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);

library.add(faTable, faPencilAlt, faCopy, faTrashAlt, faCog, faSignOutAlt);

const toastOptions: PluginOptions = {
  position: POSITION.TOP_RIGHT,
  timeout: 3000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: false,
  hideProgressBar: false,
  closeButton: 'button',
  icon: true,
  rtl: false,
};

const app = createApp(App);
app.component('FontAwesomeIcon', FontAwesomeIcon);
app.use(Toast, toastOptions);
app.use(pinia);
app.use(router);
app.mount('#app');
