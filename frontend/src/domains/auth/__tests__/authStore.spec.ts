import { mount } from '@vue/test-utils';
import { createTestingPinia } from '@pinia/testing';
import { vi } from 'vitest';
import LoginForm from '../LoginForm.vue';
import BaseInput from '@/shared/components/BaseInput.vue';
import BaseButton from '@/shared/components/BaseButton.vue';
import { useAuthStore } from '../authStore';
import { nextTick } from 'vue';

const mockRouterPush = vi.fn();
vi.mock('vue-router', () => ({
  useRouter: () => ({
    push: mockRouterPush,
  }),
}));

describe('LoginForm.vue', () => {
  let pinia: any;
  let authStore: ReturnType<typeof useAuthStore>;

  beforeEach(() => {
    vi.clearAllMocks();
    pinia = createTestingPinia({
      stubActions: true,
      createSpy: vi.fn,
    });
    authStore = useAuthStore();
  });

  it('renders email, password inputs, and login button', () => {
    const wrapper = mount(LoginForm, {
      global: { plugins: [pinia] },
    });

    expect(wrapper.find('input#email[type="email"]').exists()).toBe(true);
    expect(wrapper.find('input#password[type="password"]').exists()).toBe(true);
    expect(wrapper.findComponent(BaseButton).text()).toBe('Log In');
    expect(wrapper.find('h2').text()).toBe('Login');
  });

  it('updates form data using v-model', async () => {
    const wrapper = mount(LoginForm, { global: { plugins: [pinia] } });

    const emailInput = wrapper.find('input#email');
    const passwordInput = wrapper.find('input#password');

    await emailInput.setValue('test@example.com');
    await passwordInput.setValue('password123');

    expect((wrapper.vm as any).form.email).toBe('test@example.com');
    expect((wrapper.vm as any).form.password).toBe('password123');
  });

  it('shows validation errors for empty fields on submit', async () => {
    const wrapper = mount(LoginForm, { global: { plugins: [pinia] } });

    await wrapper.find('form').trigger('submit.prevent');

    expect(authStore.login).not.toHaveBeenCalled();
    expect(mockRouterPush).not.toHaveBeenCalled();

    const errors = (wrapper.vm as any).errors;
    expect(errors.email).toBe('Email required');
    expect(errors.password).toBe('Password required');

    const emailInputWrapper = wrapper.findComponent(BaseInput);
    const passwordInputWrapper = wrapper.findAllComponents(BaseInput)[1];
    expect(emailInputWrapper.props('error')).toBe('Email required');
    expect(passwordInputWrapper.props('error')).toBe('Password required');
  });

  it('calls authStore.login action and navigates on successful submit', async () => {
    authStore.login = vi.fn().mockResolvedValue(undefined);

    const wrapper = mount(LoginForm, { global: { plugins: [pinia] } });

    const testEmail = 'good@user.com';
    const testPassword = 'correctpassword';

    await wrapper.find('input#email').setValue(testEmail);
    await wrapper.find('input#password').setValue(testPassword);

    await wrapper.find('form').trigger('submit.prevent');

    await vi.dynamicImportSettled();
    await nextTick();

    expect(authStore.login).toHaveBeenCalledTimes(1);
    expect(authStore.login).toHaveBeenCalledWith(testEmail, testPassword);

    expect(mockRouterPush).toHaveBeenCalledTimes(1);
    expect(mockRouterPush).toHaveBeenCalledWith('/campaigns');
    expect(wrapper.find('p.text-red-600').exists()).toBe(false);
  });

  it('shows error message and does not navigate on failed login action', async () => {
    const loginError = new Error('Invalid credentials from store');
    (loginError as any).response = { status: 401 };
    authStore.login = vi.fn().mockRejectedValue(loginError);

    const wrapper = mount(LoginForm, { global: { plugins: [pinia] } });

    const testEmail = 'bad@user.com';
    const testPassword = 'wrongpassword';

    await wrapper.find('input#email').setValue(testEmail);
    await wrapper.find('input#password').setValue(testPassword);

    await wrapper.find('form').trigger('submit.prevent');
    await vi.dynamicImportSettled();
    await nextTick();

    expect(authStore.login).toHaveBeenCalledTimes(1);
    expect(authStore.login).toHaveBeenCalledWith(testEmail, testPassword);

    expect(mockRouterPush).not.toHaveBeenCalled();

    const errorMessage = wrapper.find('p.text-red-600');
    expect(errorMessage.exists()).toBe(true);
    expect(errorMessage.text()).toBe('Invalid credentials');
  });

  it('displays loading state on button during submission', async () => {
    authStore.login = vi.fn().mockImplementation(() => new Promise(() => {}));

    const wrapper = mount(LoginForm, { global: { plugins: [pinia] } });

    await wrapper.find('input#email').setValue('test@example.com');
    await wrapper.find('input#password').setValue('password');

    wrapper.find('form').trigger('submit.prevent');
    await nextTick();

    const button = wrapper.findComponent(BaseButton);
    expect(button.props('loading')).toBe(true);
  });
});
