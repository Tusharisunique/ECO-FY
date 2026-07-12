import React, { useState, useEffect } from 'react';
import AppLayout from '../../components/AppLayout';
import { Card } from '../../components/ui/Card';
import { StatCard, SectionHeader } from '../../components/ui/DataDisplay';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';
import { Leaf, Plus, Zap, Car } from 'lucide-react';
import { apiClient } from '../../core/apiClient';
import { useAuthStore } from '../../core/authStore';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend
} from 'recharts';

const EnvironmentalPage: React.FC = () => {
  const [transactions, setTransactions] = useState<any[]>([]);
  const [emissionsByScope, setEmissionsByScope] = useState<any[]>([]);
  const [topCategories, setTopCategories] = useState<any[]>([]);
  const [summary, setSummary] = useState({ total_co2e_tonnes: 0 });
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({
    activity_type: '',
    quantity: '',
    unit: '',
    description: '',
  });

  const fetchData = async () => {
    try {
      const res = await apiClient.get('/environmental/carbon-transactions');
      const txs = res.data;
      setTransactions(txs);
      
      // Compute Emissions by Scope dynamically
      let s1 = 0, s2 = 0, s3 = 0;
      txs.forEach((t: any) => {
        if (t.activity_type.includes('Scope 1')) s1 += t.co2e_kg;
        else if (t.activity_type.includes('Scope 2')) s2 += t.co2e_kg;
        else if (t.activity_type.includes('Scope 3')) s3 += t.co2e_kg;
      });
      setEmissionsByScope([{ scope: 'Emissions', scope1: s1 / 1000, scope2: s2 / 1000, scope3: s3 / 1000 }]);

      // Compute Top Categories dynamically
      const catMap: Record<string, number> = {};
      let totalEmissions = 0;
      txs.forEach((t: any) => {
        catMap[t.activity_type] = (catMap[t.activity_type] || 0) + t.co2e_kg;
        totalEmissions += t.co2e_kg;
      });
      const topCats = Object.entries(catMap)
        .map(([category, kg]) => ({
          category,
          kg: `${(kg / 1000).toFixed(1)} t`,
          pct: totalEmissions > 0 ? (kg / totalEmissions) * 100 : 0
        }))
        .sort((a, b) => b.pct - a.pct)
        .slice(0, 3);
      setTopCategories(topCats);
      
      const sumRes = await apiClient.get('/environmental/carbon-summary');
      if (sumRes.data) {
        setSummary(sumRes.data);
      }
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const payload = {
        organization_id: null,
        employee_id: useAuthStore.getState().user?.id,
        activity_type: formData.activity_type,
        quantity: parseFloat(formData.quantity),
        unit: formData.unit,
        description: formData.description,
        activity_date: new Date().toISOString()
      };
      await apiClient.post('/environmental/carbon-transactions', payload);
      setShowModal(false);
      setFormData({ activity_type: '', quantity: '', unit: '', description: '' });
      fetchData();
    } catch (err: any) {
      console.error(err);
      alert(err?.response?.data?.detail || "Failed to log emission. Please try again.");
    }
  };

  return (
    <AppLayout>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Environmental Dashboard</h1>
          <p className="text-sm text-outline-variant mt-0.5">Track your carbon footprint and energy usage</p>
        </div>
        <Button id="log-emission-btn" className="flex items-center gap-2" onClick={() => setShowModal(true)}>
          <Plus size={16} /> Log Emission
        </Button>
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <Card className="p-6 w-full max-w-md bg-surface">
            <h2 className="text-xl font-bold mb-4">Log Carbon Emission</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Activity Type</label>
                <Input value={formData.activity_type} onChange={e => setFormData({...formData, activity_type: e.target.value})} placeholder="e.g. Scope 1: Fleet" required />
              </div>
              <div className="flex gap-4">
                <div className="flex-1">
                  <label className="block text-sm font-medium mb-1">Quantity</label>
                  <Input type="number" min="0" step="any" value={formData.quantity} onChange={e => setFormData({...formData, quantity: e.target.value})} placeholder="0" required />
                </div>
                <div className="flex-1">
                  <label className="block text-sm font-medium mb-1">Unit</label>
                  <Input value={formData.unit} onChange={e => setFormData({...formData, unit: e.target.value})} placeholder="liters, kWh" required />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Description</label>
                <Input value={formData.description} onChange={e => setFormData({...formData, description: e.target.value})} placeholder="Brief description" />
              </div>
              <div className="flex justify-end gap-2 mt-6">
                <Button variant="secondary" type="button" onClick={() => setShowModal(false)}>Cancel</Button>
                <Button type="submit">Save Emission</Button>
              </div>
            </form>
          </Card>
        </div>
      )}

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatCard label="Total Footprint (YTD)" value={`${summary.total_co2e_tonnes} t`} icon={<Leaf size={16} />} />
        <StatCard label="Scope 1 Emissions" value={`${emissionsByScope[0]?.scope1?.toFixed(2) ?? 0} t`} icon={<Car size={16} />} />
        <StatCard label="Scope 2 Emissions" value={`${emissionsByScope[0]?.scope2?.toFixed(2) ?? 0} t`} icon={<Zap size={16} />} />
        <StatCard label="Net-Zero Progress" value="0%" isProgress progressValue={0} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <Card className="p-6 lg:col-span-2">
          <SectionHeader title="Emissions by Scope (tCO2e)" />
          {emissionsByScope.length > 0 ? (
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={emissionsByScope} margin={{ top: 20, right: 30, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E3E4E6" />
                <XAxis dataKey="scope" tick={{ fontSize: 12, fill: '#7a7582' }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fontSize: 12, fill: '#7a7582' }} axisLine={false} tickLine={false} />
                <Tooltip cursor={{ fill: '#F0F1F0' }} contentStyle={{ borderRadius: 8, border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
                <Legend iconType="circle" wrapperStyle={{ fontSize: 12, paddingTop: 10 }} />
                <Bar dataKey="scope1" name="Scope 1 (Direct)" stackId="a" fill="#355C4D" radius={[0, 0, 4, 4]} />
                <Bar dataKey="scope2" name="Scope 2 (Energy)" stackId="a" fill="#7A8B68" />
                <Bar dataKey="scope3" name="Scope 3 (Value Chain)" stackId="a" fill="#D8C7A3" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex items-center justify-center h-64 text-sm text-outline-variant border border-dashed rounded-lg">
              Data not available. Log more carbon transactions to populate this chart.
            </div>
          )}
        </Card>
        
        {/* Emission Factors */}
        <Card className="p-6">
          <SectionHeader title="Top Emission Categories" />
          {topCategories.length > 0 ? (
            <div className="space-y-4">
              {topCategories.map((item) => (
                <div key={item.category}>
                  <div className="flex justify-between text-sm mb-1.5">
                    <span className="text-on-surface-variant">{item.category}</span>
                    <span className="font-semibold text-on-surface">{item.kg}</span>
                  </div>
                  <div className="h-1.5 bg-surface-container-high rounded-full">
                    <div className="h-full bg-brand-green rounded-full" style={{ width: `${item.pct}%` }} />
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="flex items-center justify-center h-48 text-sm text-outline-variant border border-dashed rounded-lg">
              Data not available.
            </div>
          )}
        </Card>
      </div>

      <Card className="p-6">
        <SectionHeader title="Recent Carbon Transactions" action={
          <Button variant="secondary" size="sm">Export CSV</Button>
        } />
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead>
              <tr className="border-b border-border-color text-outline uppercase tracking-wider text-xs">
                <th className="py-3 font-semibold">Date</th>
                <th className="py-3 font-semibold">Activity Type</th>
                <th className="py-3 font-semibold">Description</th>
                <th className="py-3 font-semibold text-right">Quantity</th>
                <th className="py-3 font-semibold text-right">CO2e (kg)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border-color">
              {transactions.map((tx) => (
                <tr key={tx.id} className="hover:bg-canvas transition-colors">
                  <td className="py-3 whitespace-nowrap text-on-surface-variant">
                    {new Date(tx.activity_date).toLocaleDateString()}
                  </td>
                  <td className="py-3">
                    <Badge variant={tx.activity_type.includes('Scope 1') ? 'default' : tx.activity_type.includes('Scope 2') ? 'warning' : 'success'}>
                      {tx.activity_type}
                    </Badge>
                  </td>
                  <td className="py-3 text-on-surface font-medium truncate max-w-xs">{tx.description}</td>
                  <td className="py-3 text-right text-on-surface-variant">{tx.quantity} {tx.unit}</td>
                  <td className="py-3 text-right font-semibold text-on-surface text-error">{tx.co2e_kg?.toLocaleString(undefined, {maximumFractionDigits: 1}) || 0}</td>
                </tr>
              ))}
            </tbody>
          </table>
          {transactions.length === 0 && (
            <div className="py-8 text-center text-outline-variant text-sm border border-dashed">
              No transactions logged yet. Click "Log Emission" to add one!
            </div>
          )}
        </div>
      </Card>
    </AppLayout>
  );
};

export default EnvironmentalPage;
