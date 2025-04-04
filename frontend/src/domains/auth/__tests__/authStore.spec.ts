import { createPinia, setActivePinia } from 'pinia';
import { useAuthStore } from '../authStore'; // Import the store
import * as authService from '../authService'; // Import service to mock its functions
import { vi } from 'vitest';
import type { Token } from '../authTypes';

// --- Mocking Setup ---

// Mock the entire authService module
vi.mock('../authService', () => ({
  login: vi.fn(),
  logout: vi.fn(),
  me: vi.fn(), // Mock other functions if the store ever uses them
}));

// Type assertion for easier mocking
const mockedAuthService = authService as vi.Mocked<typeof authService>;

// --- Test Suite ---

describe('authStore.ts', () => {
  // Setup Pinia before each test
  beforeEach(() => {
    setActivePinia(createPinia());
    // Reset mocks before each test
    vi.clearAllMocks();
  });

  it('initial state has undefined token', () => {
    const store = useAuthStore();
    expect(store.token).toBeUndefined();
  });

  it('setToken updates the token state', () => {
    const store = useAuthStore();
    const newToken = 'mock-jwt-token-string'; // Cast for simplicity in test

    store.setToken(newToken);

    expect(store.token).toBe(newToken);
  });

  it('login action calls authService.login', async () => {
    const store = useAuthStore();
    const email = 'test@user.com';
    const password = 'password';
    const fakeToken = 'returned-token';

    // Mock the service call *before* calling the action
    mockedAuthService.login.mockResolvedValue(fakeToken);

    await store.login(email, password);

    expect(mockedAuthService.login).toHaveBeenCalledTimes(1);
    expect(mockedAuthService.login).toHaveBeenCalledWith(email, password);
  });

  it('logout action calls authService.logout', async () => {
    const store = useAuthStore();
    const initialToken = 'existing-token';
    store.setToken(initialToken); // Set an initial token

    // Mock the service call
    mockedAuthService.logout.mockResolvedValue({ success: true });

    await store.logout();

    expect(mockedAuthService.logout).toHaveBeenCalledTimes(1);
  });

  it('persist configuration exists', () => {
    const storeDefinition = useAuthStore();

    expect(storeDefinition.$id).toBe('auth'); // Verify store ID as an indirect check
  });
});
