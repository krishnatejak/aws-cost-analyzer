import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { BarChart, Server, TrendingDown } from 'lucide-react';

const Sidebar = () => {
  const location = useLocation();

  const navigation = [
    { name: 'Dashboard', href: '/', icon: BarChart },
    { name: 'Services', href: '/services', icon: Server },
    { name: 'Optimization', href: '/optimization', icon: TrendingDown },
  ];

  return (
    <div className="fixed inset-y-0 left-0 w-64 bg-white border-r">
      <div className="flex flex-col h-full">
        <div className="flex-1 overflow-y-auto py-4 px-3">
          <nav className="space-y-1">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href;
              const Icon = item.icon;
              
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`flex items-center px-4 py-2 text-sm font-medium rounded-md ${
                    isActive
                      ? 'bg-gray-100 text-gray-900'
                      : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                  }`}
                >
                  <Icon
                    className={`mr-3 h-6 w-6 ${
                      isActive ? 'text-gray-900' : 'text-gray-400'
                    }`}
                  />
                  {item.name}
                </Link>
              );
            })}
          </nav>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;