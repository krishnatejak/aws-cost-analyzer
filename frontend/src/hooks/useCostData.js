import { useState, useEffect } from 'react';
import { getCostOverview, getCostsByService, getCostRecommendations } from '../services/api';

const useCostData = () => {
  const [overview, setOverview] = useState(null);
  const [serviceBreakdown, setServiceBreakdown] = useState(null);
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [overviewData, serviceData, recommendationsData] = await Promise.all([
          getCostOverview(),
          getCostsByService(),
          getCostRecommendations()
        ]);

        setOverview(overviewData.data);
        setServiceBreakdown(serviceData.data);
        setRecommendations(recommendationsData.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return { overview, serviceBreakdown, recommendations, loading, error };
};

export default useCostData;