import axios from 'axios';

const API_BASE_URL = 'http://localhost:5050/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

export const getCostOverview = () => api.get('/cost/overview');
export const getEC2Analysis = () => api.get('/services/ec2/instances');
export const getRDSAnalysis = () => api.get('/services/rds/instances');