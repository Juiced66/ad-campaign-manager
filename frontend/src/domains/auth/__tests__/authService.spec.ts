import { vi } from 'vitest';
import api from '@/shared/composables/useApi';
import * as authService from '../authService';
import { User } from '@/domains/user/userTypes';

vi.mock('@/shared/composables/useApi', () => {
  return {
    default: {
      post: vi.fn(),
      get: vi.fn(),
    },
  };
});

const mockedApi = api as vi.Mocked<typeof api>;

describe('authService.ts', () => {
  beforeEach(() => {
    // Reset mocks before each test
    vi.clearAllMocks();
  });

  // --- login ---
  it('login calls api.post with correct URL and credentials', async () => {
    const email = 'test@example.com';
    const password = 'password123';
    const mockToken = 'mock-jwt-token';
    mockedApi.post.mockResolvedValue({ data: { access_token: mockToken } }); // Simulate successful API response

    await authService.login(email, password);

    expect(mockedApi.post).toHaveBeenCalledTimes(1);
    expect(mockedApi.post).toHaveBeenCalledWith('/auth/login', {
      email,
      password,
    });
  });

  it('login returns access_token on success', async () => {
    const email = 'test@example.com';
    const password = 'password123';
    const mockToken = 'mock-jwt-token';
    mockedApi.post.mockResolvedValue({ data: { access_token: mockToken } });

    const token = await authService.login(email, password);

    expect(token).toBe(mockToken);
  });

  it('login throws error on API failure', async () => {
    const email = 'test@example.com';
    const password = 'password123';
    const error = new Error('Network Error');
    mockedApi.post.mockRejectedValue(error); // Simulate API error

    await expect(authService.login(email, password)).rejects.toThrow(
      'Network Error'
    );
    expect(mockedApi.post).toHaveBeenCalledTimes(1);
  });

  // --- logout ---
  it('logout calls api.post with correct URL', async () => {
    mockedApi.post.mockResolvedValue({}); // Simulate success (logout often has no content)

    await authService.logout();

    expect(mockedApi.post).toHaveBeenCalledTimes(1);
    expect(mockedApi.post).toHaveBeenCalledWith('/auth/logout');
  });

  it('logout returns { success: true } even on API success', async () => {
    mockedApi.post.mockResolvedValue({});
    const result = await authService.logout();
    expect(result).toEqual({ success: true });
  });

  it('logout returns { success: true } even on API failure (silent fail)', async () => {
    const error = new Error('Server Error');
    mockedApi.post.mockRejectedValue(error); // Simulate API error

    const result = await authService.logout();

    expect(mockedApi.post).toHaveBeenCalledTimes(1);
    expect(result).toEqual({ success: true }); // Should still resolve successfully for the caller
  });
});
