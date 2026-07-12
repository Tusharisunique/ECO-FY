import React from 'react';
import type { HTMLAttributes } from 'react';
import { cn } from './Button';

interface BadgeProps extends HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'success' | 'warning' | 'error';
}

export const Badge: React.FC<BadgeProps> = ({ className, variant = 'default', ...props }) => {
  const variants = {
    default: 'bg-canvas text-on-surface border-border-color',
    success: 'bg-brand-olive text-white border-transparent',
    warning: 'bg-brand-sand text-on-surface border-transparent',
    error: 'bg-error text-white border-transparent',
  };

  return (
    <div
      className={cn(
        'inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-brand-green focus:ring-offset-2',
        variants[variant],
        className
      )}
      {...props}
    />
  );
};
