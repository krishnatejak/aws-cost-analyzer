import { useQuery } from 'react-query';
import { fetchCostAnalysis, fetchServiceAnalysis, fetchOptimizationRecommendations } from '../services/api';

export const useCostAnalysis = () => {
  return useQuery('costAnalysis', fetchCostAnalysis);
};

export const useServiceAnalysis = (service) => {
  return useQuery(['serviceAnalysis', service], () => fetchServiceAnalysis(service));
};

export const useOptimizationRecommendations = () => {
  return useQuery('optimizationRecommendations', fetchOptimizationRecommendations);
};