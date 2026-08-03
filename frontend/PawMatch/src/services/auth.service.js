import authApi from '../api/auth.api';
import profileApi from '../api/profile.api';
import tokenStorage from '../utils/tokenStorage';

export const authService = {
  login: async (email, password) => {
    const res = await authApi.login({ email, password });
    if (res.success && res.data) {
      const { access, refresh, user } = res.data;
      tokenStorage.setTokens(access, refresh, user);
    }
    return res;
  },

  register: async (registrationData) => {
    const res = await authApi.register(registrationData);
    return res;
  },

  logout: async () => {
    const refresh = tokenStorage.getRefreshToken();
    try {
      if (refresh) {
        await authApi.logout(refresh);
      }
    } catch (e) {
      console.warn('Logout request sent, clearing tokens locally.', e);
    } finally {
      tokenStorage.clear();
    }
    return { success: true, message: 'Logged out successfully.' };
  },

  refreshToken: async () => {
    const refresh = tokenStorage.getRefreshToken();
    if (!refresh) {
      tokenStorage.clear();
      throw new Error('No refresh token available');
    }
    const res = await authApi.refreshToken(refresh);
    if (res.success && res.data) {
      const { access, refresh: newRefresh } = res.data;
      tokenStorage.setAccessToken(access);
      if (newRefresh) {
        tokenStorage.setRefreshToken(newRefresh);
      }
    }
    return res;
  },

  getCurrentUser: async () => {
    const res = await profileApi.getCurrentUser();
    if (res.success && res.data) {
      tokenStorage.setUser(res.data);
    }
    return res;
  },

  verifyEmail: async (token, method = 'POST') => {
    return authApi.verifyEmail(token, method);
  },

  resendVerification: async (email) => {
    return authApi.resendVerification(email);
  },

  forgotPassword: async (email) => {
    return authApi.forgotPassword(email);
  },

  resetPassword: async (payload) => {
    return authApi.resetPassword(payload);
  },
};

export default authService;
