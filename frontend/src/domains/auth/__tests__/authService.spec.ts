import { vi } from 'vitest';
import api from '@/shared/composables/useApi';
import * as authService from '../authService';
import type { Token } from '../authTypes';

vi.mock('@/shared/composables/useApi', () => ({
  default: {
    post: vi.fn(),
    get: vi.fn(),
  },
}));

const mockedApi = api as vi.Mocked<typeof api>;

describe('authService.ts', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  // --- login ---
  it('login calls api.post with correct URL and credentials', async () => {
    const email = 'test@example.com';
    const password = 'password123';
    const mockResponse: Token = {
      access_token: 'mock-access',
      refresh_token: 'mock-refresh',
      token_type: 'bearer',
    };
    mockedApi.post.mockResolvedValue({ data: mockResponse });

    await authService.login(email, password);

    expect(mockedApi.post).toHaveBeenCalledTimes(1);
    expect(mockedApi.post).toHaveBeenCalledWith('/auth/login', {
      email,
      password,
    });
  });

  it('login returns Token object on success', async () => {
    const email = 'test@example.com';
    const password = 'password123';
    const mockResponse: Token = {
      access_token: 'mock-access-token',
      refresh_token: 'mock-refresh-token',
      token_type: 'bearer',
    };
    mockedApi.post.mockResolvedValue({ data: mockResponse });

    const tokenData = await authService.login(email, password);

    expect(tokenData).toEqual(mockResponse); // Check the whole object
  });

  it('login throws error on API failure', async () => {
    const email = 'test@example.com';
    const password = 'password123';
    const error = new Error('Network Error');
    mockedApi.post.mockRejectedValue(error);

    await expect(authService.login(email, password)).rejects.toThrow(
      'Network Error'
    );
    expect(mockedApi.post).toHaveBeenCalledTimes(1);
  });

  // --- logout ---
  it('logout calls api.post with correct URL and refresh token payload', async () => {
    const refreshTokenValue = 'some-refresh-token';
    mockedApi.post.mockResolvedValue({}); // Simulate success

    await authService.logout(refreshTokenValue); // Pass the token

    expect(mockedApi.post).toHaveBeenCalledTimes(1);
    expect(mockedApi.post).toHaveBeenCalledWith('/auth/logout', {
      refresh_token: refreshTokenValue,
    });
  });

  it('logout returns { success: true } on API success', async () => {
    mockedApi.post.mockResolvedValue({});
    const result = await authService.logout('token');
    expect(result).toEqual({ success: true });
  });

  it('logout returns { success: true } even on API failure (silent fail)', async () => {
    const error = new Error('Server Error');
    mockedApi.post.mockRejectedValue(error);
    const result = await authService.logout('token');
    expect(mockedApi.post).toHaveBeenCalledTimes(1);
    expect(result).toEqual({ success: true });
  });

  // --- refreshToken ---
  it('refreshToken calls api.post with correct URL and current refresh token', async () => {
    const currentRefreshToken = 'current-refresh-token';
    const mockResponse: Token = {
      access_token: 'new-access-token',
      refresh_token: 'new-refresh-token',
      token_type: 'bearer',
    };
    mockedApi.post.mockResolvedValue({ data: mockResponse });

    await authService.refreshToken(currentRefreshToken);

    expect(mockedApi.post).toHaveBeenCalledTimes(1);
    expect(mockedApi.post).toHaveBeenCalledWith('/auth/refresh', {
      refresh_token: currentRefreshToken,
    });
  });

  it('refreshToken returns new Token object on success', async () => {
    const currentRefreshToken = 'current-refresh-token';
    const mockResponse: Token = {
      access_token: 'new-access-token',
      refresh_token: 'new-refresh-token',
      token_type: 'bearer',
    };
    mockedApi.post.mockResolvedValue({ data: mockResponse });

    const newTokenData = await authService.refreshToken(currentRefreshToken);
    expect(newTokenData).toEqual(mockResponse);
  });

  it('refreshToken throws error on API failure', async () => {
    const currentRefreshToken = 'current-refresh-token';
    const error = new Error('Invalid Refresh Token');
    mockedApi.post.mockRejectedValue(error);

    await expect(authService.refreshToken(currentRefreshToken)).rejects.toThrow(
      'Invalid Refresh Token'
    );
    expect(mockedApi.post).toHaveBeenCalledTimes(1);
  });
});
