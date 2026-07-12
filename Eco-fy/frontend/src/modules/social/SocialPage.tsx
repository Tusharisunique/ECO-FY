import React, { useState, useEffect, useRef } from 'react';
import AppLayout from '../../components/AppLayout';
import { Card } from '../../components/ui/Card';
import { StatCard, SectionHeader } from '../../components/ui/DataDisplay';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';
import { Users, Heart, CheckCircle, Clock, Plus, Upload, Image as ImageIcon } from 'lucide-react';
import { apiClient } from '../../core/apiClient';
import { useAuthStore } from '../../core/authStore';

const SocialPage: React.FC = () => {
  const { user } = useAuthStore();
  const isAdmin = user?.is_superuser;
  const [tab, setTab] = useState<'activities' | 'approvals'>('activities');
  
  // Activities state
  const [activities, setActivities] = useState<any[]>([]);
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({ title: '', category: '', xp_reward: 100 });
  
  // Participation state
  const [showJoinModal, setShowJoinModal] = useState(false);
  const [selectedActivity, setSelectedActivity] = useState<any>(null);
  const [joinData, setJoinData] = useState({ hours: 1, notes: '' });
  const [uploading, setUploading] = useState(false);
  const [uploadedUrl, setUploadedUrl] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Approvals state
  const [pendingApprovals, setPendingApprovals] = useState<any[]>([]);

  const fetchActivities = async () => {
    try {
      const res = await apiClient.get('/social/activities');
      setActivities(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const fetchPendingApprovals = async () => {
    if (!isAdmin) return;
    try {
      const res = await apiClient.get('/social/participations/pending');
      setPendingApprovals(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchActivities();
    if (isAdmin) {
      fetchPendingApprovals();
    }
  }, [isAdmin]);

  // Admin: Create Activity
  const handleCreateActivity = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await apiClient.post('/social/activities', {
        title: formData.title,
        category: formData.category,
        xp_reward: formData.xp_reward,
        is_active: true
      });
      setShowModal(false);
      setFormData({ title: '', category: '', xp_reward: 100 });
      fetchActivities();
    } catch (err) {
      console.error(err);
    }
  };

  // Employee: Upload Proof Image
  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);
      const res = await apiClient.post('/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setUploadedUrl(res.data.url);
    } catch (err) {
      console.error('Upload failed', err);
    } finally {
      setUploading(false);
    }
  };

  // Employee: Join Activity
  const handleJoinActivity = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await apiClient.post('/social/participations', {
        csr_activity_id: selectedActivity.id,
        employee_id: user?.id,
        hours_contributed: joinData.hours,
        notes: joinData.notes,
        evidence_url: uploadedUrl
      });
      setShowJoinModal(false);
      setSelectedActivity(null);
      setUploadedUrl('');
      setJoinData({ hours: 1, notes: '' });
      // Optionally show success toast
      alert("Participation submitted successfully!");
    } catch (err: any) {
      console.error(err);
      alert(err.response?.data?.detail || "Failed to submit participation");
    }
  };

  // Admin: Review Approval
  const handleReview = async (id: string, status: 'Approved' | 'Rejected') => {
    try {
      await apiClient.patch(`/social/participations/${id}/review`, { status, reviewed_by: user?.id });
      fetchPendingApprovals(); // Refresh list
    } catch (err: any) {
      console.error(err);
      alert(err.response?.data?.detail || "Failed to review participation");
    }
  };

  return (
    <AppLayout>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Social {isAdmin && '(Admin)'}</h1>
          <p className="text-sm text-outline-variant mt-0.5">CSR activities and employee participation</p>
        </div>
        {isAdmin && (
          <Button id="create-activity-btn" className="flex items-center gap-2" onClick={() => setShowModal(true)}>
            <Plus size={16} /> Create Activity
          </Button>
        )}
      </div>

      {/* Create Activity Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <Card className="p-6 w-full max-w-md bg-surface">
            <h2 className="text-xl font-bold mb-4">Create CSR Activity</h2>
            <form onSubmit={handleCreateActivity} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Title</label>
                <Input value={formData.title} onChange={e => setFormData({...formData, title: e.target.value})} placeholder="e.g. Park Cleanup" required />
              </div>
              <div className="flex gap-4">
                <div className="flex-1">
                  <label className="block text-sm font-medium mb-1">Category</label>
                  <Input value={formData.category} onChange={e => setFormData({...formData, category: e.target.value})} placeholder="Community" required />
                </div>
                <div className="flex-1">
                  <label className="block text-sm font-medium mb-1">XP Reward</label>
                  <Input type="number" value={formData.xp_reward} onChange={e => setFormData({...formData, xp_reward: parseInt(e.target.value)})} placeholder="100" required />
                </div>
              </div>
              <div className="flex justify-end gap-2 mt-6">
                <Button variant="secondary" type="button" onClick={() => setShowModal(false)}>Cancel</Button>
                <Button type="submit">Create Activity</Button>
              </div>
            </form>
          </Card>
        </div>
      )}

      {/* Join Activity Modal */}
      {showJoinModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <Card className="p-6 w-full max-w-md bg-surface">
            <h2 className="text-xl font-bold mb-4">Log Participation</h2>
            <p className="text-sm text-on-surface-variant mb-4">You are logging hours for <strong>{selectedActivity?.title}</strong></p>
            <form onSubmit={handleJoinActivity} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Hours Contributed</label>
                <Input type="number" min="0.5" step="0.5" value={joinData.hours} onChange={e => setJoinData({...joinData, hours: parseFloat(e.target.value)})} required />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Upload Proof (Photo)</label>
                <div className="flex items-center gap-4">
                  <Button type="button" variant="secondary" onClick={() => fileInputRef.current?.click()}>
                    <Upload size={16} className="mr-2" /> Upload Image
                  </Button>
                  <input type="file" ref={fileInputRef} className="hidden" accept="image/*" onChange={handleFileChange} />
                  {uploading && <span className="text-sm text-outline-variant">Uploading...</span>}
                  {uploadedUrl && <span className="text-sm text-brand-green flex items-center gap-1"><CheckCircle size={14} /> Uploaded</span>}
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Notes</label>
                <Input value={joinData.notes} onChange={e => setJoinData({...joinData, notes: e.target.value})} placeholder="Describe your contribution..." />
              </div>
              <div className="flex justify-end gap-2 mt-6">
                <Button variant="secondary" type="button" onClick={() => {setShowJoinModal(false); setUploadedUrl('');}}>Cancel</Button>
                <Button type="submit" disabled={uploading}>Submit for Approval</Button>
              </div>
            </form>
          </Card>
        </div>
      )}

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatCard label="Active CSR Activities" value={activities.length.toString()} icon={<Heart size={16} />} />
        <StatCard label="Total Participants" value="-" icon={<Users size={16} />} />
        <StatCard label="Volunteer Hours" value="0h" icon={<Clock size={16} />} />
        <StatCard label="Pending Approvals" value={isAdmin ? pendingApprovals.length.toString() : "-"} icon={<CheckCircle size={16} />} />
      </div>

      {/* Tabs */}
      <div className="flex gap-1 mb-6 p-1 bg-surface-container rounded-lg w-fit">
        <button
          onClick={() => setTab('activities')}
          className={`px-4 py-2 rounded-md text-sm font-medium capitalize transition-all ${tab === 'activities' ? 'bg-white text-on-surface shadow-sm' : 'text-on-surface-variant hover:text-on-surface'}`}
        >
          activities
        </button>
        {isAdmin && (
          <button
            onClick={() => setTab('approvals')}
            className={`px-4 py-2 rounded-md text-sm font-medium capitalize transition-all ${tab === 'approvals' ? 'bg-white text-on-surface shadow-sm' : 'text-on-surface-variant hover:text-on-surface'}`}
          >
            approvals <span className="ml-1 inline-flex items-center justify-center w-4 h-4 rounded-full bg-error text-white text-xs">{pendingApprovals.length}</span>
          </button>
        )}
      </div>

      {tab === 'activities' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {activities.map((act) => (
            <Card key={act.id} className="p-5 hover:border-brand-olive/40 transition-colors">
              <div className="flex items-start justify-between mb-3">
                <div>
                  <h3 className="font-semibold text-on-surface">{act.title}</h3>
                  <p className="text-xs text-outline-variant mt-0.5">{act.category}</p>
                </div>
                <Badge variant={act.is_active ? 'success' : 'warning'} className="shrink-0">
                  {act.is_active ? 'Active' : 'Inactive'}
                </Badge>
              </div>
              <div className="flex items-center justify-between pt-3 border-t border-border-color">
                <span className="text-sm font-bold text-brand-green">+{act.xp_reward} XP</span>
                {!isAdmin && (
                  <Button size="sm" variant="secondary" onClick={() => { setSelectedActivity(act); setShowJoinModal(true); }}>
                    Log Participation
                  </Button>
                )}
              </div>
            </Card>
          ))}
          {activities.length === 0 && (
            <div className="col-span-2 py-10 text-center text-outline-variant">
              No CSR activities found.
            </div>
          )}
        </div>
      )}

      {tab === 'approvals' && isAdmin && (
        <Card className="p-6">
          <SectionHeader title="Pending Approvals" />
          <div className="space-y-0 divide-y divide-border-color">
            {pendingApprovals.map((item) => (
              <div key={item.id} className="py-4 flex items-center gap-4">
                <div className="w-8 h-8 rounded-full bg-primary-container/30 flex items-center justify-center shrink-0">
                  <span className="text-xs font-bold text-primary">E</span>
                </div>
                <div className="flex-1">
                  <p className="text-sm font-medium text-on-surface">Employee ID: {item.employee_id.slice(0, 8)}</p>
                  <p className="text-xs text-outline-variant">Activity: {item.csr_activity_id.slice(0, 8)} · {item.hours_contributed}h</p>
                  {item.notes && <p className="text-xs text-on-surface-variant mt-1">"{item.notes}"</p>}
                </div>
                {item.evidence_url && (
                  <div className="shrink-0 text-center px-4">
                    <a href={`http://localhost:8000${item.evidence_url}`} target="_blank" rel="noreferrer" className="text-brand-green hover:underline flex flex-col items-center">
                      <ImageIcon size={18} className="mb-1" />
                      <span className="text-xs">View Proof</span>
                    </a>
                  </div>
                )}
                <div className="flex gap-2 shrink-0">
                  <Button onClick={() => handleReview(item.id, 'Rejected')} variant="secondary" size="sm" className="text-error hover:border-error/40">Reject</Button>
                  <Button onClick={() => handleReview(item.id, 'Approved')} size="sm">Approve</Button>
                </div>
              </div>
            ))}
            {pendingApprovals.length === 0 && (
              <div className="py-8 text-center text-outline-variant">No pending approvals.</div>
            )}
          </div>
        </Card>
      )}
    </AppLayout>
  );
};

export default SocialPage;
