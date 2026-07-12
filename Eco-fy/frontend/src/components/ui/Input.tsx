import React, { InputHTMLAttributes } from 'react';
import { cn } from './Button';

export const Input: React.FC<InputHTMLAttributes<HTMLInputElement>> = ({ className, ...props }) => {
  return (
    <input
      className={cn(
        'flex h-10 w-full rounded-input border border-border-color bg-transparent px-3 py-2 text-sm placeholder:text-outline-variant focus-visible:outline-none focus-visible:border-brand-green disabled:cursor-not-allowed disabled:opacity-50 transition-colors',
        className
      )}
      {...props}
    />
  );
};
