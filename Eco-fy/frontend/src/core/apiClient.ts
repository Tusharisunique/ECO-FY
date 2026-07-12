import axios from 'axios';
import { useAuthStore } from './authStore';

const API_BASE = 'http://localhost:8000/api/v1';

export const apiClient = axios.create({ baseURL: API_BASE });

apiClient.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token is expired or invalid — clear auth and redirect to login
      useAuthStore.getState().logout();
      window.location.href = '/login';
    } else if (error.response && error.response.status >= 400) {
      console.error(`API Error ${error.response.status}:`, error.response.data?.detail || error.message);
    }
    return Promise.reject(error);
  }
);
