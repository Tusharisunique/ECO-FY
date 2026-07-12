import React from 'react';
import { cn } from './Button';

interface StatCardProps {
  label: string;
  value: string | number;
  delta?: string;
  deltaPositive?: boolean;
  icon?: React.ReactNode;
  className?: string;
  isProgress?: boolean;
  progressValue?: number;
}

export const StatCard: React.FC<StatCardProps> = ({ label, value, delta, deltaPositive, icon, className, isProgress, progressValue }) => {
  return (
    <div className={cn('rounded-card border border-border-color bg-white p-6', className)}>
      <div className="flex items-start justify-between mb-3">
        <p className="text-xs font-semibold uppercase tracking-wider text-outline">{label}</p>
        {icon && <div className="text-outline-variant">{icon}</div>}
      </div>
      <p className="text-3xl font-bold tracking-tight text-on-surface">{value}</p>
      {delta && (
        <p className={cn('text-xs mt-2', deltaPositive ? 'text-brand-green' : 'text-error')}>
          {deltaPositive ? '↑' : '↓'} {delta}
        </p>
      )}
      {isProgress && progressValue !== undefined && (
        <div className="mt-4">
          <ProgressBar value={progressValue} />
        </div>
      )}
    </div>
  );
};

interface ProgressBarProps {
  value: number;
  max?: number;
  label?: string;
  className?: string;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({ value, max = 100, label, className }) => {
  const pct = Math.min(100, (value / max) * 100);
  return (
    <div className={className}>
      {label && <p className="text-xs text-outline-variant mb-1.5">{label}</p>}
      <div className="h-1.5 bg-surface-container-high rounded-full overflow-hidden">
        <div
          className="h-full bg-brand-green rounded-full transition-all duration-500"
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
};

interface SectionHeaderProps {
  title: string;
  action?: React.ReactNode;
}

export const SectionHeader: React.FC<SectionHeaderProps> = ({ title, action }) => (
  <div className="flex items-center justify-between mb-5">
    <h2 className="text-base font-semibold text-on-surface">{title}</h2>
    {action}
  </div>
);
