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
  const authStore = useAuthStore(); // Get stores
  const userStore = useUserStore();

  if (to.path === '/logout') {
    await authStore.logout(); 
    next({ name: 'Login' });
    return;
  }

  if (to.meta.requiresAuth) {
    if (!userStore.isAuthenticated || !authStore.token) {
       try {
         console.log('Route requires auth, fetching user...');
         await userStore.fetchMe();
         console.log('User fetch successful, proceeding.');
         next();
       } catch (error: any) {
          console.log('User fetch failed in guard, redirecting to login.', error?.response?.status);
           if (error?.response?.status === 401 || !authStore.refreshToken) {
               await authStore.logout();
               next({ name: 'Login' });
           } else {
               console.error("Unexpected error in router guard fetchMe:", error);
               next(false);
           }
       }
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;