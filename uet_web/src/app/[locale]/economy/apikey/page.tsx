'use client';

import AppShell from '@/components/layout/AppShell';
import BentoGridLayout, { BentoCard } from '@/components/layout/BentoGridLayout';
import { Key, Globe, Activity, TrendingUp } from 'lucide-react';

const ENDPOINTS = [
  { endpoint: '/api/chat', calls: '420M', share: 35, color: 'bg-primary' },
  { endpoint: '/api/compute', calls: '280M', share: 23, color: 'bg-blue-500' },
  { endpoint: '/api/feed', calls: '210M', share: 17, color: 'bg-emerald-500' },
  { endpoint: '/api/workspaces', calls: '150M', share: 12, color: 'bg-amber-500' },
  { endpoint: 'Other', calls: '140M', share: 13, color: 'bg-muted-foreground' },
];

export default function EconomyApikeyPage() {
  return (
    <AppShell>
      <BentoGridLayout columns={3}>

        <div className="col-span-1 sm:col-span-2 lg:col-span-3 rounded-xl border border-border bg-card px-5 py-4 flex items-center gap-3">
          <Globe size={18} className="text-primary shrink-0" />
          <div>
            <h1 className="font-bold text-sm">API Usage — Global View</h1>
            <p className="text-[11px] text-muted-foreground">System-wide API request volumes and endpoint analytics</p>
          </div>
        </div>

        {/* Total requests — 2 cols */}
        <BentoCard span={2} className="bg-gradient-to-br from-blue-500/10 to-indigo-500/5">
          <div className="flex items-center gap-2 mb-3">
            <Key size={16} className="text-primary" />
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Total API Calls</span>
          </div>
          <div className="text-4xl font-bold mb-1">1.2B</div>
          <p className="text-xs text-muted-foreground mb-4">This month · <span className="text-emerald-500">+18.7% MoM</span></p>
          <div className="grid grid-cols-3 gap-3">
            {[
              { label: 'Today', val: '42.1M' },
              { label: 'Peak/hr', val: '3.8M' },
              { label: 'Error rate', val: '0.04%' },
            ].map(s => (
              <div key={s.label} className="rounded-xl bg-muted/40 p-3">
                <div className="text-[10px] text-muted-foreground mb-1">{s.label}</div>
                <div className="font-bold text-sm">{s.val}</div>
              </div>
            ))}
          </div>
        </BentoCard>

        {/* Active keys */}
        <BentoCard>
          <div className="flex items-center gap-2 mb-4">
            <Activity size={16} className="text-primary" />
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Key Stats</span>
          </div>
          <div className="space-y-3">
            {[
              { label: 'Total API keys', val: '18,420' },
              { label: 'Active (30d)', val: '14,810' },
              { label: 'Revoked', val: '1,230' },
              { label: 'Avg calls/key', val: '65K' },
            ].map(s => (
              <div key={s.label} className="flex justify-between text-xs">
                <span className="text-muted-foreground">{s.label}</span>
                <span className="font-semibold">{s.val}</span>
              </div>
            ))}
          </div>
        </BentoCard>

        {/* Top endpoints — 2 cols */}
        <BentoCard span={2} className="flex flex-col">
          <div className="flex items-center gap-2 mb-4">
            <TrendingUp size={14} className="text-primary" />
            <h2 className="font-semibold text-sm">Top Endpoints</h2>
          </div>
          <div className="space-y-3">
            {ENDPOINTS.map(e => (
              <div key={e.endpoint}>
                <div className="flex justify-between text-xs mb-1">
                  <span className="font-mono">{e.endpoint}</span>
                  <span className="font-semibold text-muted-foreground">{e.calls}</span>
                </div>
                <div className="bg-muted/40 rounded-full h-1.5 overflow-hidden">
                  <div className={`h-full ${e.color} rounded-full`} style={{ width: `${e.share}%` }} />
                </div>
              </div>
            ))}
          </div>
        </BentoCard>

        {/* Rate limits */}
        <BentoCard>
          <div className="flex items-center gap-2 mb-4">
            <Key size={14} className="text-primary" />
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Rate Limits</span>
          </div>
          <div className="space-y-3">
            {[
              { tier: 'Free', limit: '100 req/min' },
              { tier: 'Pro', limit: '1,000 req/min' },
              { tier: 'Team', limit: '10,000 req/min' },
              { tier: 'Enterprise', limit: 'Custom' },
            ].map(t => (
              <div key={t.tier} className="flex justify-between text-xs">
                <span className="text-muted-foreground">{t.tier}</span>
                <span className="font-semibold">{t.limit}</span>
              </div>
            ))}
          </div>
        </BentoCard>

      </BentoGridLayout>
    </AppShell>
  );
}
