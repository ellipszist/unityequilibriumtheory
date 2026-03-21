'use client';

import AppShell from '@/components/layout/AppShell';
import BentoGridLayout, { BentoCard } from '@/components/layout/BentoGridLayout';
import { CreditCard, TrendingUp, Users, Globe } from 'lucide-react';

const REVENUE_STREAMS = [
  { label: 'Pro Subscriptions', amount: '$58.0K', share: 57, color: 'bg-primary' },
  { label: 'Team Subscriptions', amount: '$27.9K', share: 27, color: 'bg-emerald-500' },
  { label: 'API Overage', amount: '$8.3K', share: 8, color: 'bg-blue-500' },
  { label: 'Marketplace Commission', amount: '$7.8K', share: 8, color: 'bg-amber-500' },
];

const MONTHLY = [
  { month: 'Oct', rev: 74 }, { month: 'Nov', rev: 81 }, { month: 'Dec', rev: 89 },
  { month: 'Jan', rev: 85 }, { month: 'Feb', rev: 95 }, { month: 'Mar', rev: 102 },
];

export default function EconomyBillingPage() {
  const maxRev = Math.max(...MONTHLY.map(m => m.rev));

  return (
    <AppShell>
      <BentoGridLayout columns={3}>

        <div className="col-span-1 sm:col-span-2 lg:col-span-3 rounded-xl border border-border bg-card px-5 py-4 flex items-center gap-3">
          <Globe size={18} className="text-primary shrink-0" />
          <div>
            <h1 className="font-bold text-sm">Billing & Revenue</h1>
            <p className="text-[11px] text-muted-foreground">Platform-wide income streams and growth metrics</p>
          </div>
        </div>

        {/* MRR — 2 cols */}
        <BentoCard span={2} className="bg-gradient-to-br from-primary/10 to-primary/5">
          <div className="flex items-center gap-2 mb-3">
            <CreditCard size={16} className="text-primary" />
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Monthly Recurring Revenue</span>
          </div>
          <div className="text-4xl font-bold mb-1">$102.0K</div>
          <p className="text-xs text-muted-foreground mb-4">March 2026 · <span className="text-emerald-500">+7.4% MoM</span></p>

          {/* Mini bar chart */}
          <div className="flex items-end gap-1.5 h-16">
            {MONTHLY.map(m => (
              <div key={m.month} className="flex-1 flex flex-col items-center gap-1">
                <div
                  className="w-full rounded-t-sm bg-primary/40"
                  style={{ height: `${(m.rev / maxRev) * 100}%` }}
                />
                <span className="text-[9px] text-muted-foreground">{m.month}</span>
              </div>
            ))}
          </div>
        </BentoCard>

        {/* Stats */}
        <BentoCard>
          <div className="flex items-center gap-2 mb-4">
            <TrendingUp size={16} className="text-primary" />
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Key Metrics</span>
          </div>
          <div className="space-y-3">
            {[
              { label: 'Paying users', value: '3,241' },
              { label: 'Avg revenue / user', value: '$31.47' },
              { label: 'Churn rate', value: '2.1%' },
              { label: 'Annual run rate', value: '$1.22M' },
            ].map(s => (
              <div key={s.label} className="flex justify-between items-center">
                <span className="text-xs text-muted-foreground">{s.label}</span>
                <span className="text-xs font-semibold">{s.value}</span>
              </div>
            ))}
          </div>
        </BentoCard>

        {/* Revenue breakdown — 2 cols */}
        <BentoCard span={2} className="flex flex-col">
          <div className="flex items-center gap-2 mb-4">
            <Users size={14} className="text-primary" />
            <h2 className="font-semibold text-sm">Revenue Streams</h2>
          </div>
          <div className="space-y-3">
            {REVENUE_STREAMS.map(s => (
              <div key={s.label}>
                <div className="flex justify-between text-xs mb-1">
                  <span>{s.label}</span>
                  <span className="font-semibold">{s.amount}</span>
                </div>
                <div className="bg-muted/40 rounded-full h-1.5 overflow-hidden">
                  <div className={`h-full ${s.color} rounded-full`} style={{ width: `${s.share}%` }} />
                </div>
              </div>
            ))}
          </div>
        </BentoCard>

        {/* Active subscribers */}
        <BentoCard>
          <div className="flex items-center gap-2 mb-4">
            <Users size={14} className="text-primary" />
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Subscribers</span>
          </div>
          <div className="space-y-3">
            {[
              { tier: 'Free', count: '12,400', color: 'text-muted-foreground' },
              { tier: 'Pro', count: '2,841', color: 'text-primary' },
              { tier: 'Team', count: '400', color: 'text-emerald-500' },
            ].map(t => (
              <div key={t.tier} className="flex justify-between items-center">
                <span className={`text-xs font-medium ${t.color}`}>{t.tier}</span>
                <span className="text-xs font-semibold">{t.count}</span>
              </div>
            ))}
          </div>
        </BentoCard>

      </BentoGridLayout>
    </AppShell>
  );
}
