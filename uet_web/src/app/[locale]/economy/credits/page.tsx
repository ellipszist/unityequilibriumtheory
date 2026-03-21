'use client';

import AppShell from '@/components/layout/AppShell';
import BentoGridLayout, { BentoCard } from '@/components/layout/BentoGridLayout';
import { Coins, TrendingUp, Zap, Globe } from 'lucide-react';

const CREDIT_POOLS = [
  { label: 'Free Tier Allocation', credits: '6,200,000', share: 40, color: 'bg-muted-foreground' },
  { label: 'Pro Tier Allocation', credits: '14,205,000', share: 92, color: 'bg-primary' },
  { label: 'Mining Rewards Pool', credits: '3,680,000', share: 24, color: 'bg-amber-500' },
  { label: 'Research Grants', credits: '500,000', share: 3, color: 'bg-emerald-500' },
];

const TOP_CONSUMERS = [
  { name: 'WorkChat (GPT-4o)', daily: '420K', color: 'bg-primary' },
  { name: 'WorkChat (Claude 3.5)', daily: '280K', color: 'bg-blue-500' },
  { name: 'Batch Analysis Jobs', daily: '190K', color: 'bg-amber-500' },
  { name: 'API Direct Calls', daily: '150K', color: 'bg-emerald-500' },
];

export default function EconomyCreditsPage() {
  return (
    <AppShell>
      <BentoGridLayout columns={3}>

        <div className="col-span-1 sm:col-span-2 lg:col-span-3 rounded-xl border border-border bg-card px-5 py-4 flex items-center gap-3">
          <Globe size={18} className="text-primary shrink-0" />
          <div>
            <h1 className="font-bold text-sm">Credit System</h1>
            <p className="text-[11px] text-muted-foreground">AI compute energy flow — system-wide credit circulation</p>
          </div>
        </div>

        {/* Total supply — 2 cols */}
        <BentoCard span={2} className="bg-gradient-to-br from-amber-500/10 to-yellow-500/5">
          <div className="flex items-center gap-2 mb-3">
            <Coins size={16} className="text-primary" />
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Credits in Circulation</span>
          </div>
          <div className="text-4xl font-bold mb-1">48.2M</div>
          <p className="text-xs text-muted-foreground mb-4">Total issued · <span className="text-red-400">-2.0% MoM</span></p>
          <div className="grid grid-cols-3 gap-3">
            {[
              { label: 'Issued this month', val: '4.2M' },
              { label: 'Consumed', val: '4.5M' },
              { label: 'Net change', val: '-300K' },
            ].map(s => (
              <div key={s.label} className="rounded-xl bg-muted/40 p-3">
                <div className="text-[10px] text-muted-foreground mb-1">{s.label}</div>
                <div className="font-bold text-sm">{s.val}</div>
              </div>
            ))}
          </div>
        </BentoCard>

        {/* Exchange rate */}
        <BentoCard>
          <div className="flex items-center gap-2 mb-4">
            <TrendingUp size={16} className="text-primary" />
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Exchange Rate</span>
          </div>
          <div className="text-3xl font-bold mb-1">100</div>
          <div className="text-xs text-muted-foreground mb-4">credits per $1.00 USD</div>
          <div className="border-t border-border pt-3 space-y-2">
            {[
              { label: 'Free tier monthly', val: '500 cr' },
              { label: 'Pro tier monthly', val: '5,000 cr' },
              { label: 'Team tier monthly', val: '25,000 cr' },
            ].map(s => (
              <div key={s.label} className="flex justify-between text-xs">
                <span className="text-muted-foreground">{s.label}</span>
                <span className="font-semibold">{s.val}</span>
              </div>
            ))}
          </div>
        </BentoCard>

        {/* Credit pools — 2 cols */}
        <BentoCard span={2} className="flex flex-col">
          <div className="flex items-center gap-2 mb-4">
            <Coins size={14} className="text-primary" />
            <h2 className="font-semibold text-sm">Credit Pools</h2>
          </div>
          <div className="space-y-3">
            {CREDIT_POOLS.map(p => (
              <div key={p.label}>
                <div className="flex justify-between text-xs mb-1">
                  <span>{p.label}</span>
                  <span className="font-semibold text-muted-foreground">{p.credits}</span>
                </div>
                <div className="bg-muted/40 rounded-full h-1.5 overflow-hidden">
                  <div className={`h-full ${p.color} rounded-full`} style={{ width: `${p.share}%` }} />
                </div>
              </div>
            ))}
          </div>
        </BentoCard>

        {/* Top consumers */}
        <BentoCard>
          <div className="flex items-center gap-2 mb-4">
            <Zap size={14} className="text-amber-500" />
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Top Consumers</span>
          </div>
          <div className="space-y-3">
            {TOP_CONSUMERS.map((c, i) => (
              <div key={c.name} className="flex items-center gap-2">
                <span className="text-[10px] text-muted-foreground/50 w-3">{i + 1}</span>
                <div className="w-2 h-2 rounded-full shrink-0" style={{ backgroundColor: undefined }}>
                  <div className={`w-2 h-2 rounded-full ${c.color}`} />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="text-xs truncate">{c.name}</div>
                </div>
                <span className="text-xs font-semibold shrink-0">{c.daily}/d</span>
              </div>
            ))}
          </div>
        </BentoCard>

      </BentoGridLayout>
    </AppShell>
  );
}
