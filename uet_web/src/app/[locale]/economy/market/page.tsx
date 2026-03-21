'use client';

import AppShell from '@/components/layout/AppShell';
import BentoGridLayout, { BentoCard } from '@/components/layout/BentoGridLayout';
import { Store, Bot, FileText, TrendingUp, Globe, Star } from 'lucide-react';

const TOP_ITEMS = [
  { name: 'Physics Simulation Agent', type: 'Agent', seller: 'UET Labs', sales: 840, rating: 4.9 },
  { name: 'Thermodynamics Prompt Pack', type: 'Prompt', seller: 'Dr. Beta', sales: 612, rating: 4.8 },
  { name: 'AI Alignment Benchmarks', type: 'Dataset', seller: 'MIT Group', sales: 390, rating: 4.7 },
  { name: 'Code Review Agent v3', type: 'Agent', seller: 'CodeLab', sales: 280, rating: 4.6 },
  { name: 'Research Summary Bot', type: 'Agent', seller: 'ResearchAI', sales: 210, rating: 4.5 },
];

const CATEGORIES = [
  { label: 'AI Agents', count: 142, share: 45, color: 'bg-primary' },
  { label: 'Prompt Packs', count: 95, share: 30, color: 'bg-blue-500' },
  { label: 'Datasets', count: 48, share: 15, color: 'bg-emerald-500' },
  { label: 'Fine-tuned Models', count: 27, share: 10, color: 'bg-amber-500' },
];

export default function EconomyMarketPage() {
  return (
    <AppShell>
      <BentoGridLayout columns={3}>

        <div className="col-span-1 sm:col-span-2 lg:col-span-3 rounded-xl border border-border bg-card px-5 py-4 flex items-center gap-3">
          <Globe size={18} className="text-primary shrink-0" />
          <div>
            <h1 className="font-bold text-sm">Marketplace</h1>
            <p className="text-[11px] text-muted-foreground">Platform-wide agent, prompt, and model trading ecosystem</p>
          </div>
        </div>

        {/* Overview — 2 cols */}
        <BentoCard span={2} className="bg-gradient-to-br from-violet-500/10 to-purple-500/5">
          <div className="flex items-center gap-2 mb-3">
            <Store size={16} className="text-primary" />
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Marketplace Overview</span>
          </div>
          <div className="grid grid-cols-4 gap-4 mb-4">
            {[
              { label: 'Total Listings', value: '312' },
              { label: 'Active Sellers', value: '184' },
              { label: 'Sales (30d)', value: '2,431' },
              { label: 'Commission (30d)', value: '$7.8K' },
            ].map(s => (
              <div key={s.label}>
                <div className="text-xl font-bold">{s.value}</div>
                <div className="text-[11px] text-muted-foreground">{s.label}</div>
              </div>
            ))}
          </div>
          <div className="flex items-center gap-2 text-xs text-emerald-500">
            <TrendingUp size={11} /> +24.1% listings growth MoM
          </div>
        </BentoCard>

        {/* Category breakdown */}
        <BentoCard>
          <div className="flex items-center gap-2 mb-4">
            <Bot size={14} className="text-primary" />
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">By Category</span>
          </div>
          <div className="space-y-3">
            {CATEGORIES.map(c => (
              <div key={c.label}>
                <div className="flex justify-between text-xs mb-1">
                  <span>{c.label}</span>
                  <span className="text-muted-foreground">{c.count}</span>
                </div>
                <div className="bg-muted/40 rounded-full h-1.5 overflow-hidden">
                  <div className={`h-full ${c.color} rounded-full`} style={{ width: `${c.share}%` }} />
                </div>
              </div>
            ))}
          </div>
        </BentoCard>

        {/* Top items — 2 cols */}
        <BentoCard span={2} className="flex flex-col">
          <div className="flex items-center gap-2 mb-4">
            <TrendingUp size={14} className="text-primary" />
            <h2 className="font-semibold text-sm">Top Listings (30d)</h2>
          </div>
          <div className="space-y-2">
            {TOP_ITEMS.map((item, i) => (
              <div key={item.name} className="flex items-center gap-3">
                <span className="text-[10px] text-muted-foreground/50 w-4 shrink-0">{i + 1}</span>
                <div className="w-7 h-7 rounded-lg bg-primary/10 flex items-center justify-center shrink-0">
                  {item.type === 'Agent' ? <Bot size={13} className="text-primary" /> : <FileText size={13} className="text-primary" />}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="text-xs font-medium truncate">{item.name}</div>
                  <div className="text-[10px] text-muted-foreground">{item.type} · {item.seller}</div>
                </div>
                <div className="text-right shrink-0">
                  <div className="text-xs font-semibold">{item.sales} sales</div>
                  <div className="flex items-center gap-0.5 justify-end text-[10px] text-amber-500">
                    <Star size={9} className="fill-amber-500" /> {item.rating}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </BentoCard>

        {/* Payout stats */}
        <BentoCard>
          <div className="flex items-center gap-2 mb-4">
            <TrendingUp size={14} className="text-primary" />
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Seller Payouts</span>
          </div>
          <div className="space-y-3">
            {[
              { label: 'Total paid out', val: '$70.2K' },
              { label: 'Avg per seller', val: '$381' },
              { label: 'Top seller earned', val: '$4,200' },
              { label: 'Platform commission', val: '10%' },
            ].map(s => (
              <div key={s.label} className="flex justify-between text-xs">
                <span className="text-muted-foreground">{s.label}</span>
                <span className="font-semibold">{s.val}</span>
              </div>
            ))}
          </div>
        </BentoCard>

      </BentoGridLayout>
    </AppShell>
  );
}
