'use client';

import AppShell from '@/components/layout/AppShell';
import BentoGridLayout, { BentoCard } from '@/components/layout/BentoGridLayout';
import { Pickaxe, Globe, Cpu, Zap, Circle } from 'lucide-react';

const TOP_NODES = [
  { name: 'Node-SG-001', location: 'Singapore', uptime: '99.9%', credits: '8,420' },
  { name: 'Node-EU-043', location: 'Frankfurt', uptime: '99.7%', credits: '7,910' },
  { name: 'Node-US-118', location: 'Virginia', uptime: '98.4%', credits: '6,230' },
  { name: 'Node-JP-007', location: 'Tokyo', uptime: '99.1%', credits: '5,880' },
  { name: 'Node-AU-022', location: 'Sydney', uptime: '97.8%', credits: '4,910' },
];

const REGIONS = [
  { name: 'Asia Pacific', nodes: 612, share: 33, color: 'bg-primary' },
  { name: 'Europe', nodes: 544, share: 29, color: 'bg-blue-500' },
  { name: 'North America', nodes: 430, share: 23, color: 'bg-emerald-500' },
  { name: 'Other', nodes: 261, share: 15, color: 'bg-amber-500' },
];

export default function EconomyMiningPage() {
  return (
    <AppShell>
      <BentoGridLayout columns={3}>

        <div className="col-span-1 sm:col-span-2 lg:col-span-3 rounded-xl border border-border bg-card px-5 py-4 flex items-center gap-3">
          <Globe size={18} className="text-primary shrink-0" />
          <div>
            <h1 className="font-bold text-sm">Mining Network</h1>
            <p className="text-[11px] text-muted-foreground">PoUW — Proof of Useful Work node operations and rewards</p>
          </div>
        </div>

        {/* Network overview — 2 cols */}
        <BentoCard span={2} className="bg-gradient-to-br from-orange-500/10 to-amber-500/5">
          <div className="flex items-center gap-2 mb-3">
            <Pickaxe size={16} className="text-primary" />
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Network Overview</span>
          </div>
          <div className="grid grid-cols-3 gap-4 mb-4">
            {[
              { label: 'Active Nodes', value: '1,847' },
              { label: 'Total Compute', value: '4.2 PF' },
              { label: 'Credits/Day', value: '3.68M' },
            ].map(s => (
              <div key={s.label}>
                <div className="text-2xl font-bold">{s.value}</div>
                <div className="text-[11px] text-muted-foreground">{s.label}</div>
              </div>
            ))}
          </div>
          <div className="flex items-center gap-2 text-xs text-emerald-500">
            <Circle size={8} className="fill-emerald-500" />
            Network healthy · 98.6% avg uptime
          </div>
        </BentoCard>

        {/* Rewards */}
        <BentoCard>
          <div className="flex items-center gap-2 mb-4">
            <Zap size={16} className="text-amber-500" />
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Rewards (30d)</span>
          </div>
          <div className="space-y-3">
            {[
              { label: 'Total distributed', val: '110.4M cr' },
              { label: 'Avg per node/day', val: '~200 cr' },
              { label: 'Top node earned', val: '8,420 cr' },
              { label: 'Reward pool left', val: '3.68M cr' },
            ].map(s => (
              <div key={s.label} className="flex justify-between text-xs">
                <span className="text-muted-foreground">{s.label}</span>
                <span className="font-semibold">{s.val}</span>
              </div>
            ))}
          </div>
        </BentoCard>

        {/* Top nodes — 2 cols */}
        <BentoCard span={2} className="flex flex-col">
          <div className="flex items-center gap-2 mb-4">
            <Cpu size={14} className="text-primary" />
            <h2 className="font-semibold text-sm">Top Nodes (30d)</h2>
          </div>
          <div className="space-y-2">
            {TOP_NODES.map((node, i) => (
              <div key={node.name} className="flex items-center gap-3">
                <span className="text-[10px] text-muted-foreground/50 w-4 shrink-0">{i + 1}</span>
                <div className="flex-1 min-w-0">
                  <div className="text-xs font-medium">{node.name}</div>
                  <div className="text-[10px] text-muted-foreground">{node.location} · {node.uptime} uptime</div>
                </div>
                <div className="text-xs font-semibold text-emerald-500 shrink-0">+{node.credits} cr</div>
              </div>
            ))}
          </div>
        </BentoCard>

        {/* Regional distribution */}
        <BentoCard>
          <div className="flex items-center gap-2 mb-4">
            <Globe size={14} className="text-primary" />
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">By Region</span>
          </div>
          <div className="space-y-3">
            {REGIONS.map(r => (
              <div key={r.name}>
                <div className="flex justify-between text-xs mb-1">
                  <span>{r.name}</span>
                  <span className="text-muted-foreground">{r.nodes} nodes</span>
                </div>
                <div className="bg-muted/40 rounded-full h-1.5 overflow-hidden">
                  <div className={`h-full ${r.color} rounded-full`} style={{ width: `${r.share}%` }} />
                </div>
              </div>
            ))}
          </div>
        </BentoCard>

      </BentoGridLayout>
    </AppShell>
  );
}
