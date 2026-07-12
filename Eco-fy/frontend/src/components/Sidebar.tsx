import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import {
  LayoutDashboard, Leaf, Users, Shield, Trophy, BarChart3, Settings, LogOut, ChevronRight
} from 'lucide-react';
import { useAuthStore } from '../core/authStore';
import { cn } from './ui/Button';

interface NavItem {
  to: string;
  label: string;
  icon: React.ReactNode;
}

const navItems: NavItem[] = [
  { to: '/dashboard', label: 'Dashboard', icon: <LayoutDashboard size={18} /> },
  { to: '/environmental', label: 'Environmental', icon: <Leaf size={18} /> },
  { to: '/social', label: 'Social', icon: <Users size={18} /> },
  { to: '/governance', label: 'Governance', icon: <Shield size={18} /> },
  { to: '/gamification', label: 'Gamification', icon: <Trophy size={18} /> },
  { to: '/analytics', label: 'Analytics', icon: <BarChart3 size={18} /> },
];

const Sidebar: React.FC = () => {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const isAdmin = user?.is_superuser;
  const filteredNavItems = navItems.filter(item => {
    if (!isAdmin && (item.label === 'Governance' || item.label === 'Analytics')) {
      return false;
    }
    return true;
  });

  return (
    <aside className="w-64 min-h-screen bg-sidebar border-r border-border-color flex flex-col shrink-0">
      {/* Logo */}
      <div className="px-6 py-5 border-b border-border-color">
        <div className="flex items-center gap-2.5">
          <div className="w-7 h-7 rounded-lg bg-brand-green flex items-center justify-center">
            <Leaf size={14} className="text-white" />
          </div>
          <div>
            <p className="font-bold text-sm text-on-surface leading-none">Eco-fy</p>
            <p className="text-xs text-outline-variant">ESG OS</p>
          </div>
        </div>
      </div>

      {/* Nav */}
      <nav className="flex-1 py-4 px-3 space-y-0.5">
        {filteredNavItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              cn(
                'flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors group',
                isActive
                  ? 'bg-primary-container/30 text-primary'
                  : 'text-on-surface-variant hover:bg-surface-container hover:text-on-surface'
              )
            }
          >
            {item.icon}
            <span className="flex-1">{item.label}</span>
            <ChevronRight size={14} className="opacity-0 group-hover:opacity-50 transition-opacity" />
          </NavLink>
        ))}
      </nav>

      {/* User Footer */}
      <div className="px-3 py-4 border-t border-border-color space-y-0.5">
        <button
          id="logout-btn"
          onClick={handleLogout}
          className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-on-surface-variant hover:bg-error-container hover:text-error transition-colors"
        >
          <LogOut size={18} />
          Sign out
        </button>
        {user && (
          <div className="px-3 pt-3 mt-2 border-t border-border-color">
            <p className="text-xs font-medium text-on-surface truncate">{user.first_name || user.email}</p>
            <p className="text-xs text-outline-variant truncate">{user.email}</p>
          </div>
        )}
      </div>
    </aside>
  );
};

export default Sidebar;
