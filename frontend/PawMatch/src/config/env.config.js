const ENV = {
  DEV: {
    API_BASE_URL: 'http://localhost:8000',
    TIMEOUT: 15000,
  },
  PROD: {
    API_BASE_URL: 'https://pawmatch-8zwt.onrender.com',
    TIMEOUT: 20000,
  },
};

const currentEnv = import.meta.env.MODE === 'production' ? 'PROD' : 'DEV';

export const config = {
  env: import.meta.env.MODE || 'development',
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || ENV[currentEnv].API_BASE_URL,
  timeout: Number(import.meta.env.VITE_API_TIMEOUT) || ENV[currentEnv].TIMEOUT,
  tokenKeys: {
    ACCESS: 'pawmatch_access_token',
    REFRESH: 'pawmatch_refresh_token',
    USER: 'pawmatch_user_data',
  },
};

export default config;
