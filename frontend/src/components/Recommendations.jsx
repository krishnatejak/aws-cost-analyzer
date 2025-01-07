import React from 'react';

const Recommendations = ({ recommendations = [] }) => {
  if (!Array.isArray(recommendations) || recommendations.length === 0) return null;

  return (
    <div className="bg-white p-4 rounded shadow">
      <h2 className="text-xl font-semibold mb-4">Optimization Recommendations</h2>
      <div className="space-y-4">
        {recommendations.map((rec, index) => (
          <div key={index} className="p-4 bg-blue-50 rounded">
            <h3 className="font-medium">{rec.title || 'N/A'}</h3>
            <p className="text-gray-600 mt-1">{rec.description || 'No description available'}</p>
            <div className="mt-2 text-sm">
              <span className="font-medium">Potential savings: </span>
              ${(rec.potentialSavings || 0).toFixed(2)}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Recommendations;