import React, { useState, useEffect } from 'react';
import { getCostsByService } from '../../services/api';

const CostByService = ({ service }) => {
  const [costs, setCosts] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await getCostsByService(service);
        setCosts(response.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [service]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="cost-by-service">
      <h3>{service} Costs</h3>
      {/* Add visualization of cost data */}
    </div>
  );
};

export default CostByService;