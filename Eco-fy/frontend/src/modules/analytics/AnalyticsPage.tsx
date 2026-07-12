import React, { useEffect, useState } from 'react';
import AppLayout from '../../components/AppLayout';
import { Card } from '../../components/ui/Card';
import { StatCard, SectionHeader } from '../../components/ui/DataDisplay';
import { BarChart3, Sparkles, Leaf, Trophy, Users } from 'lucide-react';
import { apiClient } from '../../core/apiClient';
import { useAuthStore } from '../../core/authStore';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar
} from 'recharts';

const AnalyticsPage: React.FC = () => {
  const { user } = useAuthStore();
  const [insights, setInsights] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState({ esgTrend: [], radarData: [] });
  const isAdmin = user?.is_superuser;

  const fetchInsights = async () => {
    if (!isAdmin) return;
    setLoading(true);
    try {
      const res = await apiClient.get('/ai/insights');
      setInsights(res.data.insights);
    } catch (err) {
      console.error(err);
      setInsights('Failed to load AI insights. Check OpenRouter configuration.');
    }
    setLoading(false);
  };

  const fetchTrends = async () => {
    if (!isAdmin) return;
    try {
      const res = await apiClient.get('/analytics/trends');
      setData(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    if (isAdmin) {
      fetchInsights();
      fetchTrends();
    }
  }, [isAdmin]);

  if (!isAdmin) {
    return (
      <AppLayout>
        <div className="mb-8">
          <h1 className="text-2xl font-bold tracking-tight">Welcome, {user?.first_name || 'Employee'}!</h1>
          <p className="text-sm text-outline-variant mt-0.5">Here is your personal ESG impact dashboard.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <StatCard label="Total Carbon Logged" value="0 kg" icon={<Leaf size={16} />} />
          <StatCard label="CSR Activities Joined" value="0" icon={<Users size={16} />} />
          <StatCard label="Your XP" value="0" icon={<Trophy size={16} />} />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card className="p-6">
            <SectionHeader title="Your Recent Impact" />
            <div className="py-8 text-center text-outline-variant text-sm border border-dashed rounded-lg">
              No recent impact logged. Start contributing!
            </div>
          </Card>
          
          <Card className="p-6 bg-brand-green text-white border-none">
            <h3 className="font-bold text-lg mb-2">Want to level up?</h3>
            <p className="text-sm text-white/80 mb-6">
              Check the gamification tab to see current challenges and earn more XP by participating in our corporate sustainability goals.
            </p>
            <button className="bg-white text-brand-green px-4 py-2 rounded-md font-semibold text-sm">
              View Challenges
            </button>
          </Card>
        </div>
      </AppLayout>
    );
  }

  return (
    <AppLayout>
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Analytics</h1>
          <p className="text-sm text-outline-variant mt-0.5">Executive ESG performance intelligence</p>
        </div>
        <button onClick={fetchInsights} disabled={loading} className="flex items-center gap-2 bg-primary text-on-primary px-4 py-2 rounded-md font-medium text-sm disabled:opacity-50 transition-colors hover:bg-primary/90">
          <Sparkles size={16} />
          {loading ? 'Generating...' : 'Refresh AI Insights'}
        </button>
      </div>

      <Card className="p-6 mb-8 bg-surface-container-low border border-primary/20">
        <div className="flex items-center gap-2 mb-3">
          <Sparkles size={18} className="text-primary" />
          <h2 className="font-semibold text-on-surface">ESG executive summary</h2>
        </div>
        <div className="text-sm text-on-surface-variant leading-relaxed whitespace-pre-wrap">
          {loading ? 'Generating insights...' : (insights || 'Click refresh to generate AI insights.')}
        </div>
      </Card>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatCard label="Overall ESG Score" value="-" icon={<BarChart3 size={16} />} />
        <StatCard label="Environmental" value="-" />
        <StatCard label="Social" value="-" />
        <StatCard label="Governance" value="-" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="p-6">
          <SectionHeader title="ESG Score Trend (E, S, G)" />
          {data.esgTrend && data.esgTrend.length > 0 ? (
            <ResponsiveContainer width="100%" height={240}>
              <LineChart data={data.esgTrend}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E3E4E6" />
                <XAxis dataKey="month" tick={{ fontSize: 11, fill: '#7a7582' }} axisLine={false} tickLine={false} />
                <YAxis domain={[60, 100]} tick={{ fontSize: 11, fill: '#7a7582' }} axisLine={false} tickLine={false} />
                <Tooltip contentStyle={{ border: '1px solid #E3E4E6', borderRadius: 8, fontSize: 12 }} />
                <Line type="monotone" dataKey="e" stroke="#355C4D" strokeWidth={2} dot={false} name="Environmental" />
                <Line type="monotone" dataKey="s" stroke="#7A8B68" strokeWidth={2} dot={false} name="Social" />
                <Line type="monotone" dataKey="g" stroke="#D8C7A3" strokeWidth={2} dot={false} name="Governance" />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex items-center justify-center h-[240px] text-sm text-outline-variant border border-dashed rounded-lg">
              Data not available. Log data across modules to generate trends.
            </div>
          )}
        </Card>

        <Card className="p-6">
          <SectionHeader title="ESG Materiality Radar" />
          {data.radarData && data.radarData.length > 0 ? (
            <ResponsiveContainer width="100%" height={240}>
              <RadarChart data={data.radarData}>
                <PolarGrid stroke="#E3E4E6" />
                <PolarAngleAxis dataKey="subject" tick={{ fontSize: 11, fill: '#7a7582' }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{ fontSize: 10, fill: '#7a7582' }} />
                <Radar name="Score" dataKey="score" stroke="#355C4D" fill="#355C4D" fillOpacity={0.15} strokeWidth={2} />
              </RadarChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex items-center justify-center h-[240px] text-sm text-outline-variant border border-dashed rounded-lg">
              Data not available.
            </div>
          )}
        </Card>
      </div>
    </AppLayout>
  );
};

export default AnalyticsPage;
