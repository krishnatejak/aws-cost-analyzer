import React from 'react';
import CostOverview from './components/CostOverview';
import ServiceBreakdown from './components/ServiceBreakdown';
import Recommendations from './components/Recommendations';
import useCostData from './hooks/useCostData';

const App = () => {
  const { overview, serviceBreakdown, recommendations, loading, error } = useCostData();

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-lg">Loading AWS cost data...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-red-500 text-lg">
          Error: {typeof error === 'string' ? error : 'Failed to load data'}
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6">AWS Cost Analysis</h1>
      <div className="grid grid-cols-1 gap-6">
        <CostOverview data={overview} />
        <ServiceBreakdown data={serviceBreakdown} />
        <Recommendations recommendations={recommendations} />
      </div>
    </div>
  );
};

export default App;