import React, { useState, useEffect } from 'react';
import { apiClient } from '../../core/apiClient';
import { useAuthStore } from '../../core/authStore';
import AppLayout from '../../components/AppLayout';
import { Card } from '../../components/ui/Card';
import { StatCard, SectionHeader } from '../../components/ui/DataDisplay';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { Trophy, Zap, Award, Star, Crown } from 'lucide-react';

const rankColors: Record<number, string> = { 1: 'text-yellow-500', 2: 'text-gray-400', 3: 'text-amber-600' };
const RankIcon = ({ rank }: { rank: number }) => rank <= 3
  ? <Crown size={16} className={rankColors[rank]} />
  : <span className="text-sm font-semibold text-outline-variant">#{rank}</span>;

const GamificationPage: React.FC = () => {
  const { user } = useAuthStore();
  const [leaderboardData, setLeaderboardData] = useState<any[]>([]);
  const [challenges, setChallenges] = useState<any[]>([]);
  const [badgesData, setBadgesData] = useState<any[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [lbRes, chRes, bgRes] = await Promise.all([
          apiClient.get('/gamification/leaderboard'),
          apiClient.get('/gamification/challenges'),
          apiClient.get('/gamification/badges')
        ]);
        setLeaderboardData(lbRes.data);
        setChallenges(chRes.data);
        setBadgesData(bgRes.data);
      } catch (err) {
        console.error("Failed to fetch gamification data", err);
      }
    };
    fetchData();
  }, []);

  // Derive current user's XP and rank from leaderboard
  const myEntry = leaderboardData.find(e => e.employee_id === user?.id);
  const myXP = myEntry ? myEntry.total_xp : 0;
  const myRank = myEntry ? myEntry.rank : '-';

  return (
    <AppLayout>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Gamification</h1>
          <p className="text-sm text-outline-variant mt-0.5">Leaderboards, badges, challenges, and rewards</p>
        </div>
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatCard label="Your XP" value={myXP.toLocaleString()} icon={<Zap size={16} />} />
        <StatCard label="Badges Earned" value="0" icon={<Award size={16} />} />
        <StatCard label="Active Challenges" value={challenges.length.toString()} icon={<Trophy size={16} />} />
        <StatCard label="Your Rank" value={myRank === '-' ? '-' : `#${myRank}`} icon={<Star size={16} />} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* Leaderboard */}
        <Card className="p-6">
          <SectionHeader title="🏆 Leaderboard — Top Employees" action={
            <Button variant="secondary" size="sm">View All</Button>
          } />
          <div className="space-y-0 divide-y divide-border-color">
            {leaderboardData.length > 0 ? (
              leaderboardData.map((emp, index) => {
                const rank = emp.rank || index + 1;
                const name = emp.employee_name || emp.name || 'Anonymous';
                return (
                <div key={emp.employee_id || rank} className={`py-3 flex items-center gap-3 ${rank === 1 ? 'bg-yellow-50/50 -mx-6 px-6 rounded' : ''}`}>
                  <div className="w-6 flex items-center justify-center shrink-0">
                    <RankIcon rank={rank} />
                  </div>
                  <div className="w-7 h-7 rounded-full bg-primary-container/30 flex items-center justify-center shrink-0">
                    <span className="text-xs font-bold text-primary">{name.charAt(0)}</span>
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-on-surface leading-none">{name}</p>
                    <p className="text-xs text-outline-variant mt-0.5">{emp.dept || 'Employee'}</p>
                  </div>
                  <div className="text-right shrink-0">
                    <p className="text-sm font-bold text-on-surface">{(emp.total_xp || emp.xp || 0).toLocaleString()} XP</p>
                    <p className="text-xs text-brand-green">{emp.delta || ''}</p>
                  </div>
                </div>
              )})
            ) : (
              <div className="py-8 text-center text-outline-variant text-sm">
                No XP data available. Start completing activities to appear on the leaderboard!
              </div>
            )}
          </div>
        </Card>

        {/* Challenges */}
        <div className="space-y-4">
          <SectionHeader title="🎯 Active Challenges" />
          {challenges.length > 0 ? (
            challenges.map((ch) => (
              <Card key={ch.id} className="p-5">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h3 className="font-semibold text-on-surface text-sm">{ch.title}</h3>
                    <p className="text-xs text-outline-variant mt-0.5">{ch.participants || 0} participants · Ends {new Date(ch.end_date).toLocaleDateString()}</p>
                  </div>
                  <span className="text-sm font-bold text-brand-green shrink-0 ml-2">+{ch.xp_reward || ch.xp} XP</span>
                </div>
                <div className="flex items-center gap-3">
                  <div className="flex-1 h-1.5 bg-surface-container-high rounded-full">
                    <div className="h-full bg-brand-green rounded-full transition-all" style={{ width: `${ch.progress || 0}%` }} />
                  </div>
                  <span className="text-xs text-outline-variant w-8 text-right">{ch.progress || 0}%</span>
                </div>
                <div className="mt-3">
                  <Badge variant={ch.category === 'Environmental' ? 'success' : ch.category === 'Social' ? 'default' : 'warning'}>
                    {ch.category}
                  </Badge>
                </div>
              </Card>
            ))
          ) : (
            <Card className="p-8 text-center text-outline-variant text-sm flex items-center justify-center border-dashed">
              No active challenges available.
            </Card>
          )}
        </div>
      </div>

      {/* Badges */}
      <Card className="p-6">
        <SectionHeader title="🎖️ Available Badges" />
        {badgesData.length > 0 ? (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {badgesData.map((badge) => (
              <div key={badge.id || badge.name} className="flex flex-col items-center text-center p-4 rounded-card border border-border-color hover:border-brand-olive/40 transition-colors cursor-pointer">
                <span className="text-3xl mb-2">{badge.icon || '🏅'}</span>
                <p className="font-semibold text-sm text-on-surface">{badge.name}</p>
                <p className="text-xs text-outline-variant mt-1">{badge.description || badge.desc}</p>
                <Badge className="mt-3" variant="default">{badge.category}</Badge>
              </div>
            ))}
          </div>
        ) : (
          <div className="py-10 text-center text-outline-variant text-sm border border-dashed rounded-lg">
            No badges configured yet.
          </div>
        )}
      </Card>
    </AppLayout>
  );
};

export default GamificationPage;
