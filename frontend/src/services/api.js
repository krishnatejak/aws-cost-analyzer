import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5050';

axios.interceptors.request.use((config) => {
  const authToken = localStorage.getItem('token');
  if (authToken) {
    config.headers.Authorization = `Bearer ${authToken}`;
  }
  return config;
});

export const getCostOverview = () => {
  return axios.get(`${API_BASE_URL}/api/v1/cost/overview`);
};

export const getCostsByService = async () => {
  const response = await axios.get(`${API_BASE_URL}/api/v1/cost/by-service`);
  // Return the raw response without unwrapping
  return response;
};

export const getOptimizationRecommendations = () => {
  return axios.get(`${API_BASE_URL}/api/v1/optimization/recommendations`);
};