import { createRouter, createWebHistory } from 'vue-router';
import CampaignList from '@/domains/campaign/views/CampaignList.vue';
import LoginForm from '@/domains/auth/LoginForm.vue';
import { useUserStore } from '@/domains/user/userStore';
import { useAuthStore } from '@/domains/auth';
import SettingsPage from '@/domains/user/views/SettingsPage.vue';
import SignupPage from '@/domains/user/views/SignupPage.vue';

const routes = [
  {
    path: '/',
    redirect: '/campaigns',
  },
  {
    path: '/campaigns',
    name: 'CampaignList',
    component: CampaignList,
    meta: { requiresAuth: true },
  },
  {
    path: '/settings',
    name: 'Settings',
    component: SettingsPage,
    meta: { requiresAuth: true },
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginForm,
  },
  {
    path: '/signup',
    name: 'Signup',
    component: SignupPage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to, _, next) => {
  if (to.path === '/logout') {
    const authStore = useAuthStore();
    await authStore.logout();

    next({ name: 'Login' });
    return;
  }
  if (to.meta.requiresAuth) {
    const userStore = useUserStore();
    try {
      await userStore.fetchMe();
      next();
    } catch {
      next({ name: 'Login' });
    }
  } else {
    next();
  }
});

export default router;
