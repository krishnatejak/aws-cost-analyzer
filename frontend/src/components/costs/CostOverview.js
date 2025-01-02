import React, { useState, useEffect } from 'react';
import { getCostOverview } from '../../services/api';

const CostOverview = () => {
  const [overview, setOverview] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchOverview = async () => {
      try {
        const response = await getCostOverview();
        setOverview(response.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchOverview();
  }, []);

  if (loading) return <div>Loading overview...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="cost-overview">
      <h2 className="text-xl font-bold mb-4">Cost Overview</h2>
      {overview && (
        <div>
          <div className="total-cost mb-6">
            <span className="text-lg font-semibold">Total Cost: </span>
            <span className="text-xl">${overview.total_cost?.toFixed(2)}</span>
          </div>
          
          <div className="services-breakdown">
            <h3 className="text-lg font-semibold mb-3">Services Breakdown</h3>
            {overview.services?.map((service, index) => (
              <div key={index} className="service-row flex justify-between py-2 border-b">
                <span>{service.name}</span>
                <span>${service.cost?.toFixed(2)}</span>
              </div>
            ))}
          </div>

          {overview.daily_costs?.length > 0 && (
            <div className="daily-trend mt-6">
              <h3 className="text-lg font-semibold mb-3">Daily Trend</h3>
              {overview.daily_costs.map((day, index) => (
                <div key={index} className="day-row flex justify-between py-1">
                  <span>{day.date}</span>
                  <span>${day.cost?.toFixed(2)}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default CostOverview;