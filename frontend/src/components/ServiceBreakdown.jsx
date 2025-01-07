import React from 'react';

const ServiceBreakdown = ({ data }) => {
  // Handle case when data is not available yet
  if (!data || !data.ResultsByTime || !data.ResultsByTime[0] || !data.ResultsByTime[0].Groups) {
    return (
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-xl font-bold mb-4">Service Cost Breakdown</h2>
        <p className="text-gray-500">Loading service data...</p>
      </div>
    );
  }

  // Get non-estimated data period or fall back to the first period
  const relevantPeriod = data.ResultsByTime.find(period => !period.Estimated) || data.ResultsByTime[0];

  // Transform and sort the data
  const servicesData = relevantPeriod.Groups
    .map(group => ({
      name: group.Keys[0],
      cost: parseFloat(group.Metrics.UnblendedCost.Amount || 0)
    }))
    .filter(service => service.cost > 0)
    .sort((a, b) => b.cost - a.cost)
    .slice(0, 10);

  // Calculate total cost
  const totalCost = servicesData.reduce((sum, service) => sum + service.cost, 0);

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h2 className="text-xl font-bold mb-6">Top 10 Services by Cost</h2>
      <div className="space-y-4">
        {servicesData.map((service, index) => (
          <div 
            key={service.name}
            className="border-b border-gray-100 last:border-0 pb-4 last:pb-0"
          >
            <div className="flex justify-between items-center">
              <div className="flex items-center space-x-3">
                <span className="w-6 h-6 flex items-center justify-center bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
                  {index + 1}
                </span>
                <span className="text-gray-700">{service.name}</span>
              </div>
              <span className="font-medium text-gray-900">
                ${service.cost.toLocaleString(undefined, {
                  minimumFractionDigits: 2,
                  maximumFractionDigits: 2
                })}
              </span>
            </div>
            <div className="mt-2 w-full bg-gray-100 rounded-full h-1.5">
              <div
                className="bg-blue-500 h-1.5 rounded-full transition-all duration-300"
                style={{
                  width: `${(service.cost / servicesData[0].cost) * 100}%`
                }}
              />
            </div>
          </div>
        ))}
      </div>
      <div className="mt-6 pt-4 border-t border-gray-200">
        <div className="flex justify-between items-center">
          <span className="font-semibold text-gray-700">Total (Top 10)</span>
          <span className="font-bold text-gray-900">
            ${totalCost.toLocaleString(undefined, {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2
            })}
          </span>
        </div>
      </div>
    </div>
  );
};

export default ServiceBreakdown;