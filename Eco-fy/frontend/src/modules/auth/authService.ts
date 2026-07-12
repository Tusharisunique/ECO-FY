import { apiClient } from '../../core/apiClient';

export const login = async (email: string, password: string) => {
  const params = new URLSearchParams();
  params.append('username', email);
  params.append('password', password);
  const { data } = await apiClient.post('/auth/login', params, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  });
  return data as { access_token: string; token_type: string };
};

export const getMe = async () => {
  const { data } = await apiClient.get('/auth/me');
  return data;
};

export const register = async (payload: any) => {
  const { data } = await apiClient.post('/auth/register', payload);
  return data;
};
