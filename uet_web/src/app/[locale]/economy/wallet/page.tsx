'use client';

import AppShell from '@/components/layout/AppShell';
import BentoGridLayout, { BentoCard } from '@/components/layout/BentoGridLayout';
import { Wallet, TrendingUp, ArrowDownLeft, ArrowUpRight, Globe } from 'lucide-react';

const FLOW_DATA = [
  { label: 'Subscription revenue', amount: '+$94.2K', dir: 'in', date: 'Mar 2026' },
  { label: 'Mining rewards issued', amount: '-$18.4K', dir: 'out', date: 'Mar 2026' },
  { label: 'API compute cost', amount: '-$31.0K', dir: 'out', date: 'Mar 2026' },
  { label: 'Marketplace commission', amount: '+$7.8K', dir: 'in', date: 'Mar 2026' },
  { label: 'Infrastructure costs', amount: '-$22.1K', dir: 'out', date: 'Mar 2026' },
];

export default function EconomyWalletPage() {
  return (
    <AppShell>
      <BentoGridLayout columns={3}>

        {/* Header */}
        <div className="col-span-1 sm:col-span-2 lg:col-span-3 rounded-xl border border-border bg-card px-5 py-4 flex items-center gap-3">
          <Globe size={18} className="text-primary shrink-0" />
          <div>
            <h1 className="font-bold text-sm">Global Treasury</h1>
            <p className="text-[11px] text-muted-foreground">System-wide wallet — transparent reserve overview</p>
          </div>
        </div>

        {/* Total reserve — 2 cols */}
        <BentoCard span={2} className="bg-gradient-to-br from-emerald-500/10 to-green-500/5">
          <div className="flex items-center gap-2 mb-3">
            <Wallet size={16} className="text-primary" />
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Total Reserve</span>
          </div>
          <div className="text-4xl font-bold mb-1">$2,400,000</div>
          <p className="text-xs text-muted-foreground mb-4">System Treasury & Reserves</p>
          <div className="grid grid-cols-2 gap-3">
            <div className="rounded-xl bg-muted/40 p-3">
              <div className="text-[10px] text-muted-foreground mb-1">Operating Reserve</div>
              <div className="font-bold">$1,200,000</div>
            </div>
            <div className="rounded-xl bg-muted/40 p-3">
              <div className="text-[10px] text-muted-foreground mb-1">Growth Fund</div>
              <div className="font-bold">$1,200,000</div>
            </div>
          </div>
        </BentoCard>

        {/* Monthly P&L */}
        <BentoCard>
          <div className="flex items-center gap-2 mb-3">
            <TrendingUp size={16} className="text-primary" />
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Monthly P&L</span>
          </div>
          <div className="space-y-2 mt-2">
            <div>
              <div className="text-[10px] text-muted-foreground">Revenue</div>
              <div className="text-xl font-bold text-emerald-500">+$102.0K</div>
            </div>
            <div>
              <div className="text-[10px] text-muted-foreground">Expenses</div>
              <div className="text-xl font-bold text-red-400">-$71.5K</div>
            </div>
            <div className="border-t border-border pt-2">
              <div className="text-[10px] text-muted-foreground">Net</div>
              <div className="text-xl font-bold">+$30.5K</div>
            </div>
          </div>
        </BentoCard>

        {/* Cash flow — spans 2 cols */}
        <BentoCard span={2} className="flex flex-col">
          <h2 className="font-semibold text-sm mb-4">Cash Flow (Mar 2026)</h2>
          <div className="space-y-2">
            {FLOW_DATA.map(f => (
              <div key={f.label} className="flex items-center gap-3">
                <div className={`w-6 h-6 rounded-full flex items-center justify-center shrink-0 ${f.dir === 'in' ? 'bg-emerald-500/10' : 'bg-red-500/10'}`}>
                  {f.dir === 'in' ? <ArrowDownLeft size={12} className="text-emerald-500" /> : <ArrowUpRight size={12} className="text-red-400" />}
                </div>
                <div className="flex-1 text-xs">{f.label}</div>
                <div className={`text-xs font-semibold ${f.dir === 'in' ? 'text-emerald-500' : 'text-foreground'}`}>{f.amount}</div>
              </div>
            ))}
          </div>
        </BentoCard>

        {/* Reserve ratio */}
        <BentoCard>
          <div className="flex items-center gap-2 mb-4">
            <Wallet size={14} className="text-primary" />
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Reserve Ratio</span>
          </div>
          <div className="text-3xl font-bold mb-2">87.4%</div>
          <p className="text-xs text-muted-foreground mb-3">Above 80% target</p>
          <div className="bg-muted/40 rounded-full h-2 overflow-hidden">
            <div className="h-full bg-emerald-500 rounded-full" style={{ width: '87.4%' }} />
          </div>
          <div className="flex justify-between text-[10px] text-muted-foreground mt-1">
            <span>0%</span><span>Target: 80%</span><span>100%</span>
          </div>
        </BentoCard>

      </BentoGridLayout>
    </AppShell>
  );
}
