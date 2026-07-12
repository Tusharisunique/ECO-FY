import React, { useState, useEffect } from 'react';
import AppLayout from '../../components/AppLayout';
import { Card } from '../../components/ui/Card';
import { StatCard, SectionHeader } from '../../components/ui/DataDisplay';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';
import { Shield, FileText, AlertTriangle, CheckCircle, Plus } from 'lucide-react';
import { apiClient } from '../../core/apiClient';

const severityVariant: Record<string, 'default' | 'success' | 'warning' | 'error'> = {
  Low: 'default', Medium: 'warning', High: 'error', Critical: 'error',
};

const GovernancePage: React.FC = () => {
  const [tab, setTab] = useState<'policies' | 'audits' | 'issues'>('policies');
  
  // Data State
  const [policies, setPolicies] = useState<any[]>([]);
  const [audits, setAudits] = useState<any[]>([]);
  const [issues, setIssues] = useState<any[]>([]);

  // Modal State
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({ title: '', category: '', version: '1.0' });

  const fetchData = async () => {
    try {
      const [polRes, audRes, issRes] = await Promise.all([
        apiClient.get('/governance/policies'),
        apiClient.get('/governance/audits'),
        apiClient.get('/governance/compliance-issues') // Assuming this endpoint handles empty query gracefully or needs audit_id
      ]);
      setPolicies(polRes.data);
      setAudits(audRes.data);
      // If compliance issues requires audit_id, we might need a different approach. But backend handles empty audit_id or we fetch all.
      // Wait, let's catch individual errors so one failing doesn't break the others.
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    const loadAll = async () => {
      try {
        const pRes = await apiClient.get('/governance/policies');
        setPolicies(pRes.data);
      } catch (e) { console.error("Failed to load policies"); }
      
      try {
        const aRes = await apiClient.get('/governance/audits');
        setAudits(aRes.data);
      } catch (e) { console.error("Failed to load audits"); }

      try {
        const iRes = await apiClient.get('/governance/compliance-issues');
        setIssues(iRes.data);
      } catch (e) { console.error("Failed to load issues"); }
    };
    loadAll();
  }, []);

  const handleCreatePolicy = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await apiClient.post('/governance/policies', {
        title: formData.title,
        category: formData.category,
        version: formData.version,
        effective_date: new Date().toISOString()
      });
      setShowModal(false);
      setFormData({ title: '', category: '', version: '1.0' });
      const pRes = await apiClient.get('/governance/policies');
      setPolicies(pRes.data);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <AppLayout>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Governance</h1>
          <p className="text-sm text-outline-variant mt-0.5">Policies, audits, and compliance management</p>
        </div>
        <Button id="add-policy-btn" className="flex items-center gap-2" onClick={() => setShowModal(true)}>
          <Plus size={16} /> Add Policy
        </Button>
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <Card className="p-6 w-full max-w-md bg-surface">
            <h2 className="text-xl font-bold mb-4">Create Policy</h2>
            <form onSubmit={handleCreatePolicy} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Title</label>
                <Input value={formData.title} onChange={e => setFormData({...formData, title: e.target.value})} placeholder="e.g. Code of Conduct" required />
              </div>
              <div className="flex gap-4">
                <div className="flex-1">
                  <label className="block text-sm font-medium mb-1">Category</label>
                  <Input value={formData.category} onChange={e => setFormData({...formData, category: e.target.value})} placeholder="Ethics" required />
                </div>
                <div className="flex-1">
                  <label className="block text-sm font-medium mb-1">Version</label>
                  <Input value={formData.version} onChange={e => setFormData({...formData, version: e.target.value})} placeholder="1.0" required />
                </div>
              </div>
              <div className="flex justify-end gap-2 mt-6">
                <Button variant="secondary" type="button" onClick={() => setShowModal(false)}>Cancel</Button>
                <Button type="submit">Create Policy</Button>
              </div>
            </form>
          </Card>
        </div>
      )}

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatCard label="Active Policies" value={policies.length.toString()} icon={<FileText size={16} />} />
        <StatCard label="Avg. Acknowledgement" value="0%" icon={<CheckCircle size={16} />} />
        <StatCard label="Scheduled Audits" value={audits.length.toString()} icon={<Shield size={16} />} />
        <StatCard label="Open Issues" value={issues.length.toString()} icon={<AlertTriangle size={16} />} />
      </div>

      <div className="flex gap-1 mb-6 p-1 bg-surface-container rounded-lg w-fit">
        {(['policies', 'audits', 'issues'] as const).map((t) => (
          <button key={t} id={`gov-tab-${t}`} onClick={() => setTab(t)}
            className={`px-4 py-2 rounded-md text-sm font-medium capitalize transition-all ${tab === t ? 'bg-white text-on-surface shadow-sm' : 'text-on-surface-variant hover:text-on-surface'}`}>
            {t}
          </button>
        ))}
      </div>

      {tab === 'policies' && (
        <Card className="p-6">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border-color">
                {['Policy', 'Category', 'Version', 'Acknowledgement', 'Status'].map(h => (
                  <th key={h} className="text-left pb-3 text-xs font-semibold uppercase tracking-wider text-outline pr-4">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-border-color">
              {policies.map(p => (
                <tr key={p.id} className="hover:bg-canvas transition-colors">
                  <td className="py-3 pr-4 font-medium">{p.title}</td>
                  <td className="py-3 pr-4 text-on-surface-variant">{p.category}</td>
                  <td className="py-3 pr-4 text-on-surface-variant">v{p.version}</td>
                  <td className="py-3 pr-4">
                    <div className="flex items-center gap-2">
                      <div className="flex-1 h-1.5 bg-surface-container-high rounded-full">
                        <div className="h-full bg-brand-green rounded-full" style={{ width: `0%` }} />
                      </div>
                      <span className="text-xs font-semibold w-8">0%</span>
                    </div>
                  </td>
                  <td className="py-3"><Badge variant={p.is_active ? 'success' : 'warning'}>{p.is_active ? 'Active' : 'Draft'}</Badge></td>
                </tr>
              ))}
              {policies.length === 0 && (
                <tr>
                  <td colSpan={5} className="py-8 text-center text-outline-variant">No policies created yet.</td>
                </tr>
              )}
            </tbody>
          </table>
        </Card>
      )}

      {tab === 'audits' && (
        <div className="space-y-4">
          {audits.length > 0 ? audits.map(a => (
            <Card key={a.id} className="p-5">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="font-semibold text-on-surface">{a.title}</h3>
                  <p className="text-xs text-outline-variant mt-0.5">Auditor: {a.auditor || 'Internal'} · {new Date(a.created_at).toLocaleDateString()}</p>
                </div>
                <Badge variant={a.status === 'Completed' ? 'success' : a.status === 'In Progress' ? 'warning' : 'default'}>
                  {a.status}
                </Badge>
              </div>
            </Card>
          )) : (
            <Card className="p-8 text-center text-outline-variant text-sm border border-dashed">
              No audits scheduled.
            </Card>
          )}
        </div>
      )}

      {tab === 'issues' && (
        <Card className="p-6">
          <SectionHeader title="Open Compliance Issues" />
          <div className="space-y-0 divide-y divide-border-color">
            {issues.length > 0 ? issues.map(issue => (
              <div key={issue.id} className="py-4 flex items-center gap-4">
                <Badge variant={severityVariant[issue.severity]} className="shrink-0 w-16 justify-center">{issue.severity}</Badge>
                <div className="flex-1">
                  <p className="text-sm font-medium text-on-surface">{issue.title}</p>
                  <p className="text-xs text-outline-variant">Due: {issue.due}</p>
                </div>
                <Badge variant={issue.status === 'In Progress' ? 'warning' : 'default'}>{issue.status}</Badge>
              </div>
            )) : (
              <div className="py-8 text-center text-outline-variant text-sm">
                No open compliance issues!
              </div>
            )}
          </div>
        </Card>
      )}
    </AppLayout>
  );
};

export default GovernancePage;

