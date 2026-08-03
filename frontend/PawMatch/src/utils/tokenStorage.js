import config from '../config/env.config';

export const tokenStorage = {
  getAccessToken: () => {
    try {
      return localStorage.getItem(config.tokenKeys.ACCESS) || null;
    } catch (e) {
      console.error('Error reading access token:', e);
      return null;
    }
  },

  setAccessToken: (token) => {
    try {
      if (token) {
        localStorage.setItem(config.tokenKeys.ACCESS, token);
      } else {
        localStorage.removeItem(config.tokenKeys.ACCESS);
      }
    } catch (e) {
      console.error('Error saving access token:', e);
    }
  },

  getRefreshToken: () => {
    try {
      return localStorage.getItem(config.tokenKeys.REFRESH) || null;
    } catch (e) {
      console.error('Error reading refresh token:', e);
      return null;
    }
  },

  setRefreshToken: (token) => {
    try {
      if (token) {
        localStorage.setItem(config.tokenKeys.REFRESH, token);
      } else {
        localStorage.removeItem(config.tokenKeys.REFRESH);
      }
    } catch (e) {
      console.error('Error saving refresh token:', e);
    }
  },

  getUser: () => {
    try {
      const userStr = localStorage.getItem(config.tokenKeys.USER);
      return userStr ? JSON.parse(userStr) : null;
    } catch (e) {
      console.error('Error reading stored user:', e);
      return null;
    }
  },

  setUser: (user) => {
    try {
      if (user) {
        localStorage.setItem(config.tokenKeys.USER, JSON.stringify(user));
      } else {
        localStorage.removeItem(config.tokenKeys.USER);
      }
    } catch (e) {
      console.error('Error saving user data:', e);
    }
  },

  setTokens: (access, refresh, user = null) => {
    tokenStorage.setAccessToken(access);
    tokenStorage.setRefreshToken(refresh);
    if (user) {
      tokenStorage.setUser(user);
    }
  },

  clear: () => {
    try {
      localStorage.removeItem(config.tokenKeys.ACCESS);
      localStorage.removeItem(config.tokenKeys.REFRESH);
      localStorage.removeItem(config.tokenKeys.USER);
    } catch (e) {
      console.error('Error clearing stored tokens:', e);
    }
  },
};

export default tokenStorage;
