import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:5000/api/v1',
  timeout: 30000,
});

export const fetchCostAnalysis = async () => {
  const response = await api.get('/cost-analysis');
  return response.data;
};

export const fetchServiceAnalysis = async (service) => {
  const response = await api.get(`/services/${service}`);
  return response.data;
};

export const fetchOptimizationRecommendations = async () => {
  const response = await api.get('/recommendations');
  return response.data;
};

export const fetchResourceUtilization = async (resourceType) => {
  const response = await api.get(`/utilization/${resourceType}`);
  return response.data;
};

export const exportAnalysisReport = async (filters) => {
  const response = await api.post('/export', filters, { responseType: 'blob' });
  return response.data;
};