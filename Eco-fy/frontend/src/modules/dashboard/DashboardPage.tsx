import React, { useState, useEffect } from 'react';
import { apiClient } from '../../core/apiClient';
import AppLayout from '../../components/AppLayout';
import { Card } from '../../components/ui/Card';
import { StatCard, ProgressBar, SectionHeader } from '../../components/ui/DataDisplay';
import { Badge } from '../../components/ui/Badge';
import { Leaf, Users, Shield, TrendingDown, ChevronRight } from 'lucide-react';
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell
} from 'recharts';

const DashboardPage: React.FC = () => {
  const [data, setData] = useState<any>({
    carbonData: [],
    esgBreakdown: [],
    recentActivities: [],
    goals: [],
    kpis: null
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const res = await apiClient.get('/analytics/dashboard');
        setData(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboard();
  }, []);

  return (
    <AppLayout>
      {/* Page Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-on-surface">ESG Dashboard</h1>
          <p className="text-sm text-outline-variant mt-0.5">Organization-wide sustainability performance</p>
        </div>
        <Badge variant="success" className="text-xs px-3 py-1.5">FY 2025-26</Badge>
      </div>

      {/* KPI Row */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatCard label="ESG Score" value={data.kpis ? `${data.kpis.esg_score}/100` : '-'} icon={<Shield size={16} />} />
        <StatCard label="Total Carbon (YTD)" value={data.kpis ? `${data.kpis.total_co2e_tonnes} t` : '0 t'} icon={<Leaf size={16} />} />
        <StatCard label="Active Employees" value={data.kpis ? String(data.kpis.active_employees) : '-'} icon={<Users size={16} />} />
        <StatCard label="Open Issues" value={data.kpis ? String(data.kpis.open_issues) : '-'} icon={<TrendingDown size={16} />} />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        {/* Carbon Trend */}
        <Card className="lg:col-span-2 p-6">
          <SectionHeader title="Carbon Emissions Trend (tCO₂e)" />
          {data.carbonData && data.carbonData.length > 0 ? (
            <ResponsiveContainer width="100%" height={200}>
              <AreaChart data={data.carbonData}>
                <defs>
                  <linearGradient id="carbonGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#355C4D" stopOpacity={0.15} />
                    <stop offset="95%" stopColor="#355C4D" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#E3E4E6" />
                <XAxis dataKey="month" tick={{ fontSize: 11, fill: '#7a7582' }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fontSize: 11, fill: '#7a7582' }} axisLine={false} tickLine={false} />
                <Tooltip
                  contentStyle={{ border: '1px solid #E3E4E6', borderRadius: 8, fontSize: 12 }}
                  cursor={{ stroke: '#355C4D', strokeWidth: 1 }}
                />
                <Area type="monotone" dataKey="value" stroke="#355C4D" strokeWidth={2} fill="url(#carbonGrad)" />
              </AreaChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex items-center justify-center h-[200px] text-sm text-outline-variant border border-dashed rounded-lg">
              Data not available. Log carbon transactions to view trends.
            </div>
          )}
        </Card>

        {/* ESG Breakdown */}
        <Card className="p-6">
          <SectionHeader title="ESG Pillar Scores" />
          {data.esgBreakdown && data.esgBreakdown.length > 0 ? (
            <div className="flex flex-col items-center">
              <ResponsiveContainer width="100%" height={140}>
                <PieChart>
                  <Pie data={data.esgBreakdown} cx="50%" cy="50%" innerRadius={45} outerRadius={65} paddingAngle={3} dataKey="value">
                    {data.esgBreakdown.map((entry: any, i: number) => (
                      <Cell key={i} fill={entry.color} />
                    ))}
                  </Pie>
                </PieChart>
              </ResponsiveContainer>
              <div className="w-full space-y-2 mt-3">
                {data.esgBreakdown.map((item: any) => (
                  <div key={item.name} className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="w-2 h-2 rounded-full" style={{ backgroundColor: item.color }} />
                      <span className="text-xs text-on-surface-variant">{item.name}</span>
                    </div>
                    <span className="text-xs font-semibold text-on-surface">{item.value}</span>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="flex items-center justify-center h-48 text-sm text-outline-variant border border-dashed rounded-lg">
              Data not available.
            </div>
          )}
        </Card>
      </div>

      {/* Bottom Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Sustainability Goals */}
        <Card className="p-6">
          <SectionHeader title="Sustainability Goals" action={
            <button className="text-xs text-primary flex items-center gap-1 hover:underline">View all <ChevronRight size={12} /></button>
          } />
          {data.goals && data.goals.length > 0 ? (
            <div className="space-y-5">
              {data.goals.map((goal: any) => (
                <div key={goal.name}>
                  <div className="flex items-center justify-between mb-2">
                    <p className="text-sm font-medium text-on-surface">{goal.name}</p>
                    <span className="text-xs text-outline-variant">{goal.current}%</span>
                  </div>
                  <ProgressBar value={goal.current} />
                </div>
              ))}
            </div>
          ) : (
            <div className="py-10 text-center text-outline-variant text-sm border border-dashed rounded-lg">
              No sustainability goals configured yet.
            </div>
          )}
        </Card>

        {/* Recent Activity */}
        <Card className="p-6">
          <SectionHeader title="Employee Activity Feed" action={
            <button className="text-xs text-primary flex items-center gap-1 hover:underline">View all <ChevronRight size={12} /></button>
          } />
          {data.recentActivities && data.recentActivities.length > 0 ? (
            <div className="space-y-0 divide-y divide-border-color">
              {data.recentActivities.map((act: any) => (
                <div key={act.id} className="py-3 flex items-start gap-3">
                  <div className="w-7 h-7 rounded-full bg-primary-container/30 flex items-center justify-center shrink-0 mt-0.5">
                    <span className="text-xs font-bold text-primary">{act.user?.charAt(0) || '?'}</span>
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-on-surface font-medium leading-snug">{act.user}</p>
                    <p className="text-xs text-outline-variant truncate">{act.action}</p>
                  </div>
                  <div className="text-right shrink-0">
                    <p className="text-xs font-semibold text-brand-green">{act.xp}</p>
                    <p className="text-xs text-outline-variant">{act.time}</p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="py-10 text-center text-outline-variant text-sm border border-dashed rounded-lg">
              No recent activity.
            </div>
          )}
        </Card>
      </div>
    </AppLayout>
  );
};

export default DashboardPage;
