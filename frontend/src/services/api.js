import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const getCostOverview = () => api.get('/api/costs/overview');
export const getCostsByService = () => api.get('/api/costs/by-service');
export const getCostRecommendations = () => api.get('/api/costs/recommendations');

export default api;