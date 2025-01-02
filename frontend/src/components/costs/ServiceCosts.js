import React, { useState, useEffect } from 'react';
import { getServiceCosts } from '../../services/api';

const ServiceCosts = ({ service }) => {
  const [costs, setCosts] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await getServiceCosts(service);
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
    <div className="service-costs">
      <h3>{service} Costs</h3>
      {costs && (
        <div className="cost-details">
          <div className="mb-4">
            <span className="font-bold">Total Cost: </span>
            ${costs.total_cost?.toFixed(2)}
          </div>
          {costs.daily_costs?.length > 0 && (
            <div className="daily-costs">
              <h4 className="font-semibold mb-2">Daily Breakdown</h4>
              {costs.daily_costs.map((day, index) => (
                <div key={index} className="flex justify-between py-1">
                  <span>{day.date}</span>
                  <span>${day.cost.toFixed(2)}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ServiceCosts;