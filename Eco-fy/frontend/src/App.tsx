import { Routes, Route, Navigate } from 'react-router-dom';
import ProtectedRoute from './modules/auth/ProtectedRoute';
import LoginPage from './modules/auth/LoginPage';
import DashboardPage from './modules/dashboard/DashboardPage';
import EnvironmentalPage from './modules/environmental/EnvironmentalPage';
import SocialPage from './modules/social/SocialPage';
import GovernancePage from './modules/governance/GovernancePage';
import GamificationPage from './modules/gamification/GamificationPage';
import AnalyticsPage from './modules/analytics/AnalyticsPage';

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="/dashboard" element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
      <Route path="/environmental" element={<ProtectedRoute><EnvironmentalPage /></ProtectedRoute>} />
      <Route path="/social" element={<ProtectedRoute><SocialPage /></ProtectedRoute>} />
      <Route path="/governance" element={<ProtectedRoute><GovernancePage /></ProtectedRoute>} />
      <Route path="/gamification" element={<ProtectedRoute><GamificationPage /></ProtectedRoute>} />
      <Route path="/analytics" element={<ProtectedRoute><AnalyticsPage /></ProtectedRoute>} />
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}

export default App;
