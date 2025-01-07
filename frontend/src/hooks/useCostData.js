import { useState, useEffect } from 'react';
import { getCostOverview, getCostsByService, getOptimizationRecommendations } from '../services/api';

const useCostData = () => {
  const [overview, setOverview] = useState(null);
  const [serviceBreakdown, setServiceBreakdown] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);

        const servicesRes = await getCostsByService();
        if (servicesRes?.data) {
          setServiceBreakdown(servicesRes.data);
        }

        const [overviewRes, recsRes] = await Promise.all([
          getCostOverview(),
          getOptimizationRecommendations()
        ]);

        if (overviewRes?.data) {
          setOverview(overviewRes.data);
        }

        if (recsRes?.data) {
          setRecommendations(recsRes.data);
        }

      } catch (err) {
        console.error('Error fetching data:', err);
        setError(err.response?.data?.error || err.message || 'Failed to fetch data');
        setServiceBreakdown(null);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return {
    overview,
    serviceBreakdown,
    recommendations,
    loading,
    error,
  };
};

export default useCostData;