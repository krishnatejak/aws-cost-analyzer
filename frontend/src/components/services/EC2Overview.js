import React, { useState, useEffect } from 'react';
import { getEC2Analysis } from '../../services/api';

const EC2Overview = () => {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAnalysis = async () => {
      try {
        const response = await getEC2Analysis();
        setAnalysis(response.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchAnalysis();
  }, []);

  if (loading) return <div>Loading EC2 analysis...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="ec2-overview">
      <h2 className="text-xl font-bold mb-4">EC2 Analysis</h2>
      {analysis && (
        <div>
          <div className="stats grid grid-cols-3 gap-4 mb-6">
            <div className="stat-card p-4 border rounded">
              <div className="text-lg font-semibold">Total Instances</div>
              <div className="text-2xl">{analysis.total_instances}</div>
            </div>
            <div className="stat-card p-4 border rounded">
              <div className="text-lg font-semibold">Running</div>
              <div className="text-2xl">{analysis.running_instances}</div>
            </div>
            <div className="stat-card p-4 border rounded">
              <div className="text-lg font-semibold">Stopped</div>
              <div className="text-2xl">{analysis.stopped_instances}</div>
            </div>
          </div>

          {analysis.optimization_opportunities?.length > 0 && (
            <div className="opportunities mb-6">
              <h3 className="text-lg font-semibold mb-3">Optimization Opportunities</h3>
              {analysis.optimization_opportunities.map((opp, index) => (
                <div key={index} className="opportunity-card p-4 mb-3 border rounded">
                  <div className="font-semibold">{opp.type}</div>
                  <div className="text-gray-600">{opp.description}</div>
                  <div className="mt-2">
                    <span className="font-medium">Current Value: </span>
                    {opp.current_value}
                  </div>
                  {opp.estimated_savings && (
                    <div className="text-green-600">
                      Potential Savings: {opp.estimated_savings}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}

          <div className="instances">
            <h3 className="text-lg font-semibold mb-3">Instance Details</h3>
            {analysis.instances?.map((instance, index) => (
              <div key={index} className="instance-card p-4 mb-3 border rounded">
                <div className="flex justify-between">
                  <span className="font-semibold">{instance.id}</span>
                  <span className={`status ${instance.state === 'running' ? 'text-green-600' : 'text-red-600'}`}>
                    {instance.state}
                  </span>
                </div>
                <div className="mt-2">
                  <div>Type: {instance.type}</div>
                  <div>Launch Time: {new Date(instance.launch_time).toLocaleString()}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default EC2Overview;