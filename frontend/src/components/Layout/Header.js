import React from 'react';
import { useNavigate } from 'react-router-dom';

const Header = () => {
  const navigate = useNavigate();

  return (
    <header className="bg-white shadow-sm">
      <div className="mx-auto py-4 px-6">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-semibold text-gray-900">
            AWS Cost Analyzer
          </h1>
          <div className="flex items-center space-x-4">
            <button
              onClick={() => navigate('/settings')}
              className="text-gray-600 hover:text-gray-900"
            >
              Settings
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;