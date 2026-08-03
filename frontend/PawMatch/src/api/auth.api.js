import apiClient from './apiClient';

export const authApi = {
  /**
   * POST /api/v1/accounts/register/
   * Register a new user account
   */
  register: (payload) => {
    return apiClient.post('/api/v1/accounts/register/', payload);
  },

  /**
   * POST /api/v1/accounts/login/
   * Authenticate user credentials and receive token pair
   */
  login: (credentials) => {
    return apiClient.post('/api/v1/accounts/login/', credentials);
  },

  /**
   * POST /api/v1/accounts/logout/
   * Blacklist refresh token and terminate active session
   */
  logout: (refreshToken) => {
    return apiClient.post('/api/v1/accounts/logout/', { refresh: refreshToken });
  },

  /**
   * POST /api/v1/accounts/token/refresh/
   * Acquire a new access token using a valid refresh token
   */
  refreshToken: (refreshToken) => {
    return apiClient.post('/api/v1/accounts/token/refresh/', { refresh: refreshToken });
  },

  /**
   * GET/POST /api/v1/accounts/verify-email/
   * Verify email using raw token
   */
  verifyEmail: (token, method = 'POST') => {
    if (method.toUpperCase() === 'GET') {
      return apiClient.get(`/api/v1/accounts/verify-email/?token=${encodeURIComponent(token)}`);
    }
    return apiClient.post('/api/v1/accounts/verify-email/', { token });
  },

  /**
   * POST /api/v1/accounts/resend-verification/
   * Resend account email verification link
   */
  resendVerification: (email) => {
    return apiClient.post('/api/v1/accounts/resend-verification/', { email });
  },

  /**
   * POST /api/v1/accounts/forgot-password/
   * Request password reset link
   */
  forgotPassword: (email) => {
    return apiClient.post('/api/v1/accounts/forgot-password/', { email });
  },

  /**
   * POST /api/v1/accounts/reset-password/
   * Reset password using verification token
   */
  resetPassword: (payload) => {
    return apiClient.post('/api/v1/accounts/reset-password/', payload);
  },
};

export default authApi;
