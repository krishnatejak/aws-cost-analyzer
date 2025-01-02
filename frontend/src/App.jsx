import React from 'react';
import CostOverview from './components/CostOverview';
import ServiceBreakdown from './components/ServiceBreakdown';
import Recommendations from './components/Recommendations';
import useCostData from './hooks/useCostData';

const App = () => {
  const { overview, serviceBreakdown, recommendations, loading, error } = useCostData();

  if (loading) return <div className="p-4">Loading...</div>;
  if (error) return <div className="p-4 text-red-500">Error: {error}</div>;

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6">AWS Cost Analysis</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <CostOverview data={overview} />
        <ServiceBreakdown data={serviceBreakdown} />
      </div>
      <div className="mt-6">
        <Recommendations recommendations={recommendations} />
      </div>
    </div>
  );
};

export default App;