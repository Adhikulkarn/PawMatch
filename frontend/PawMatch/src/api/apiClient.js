import axios from 'axios';
import config from '../config/env.config';
import tokenStorage from '../utils/tokenStorage';
import parseApiError from '../utils/errorHandler';
import handleApiResponse from '../utils/responseHandler';

let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  failedQueue = [];
};

export const apiClient = axios.create({
  baseURL: config.apiBaseUrl,
  timeout: config.timeout,
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
});

// Attach JWT bearer token to requests
apiClient.interceptors.request.use(
  (reqConfig) => {
    const accessToken = tokenStorage.getAccessToken();
    if (accessToken && !reqConfig.headers.Authorization) {
      reqConfig.headers.Authorization = `Bearer ${accessToken}`;
    }
    return reqConfig;
  },
  (error) => Promise.reject(error)
);

// Response Interceptor for Token Refresh & Error Handling
apiClient.interceptors.response.use(
  (response) => handleApiResponse(response),
  async (error) => {
    const originalRequest = error.config;

    if (
      error.response?.status === 401 &&
      originalRequest &&
      !originalRequest._retry &&
      !originalRequest.url?.includes('/accounts/login/') &&
      !originalRequest.url?.includes('/accounts/token/refresh/')
    ) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        })
          .then((token) => {
            originalRequest.headers.Authorization = `Bearer ${token}`;
            return apiClient(originalRequest);
          })
          .catch((err) => Promise.reject(parseApiError(err)));
      }

      originalRequest._retry = true;
      isRefreshing = true;

      const refreshToken = tokenStorage.getRefreshToken();
      if (!refreshToken) {
        isRefreshing = false;
        tokenStorage.clear();
        window.dispatchEvent(new CustomEvent('auth:logout'));
        return Promise.reject(parseApiError(error));
      }

      try {
        const refreshResponse = await axios.post(
          `${config.apiBaseUrl}/api/v1/accounts/token/refresh/`,
          { refresh: refreshToken },
          { headers: { 'Content-Type': 'application/json' } }
        );

        const responseData = refreshResponse.data?.data || refreshResponse.data;
        const newAccessToken = responseData?.access;
        const newRefreshToken = responseData?.refresh;

        if (newAccessToken) {
          tokenStorage.setAccessToken(newAccessToken);
          if (newRefreshToken) {
            tokenStorage.setRefreshToken(newRefreshToken);
          }

          apiClient.defaults.headers.common.Authorization = `Bearer ${newAccessToken}`;
          originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;

          processQueue(null, newAccessToken);
          return apiClient(originalRequest);
        } else {
          throw new Error('Refresh endpoint response missing access token');
        }
      } catch (refreshErr) {
        processQueue(refreshErr, null);
        tokenStorage.clear();
        window.dispatchEvent(new CustomEvent('auth:logout'));
        return Promise.reject(parseApiError(refreshErr));
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(parseApiError(error));
  }
);

export default apiClient;
