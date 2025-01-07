import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const CostOverview = ({ data }) => {
  // Add explicit console log for debugging
  console.log('CostOverview data:', data);

  if (!data || !data.ResultsByTime) {
    return (
      <div className="bg-white p-4 rounded shadow">
        <h2 className="text-xl font-semibold mb-4">Cost Overview</h2>
        <p>No cost data available</p>
      </div>
    );
  }

  const chartData = data.ResultsByTime.map(item => ({
    date: item.TimePeriod?.Start,
    cost: parseFloat(item.Total?.UnblendedCost?.Amount || 0)
  })).filter(item => !isNaN(item.cost));

  if (chartData.length === 0) {
    return (
      <div className="bg-white p-4 rounded shadow">
        <h2 className="text-xl font-semibold mb-4">Cost Overview</h2>
        <p>No valid cost data available</p>
      </div>
    );
  }

  return (
    <div className="bg-white p-4 rounded shadow">
      <h2 className="text-xl font-semibold mb-4">Cost Overview</h2>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="date" 
              tickFormatter={(date) => new Date(date).toLocaleDateString()}
            />
            <YAxis 
              tickFormatter={(value) => `$${value.toFixed(2)}`}
            />
            <Tooltip 
              formatter={(value) => [`$${value.toFixed(2)}`, 'Cost']}
              labelFormatter={(date) => new Date(date).toLocaleDateString()}
            />
            <Line type="monotone" dataKey="cost" stroke="#8884d8" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default CostOverview;