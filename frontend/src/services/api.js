import axios from 'axios';

const API_BASE_URL = 'http://localhost:5050/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

export const getCostOverview = () => api.get('/cost/overview');
export const getCostsByService = (service) => api.get(`/cost/${service}`);
export const getServiceCosts = (service) => api.get(`/cost/${service}`);
export const getEC2Analysis = () => api.get('/services/ec2');
export const getRDSAnalysis = () => api.get('/services/rds');
export const getCostRecommendations = () => api.get('/optimization/recommendations');
export const getSavingsPlan = () => api.get('/optimization/overview');
export const getCostTrends = (timeRange) => api.get('/cost/trends', { params: { timeRange } });