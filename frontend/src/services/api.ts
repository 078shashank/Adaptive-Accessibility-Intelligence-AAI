/** API Service */
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add JWT token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authService = {
  register: async (email: string, password: string, fullName?: string) => {
    const response = await api.post('/auth/register', {
      email,
      password,
      full_name: fullName,
    });
    return response.data;
  },

  login: async (email: string, password: string) => {
    const response = await api.post('/auth/login', {
      email,
      password,
    });
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token);
    }
    return response.data;
  },

  logout: () => {
    localStorage.removeItem('access_token');
  },
};

export const userService = {
  getProfile: async () => {
    const response = await api.get('/user/profile');
    return response.data;
  },

  updateProfile: async (profile: Record<string, any>) => {
    const response = await api.put('/user/profile', profile);
    return response.data;
  },
};

export const textService = {
  simplify: async (text: string, readingLevel: string = 'intermediate') => {
    const response = await api.post('/text/simplify', {
      text,
      reading_level: readingLevel,
    });
    return response.data;
  },
};

export const avatarService = {
  generateSignAnimation: async (text: string) => {
    const response = await api.post('/avatar/sign', { text });
    return response.data;
  },

  getLanguages: async () => {
    const response = await api.get('/avatar/languages');
    return response.data;
  },

  segmentText: async (text: string) => {
    const response = await api.post('/avatar/segment', { text });
    return response.data;
  },
};

export const healthService = {
  check: async () => {
    const response = await api.get('/health');
    return response.data;
  },
};

export default api;
