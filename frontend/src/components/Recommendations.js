import React from 'react';

const Recommendations = ({ recommendations }) => {
  return (
    <div className="p-4 bg-white rounded-lg shadow">
      <h2 className="text-xl font-bold mb-4">Cost Optimization Recommendations</h2>
      <div className="space-y-4">
        {recommendations.map((recommendation, index) => (
          <div key={index} className="border-l-4 border-blue-500 p-4 bg-blue-50">
            <h3 className="font-semibold">{recommendation.title}</h3>
            <p className="text-gray-600">{recommendation.description}</p>
            <div className="mt-2">
              <span className="text-sm font-medium text-blue-600">
                Potential Savings: ${recommendation.potentialSavings}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Recommendations;