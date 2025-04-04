import { mount } from '@vue/test-utils';
import { createTestingPinia } from '@pinia/testing';
import { vi } from 'vitest'; // Import Vitest utilities
import LoginForm from '../LoginForm.vue'; // Adjust path
import BaseInput from '@/shared/components/BaseInput.vue'; // Import used components
import BaseButton from '@/shared/components/BaseButton.vue';
import { useAuthStore } from '../authStore'; // Import store
import * as authService from '../authService'; // Import service to mock
import { nextTick } from 'vue';

// --- Mocking Setup ---

// Mock the vue-router
const mockRouterPush = vi.fn();
vi.mock('vue-router', () => ({
  useRouter: () => ({
    push: mockRouterPush,
  }),
}));

// Mock the authService.login function
const mockLoginService = vi.spyOn(authService, 'login'); // Use spyOn if you import *

// --- Test Suite ---

describe('LoginForm.vue', () => {
  let pinia: any; // Type explicitly if needed

  // Setup Pinia and reset mocks before each test
  beforeEach(() => {
    vi.clearAllMocks(); // Reset all mocks

    pinia = createTestingPinia({
      // Set stubActions to false if you want to test action logic
      // or rely on spies to check if they were called
      stubActions: false, // Let actions run, but we spy on service calls
      createSpy: vi.fn, // Use vitest's spy function
    });

    // Reset the service mock implementation before each test
    mockLoginService.mockResolvedValue('mock-test-token'); // Default success
  });

  it('renders email, password inputs, and login button', () => {
    const wrapper = mount(LoginForm, {
      global: {
        plugins: [pinia],
        stubs: {
          // Stub components only if necessary, often better to render real ones
          // BaseInput: true,
          // BaseButton: true,
        },
      },
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

    // Access internal component state (less ideal but sometimes needed)
    // Alternatively, check emitted events if BaseInput emitted them directly
    expect((wrapper.vm as any).form.email).toBe('test@example.com');
    expect((wrapper.vm as any).form.password).toBe('password123');
  });

  it('shows validation errors for empty fields on submit', async () => {
    const wrapper = mount(LoginForm, { global: { plugins: [pinia] } });

    await wrapper.find('form').trigger('submit.prevent');

    expect(mockLoginService).not.toHaveBeenCalled();
    expect(mockRouterPush).not.toHaveBeenCalled();

    const errors = (wrapper.vm as any).errors;
    expect(errors.email).toBe('Email required');
    expect(errors.password).toBe('Password required');

    // Check if errors are passed to BaseInput props (better approach)
    const emailInputWrapper = wrapper.findComponent(BaseInput); // Assuming first is email
    const passwordInputWrapper = wrapper.findAllComponents(BaseInput)[1];
    expect(emailInputWrapper.props('error')).toBe('Email required');
    expect(passwordInputWrapper.props('error')).toBe('Password required');
  });

  it('calls login service, sets token, and navigates on successful submit', async () => {
    const wrapper = mount(LoginForm, { global: { plugins: [pinia] } });
    const authStore = useAuthStore(); // Get store instance *after* pinia is attached

    const testEmail = 'good@user.com';
    const testPassword = 'correctpassword';
    const fakeToken = 'abc.123.def';
    mockLoginService.mockResolvedValue(fakeToken); // Ensure success mock

    await wrapper.find('input#email').setValue(testEmail);
    await wrapper.find('input#password').setValue(testPassword);

    await wrapper.find('form').trigger('submit.prevent');

    // Check service call
    expect(mockLoginService).toHaveBeenCalledTimes(1);
    expect(mockLoginService).toHaveBeenCalledWith(testEmail, testPassword);

    // Need to wait for promises inside submit to resolve
    await vi.dynamicImportSettled(); // Wait for async operations triggered by submit

    // Check store action (since stubActions is false, we check effects or spies)
    expect(authStore.token).toBe(fakeToken); // Check if state was updated

    // Check navigation
    expect(mockRouterPush).toHaveBeenCalledTimes(1);
    expect(mockRouterPush).toHaveBeenCalledWith('/campaigns');

    // Check no error message displayed
    expect(wrapper.find('p.text-red-600').exists()).toBe(false);
  });

  it('shows error message and does not navigate on failed login (invalid credentials)', async () => {
    const wrapper = mount(LoginForm, { global: { plugins: [pinia] } });
    const authStore = useAuthStore();

    const testEmail = 'bad@user.com';
    const testPassword = 'wrongpassword';

    // Simulate login failure
    mockLoginService.mockRejectedValue(
      new Error('Request failed with status code 401')
    );

    await wrapper.find('input#email').setValue(testEmail);
    await wrapper.find('input#password').setValue(testPassword);

    await wrapper.find('form').trigger('submit.prevent');

    // Check service call
    expect(mockLoginService).toHaveBeenCalledTimes(1);
    expect(mockLoginService).toHaveBeenCalledWith(testEmail, testPassword);

    // Need to wait for promises inside submit to resolve (including catch block)
    await vi.dynamicImportSettled();

    // Check store and router were NOT called/changed
    expect(authStore.token).toBeUndefined();
    expect(mockRouterPush).not.toHaveBeenCalled();

    // Check error message
    const errorMessage = wrapper.find('p.text-red-600');
    expect(errorMessage.exists()).toBe(true);
    expect(errorMessage.text()).toBe('Invalid credentials');
  });

  it('displays loading state on button during submission', async () => {
    // Mock login that never resolves to keep loading state
    mockLoginService.mockImplementation(() => new Promise(() => {}));

    const wrapper = mount(LoginForm, { global: { plugins: [pinia] } });

    await wrapper.find('input#email').setValue('test@example.com');
    await wrapper.find('input#password').setValue('password');

    // Trigger submit but don't wait for it to finish
    wrapper.find('form').trigger('submit.prevent');

    // Wait a tick for the loading state to potentially update
    await nextTick();

    const button = wrapper.findComponent(BaseButton);
    expect(button.props('loading')).toBe(true);
    // Optionally check for spinner SVG if needed
  });
});
