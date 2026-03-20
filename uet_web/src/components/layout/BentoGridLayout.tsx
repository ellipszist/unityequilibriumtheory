'use client';

import { ReactNode } from 'react';

interface BentoGridLayoutProps {
  children: ReactNode;
  columns?: 2 | 3 | 4;
  className?: string;
}

export default function BentoGridLayout({
  children,
  columns = 3,
  className = '',
}: BentoGridLayoutProps) {
  const colClass = {
    2: 'sm:grid-cols-2',
    3: 'sm:grid-cols-2 lg:grid-cols-3',
    4: 'sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4',
  }[columns];

  return (
    <div className={`h-[calc(100vh-56px)] overflow-y-auto ${className}`}>
      <div className={`grid grid-cols-1 ${colClass} gap-4 p-6 max-w-7xl mx-auto`}>
        {children}
      </div>
    </div>
  );
}

interface BentoCardProps {
  children: ReactNode;
  span?: 1 | 2;
  rowSpan?: 1 | 2;
  className?: string;
}

export function BentoCard({ children, span = 1, rowSpan = 1, className = '' }: BentoCardProps) {
  const spanClass = span === 2 ? 'sm:col-span-2' : '';
  const rowClass = rowSpan === 2 ? 'row-span-2' : '';

  return (
    <div className={`rounded-xl border border-border bg-card p-5 hover:border-primary/30 transition-colors ${spanClass} ${rowClass} ${className}`}>
      {children}
    </div>
  );
}
