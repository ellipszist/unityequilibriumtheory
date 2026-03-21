'use client';

import AppShell from '@/components/layout/AppShell';
import { Pickaxe, Cpu, Zap, Plus, Circle } from 'lucide-react';

const MOCK_NODES = [
  { id: 'node-1', name: 'Node Alpha', status: 'active', uptime: '99.2%', earned: '+842 credits', location: 'Singapore', cpu: 72 },
  { id: 'node-2', name: 'Node Beta', status: 'active', uptime: '97.8%', earned: '+631 credits', location: 'Frankfurt', cpu: 45 },
];

export default function AccountMiningPage() {
  return (
    <AppShell>
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-3xl mx-auto px-4 py-8 space-y-6">

          {/* Summary */}
          <div className="rounded-2xl border border-border bg-gradient-to-br from-orange-500/10 to-amber-500/5 p-6">
            <div className="flex items-center gap-2 mb-4">
              <Pickaxe size={18} className="text-primary" />
              <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Mining Overview</span>
            </div>
            <div className="grid grid-cols-3 gap-4">
              <div>
                <div className="text-2xl font-bold">2</div>
                <div className="text-[11px] text-muted-foreground">Active Nodes</div>
              </div>
              <div>
                <div className="text-2xl font-bold">1,473</div>
                <div className="text-[11px] text-muted-foreground">Credits Earned (30d)</div>
              </div>
              <div>
                <div className="text-2xl font-bold">98.5%</div>
                <div className="text-[11px] text-muted-foreground">Avg Uptime</div>
              </div>
            </div>
          </div>

          {/* Nodes list */}
          <div className="rounded-2xl border border-border bg-card overflow-hidden">
            <div className="px-5 py-4 border-b border-border flex items-center justify-between">
              <h2 className="font-semibold text-sm">My Nodes</h2>
              <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-primary/10 text-primary text-xs font-medium hover:bg-primary/20 transition-colors">
                <Plus size={13} /> Add Node
              </button>
            </div>
            <div className="divide-y divide-border">
              {MOCK_NODES.map(node => (
                <div key={node.id} className="px-5 py-4">
                  <div className="flex items-start justify-between gap-3 mb-3">
                    <div className="flex items-center gap-2">
                      <Circle size={8} className="text-emerald-500 fill-emerald-500 shrink-0" />
                      <span className="text-sm font-semibold">{node.name}</span>
                      <span className="text-[10px] bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 px-1.5 py-0.5 rounded-full capitalize">{node.status}</span>
                    </div>
                    <span className="text-xs font-semibold text-emerald-500">{node.earned}</span>
                  </div>
                  <div className="grid grid-cols-3 gap-3 mb-3">
                    <div className="text-center rounded-lg bg-muted/40 py-2">
                      <div className="text-xs font-semibold">{node.uptime}</div>
                      <div className="text-[10px] text-muted-foreground">Uptime</div>
                    </div>
                    <div className="text-center rounded-lg bg-muted/40 py-2">
                      <div className="text-xs font-semibold">{node.location}</div>
                      <div className="text-[10px] text-muted-foreground">Location</div>
                    </div>
                    <div className="text-center rounded-lg bg-muted/40 py-2">
                      <div className="text-xs font-semibold">{node.cpu}%</div>
                      <div className="text-[10px] text-muted-foreground">CPU</div>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <Cpu size={11} className="text-muted-foreground" />
                    <div className="flex-1 bg-muted/40 rounded-full h-1.5 overflow-hidden">
                      <div className="h-full bg-primary rounded-full" style={{ width: `${node.cpu}%` }} />
                    </div>
                    <Zap size={11} className="text-amber-500" />
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="rounded-2xl border border-border bg-card p-5 text-center">
            <Pickaxe size={24} className="text-muted-foreground mx-auto mb-2" />
            <p className="text-sm font-medium mb-1">Set up another node</p>
            <p className="text-xs text-muted-foreground mb-3">Each node earns ~200 credits/day. Requires minimum 4 CPU cores.</p>
            <button className="px-4 py-2 rounded-xl bg-primary text-primary-foreground text-xs font-semibold hover:bg-primary/90 transition-colors">
              Download Node Setup
            </button>
          </div>

        </div>
      </div>
    </AppShell>
  );
}
