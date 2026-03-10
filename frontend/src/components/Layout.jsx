import { useEffect, useState } from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import Sidebar from './Sidebar';
import Toast from './Toast';
import LoadingOverlay from './LoadingOverlay';
import api from '../services/api';

const pageTitles = {
  '/': 'Dashboard',
  '/company': 'Company Profile',
  '/documents': 'Data Ingestor',
  '/financials': 'Financial Analysis',
  '/research': 'Research Agent',
  '/insights': 'Primary Insights',
  '/scoring': 'Credit Scoring',
  '/cam': 'CAM Report',
};

export default function Layout() {
  const location = useLocation();
  const [apiStatus, setApiStatus] = useState(null);

  useEffect(() => {
    api.health()
      .then(() => setApiStatus(true))
      .catch(() => setApiStatus(false));
  }, []);

  const title = pageTitles[location.pathname] || 'IntelCredit';

  return (
    <div className="app-layout">
      <Sidebar />
      <main className="main-content">
        <div className="topbar">
          <h2 className="page-title">{title}</h2>
          <div className="status-indicator">
            <span className={`status-dot${apiStatus === false ? ' offline' : ''}`} />
            {apiStatus === true ? 'API Connected' : apiStatus === false ? 'API Offline' : 'Checking...'}
          </div>
        </div>
        <div className="page-content">
          <Outlet />
        </div>
      </main>
      <Toast />
      <LoadingOverlay />
    </div>
  );
}
