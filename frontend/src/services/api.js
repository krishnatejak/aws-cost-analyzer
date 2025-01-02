import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5050';

export const getCostOverview = () => {
  return axios.get(`${API_BASE_URL}/api/v1/cost/overview`);
};

export const getOptimizationRecommendations = () => {
  return axios.get(`${API_BASE_URL}/api/v1/optimization/recommendations`);
};

export const getCostDetails = (timeRange) => {
  return axios.get(`${API_BASE_URL}/api/v1/cost/${timeRange}`);
};