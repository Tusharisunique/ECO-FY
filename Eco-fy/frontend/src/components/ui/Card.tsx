import React from 'react';
import type { HTMLAttributes } from 'react';
import { cn } from './Button';

export const Card: React.FC<HTMLAttributes<HTMLDivElement>> = ({ className, ...props }) => {
  return (
    <div
      className={cn('rounded-card border border-border-color bg-white p-6', className)}
      {...props}
    />
  );
};
