import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard, Building2, FileUp, BarChart3,
  Search, MessageSquarePlus, Shield, FileText, Landmark
} from 'lucide-react';

const navItems = [
  { path: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { path: '/company', icon: Building2, label: 'Company Profile' },
  { path: '/documents', icon: FileUp, label: 'Data Ingestor' },
  { path: '/financials', icon: BarChart3, label: 'Financial Analysis' },
  { path: '/research', icon: Search, label: 'Research Agent' },
  { path: '/insights', icon: MessageSquarePlus, label: 'Primary Insights' },
  { path: '/scoring', icon: Shield, label: 'Credit Scoring' },
  { path: '/cam', icon: FileText, label: 'CAM Report' },
];

export default function Sidebar() {
  return (
    <nav className="sidebar">
      <div className="sidebar-header">
        <div className="logo">
          <Landmark size={28} />
          <span>IntelCredit</span>
        </div>
        <small>AI-Powered Credit Decisioning</small>
      </div>
      <ul className="nav-menu">
        {navItems.map(item => (
          <li key={item.path}>
            <NavLink
              to={item.path}
              end={item.path === '/'}
              className={({ isActive }) => `nav-item${isActive ? ' active' : ''}`}
            >
              <item.icon size={18} />
              {item.label}
            </NavLink>
          </li>
        ))}
      </ul>
    </nav>
  );
}
