import React, { useState, useEffect } from 'react';
import { getCostRecommendations } from '../../services/api';

const CostRecommendations = () => {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRecommendations = async () => {
      try {
        const response = await getCostRecommendations();
        setRecommendations(response.data);
      } catch (error) {
        console.error('Error fetching recommendations:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchRecommendations();
  }, []);

  if (loading) return <div>Loading recommendations...</div>;

  return (
    <div className="recommendations">
      <h2 className="text-xl font-bold mb-4">Cost Optimization Recommendations</h2>
      {recommendations.map((rec, index) => (
        <div key={index} className="recommendation-card p-4 mb-4 border rounded">
          <h3 className="font-semibold">{rec.title}</h3>
          <p>{rec.description}</p>
          <div className="mt-2">
            <span className="font-medium">Potential Savings: </span>
            ${rec.potentialSavings}
          </div>
        </div>
      ))}
    </div>
  );
};

export default CostRecommendations;