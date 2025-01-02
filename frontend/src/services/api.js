import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

export const getCostOverview = () => {
  return axios.get(`${API_BASE_URL}/api/costs/overview`);
};

export const getOptimizationRecommendations = () => {
  return axios.get(`${API_BASE_URL}/api/recommendations`);
};

export const getCostDetails = (timeRange) => {
  return axios.get(`${API_BASE_URL}/api/costs/details`, {
    params: { timeRange }
  });
};