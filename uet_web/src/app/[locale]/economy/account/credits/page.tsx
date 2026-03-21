'use client';

import AppShell from '@/components/layout/AppShell';
import { Coins, Sparkles, Pickaxe, Plus } from 'lucide-react';

const MOCK_USAGE = [
  { id: 'u1', label: 'WorkChat — GPT-4o query', cost: -12, date: 'Mar 20, 2026' },
  { id: 'u2', label: 'WorkChat — Claude 3.5 query', cost: -8, date: 'Mar 19, 2026' },
  { id: 'u3', label: 'Mining reward payout', cost: +200, date: 'Mar 18, 2026' },
  { id: 'u4', label: 'WorkChat — batch analysis', cost: -45, date: 'Mar 17, 2026' },
  { id: 'u5', label: 'Monthly free allocation', cost: +500, date: 'Mar 1, 2026' },
];

const EARN_OPTIONS = [
  { icon: Pickaxe, label: 'Run a Mining Node', desc: 'Earn ~200 credits/day by contributing compute' },
  { icon: Sparkles, label: 'Complete Research Tasks', desc: 'Earn credits by validating AI outputs' },
  { icon: Plus, label: 'Buy Credits', desc: 'Purchase directly — $1 = 100 credits' },
];

export default function AccountCreditsPage() {
  return (
    <AppShell>
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-3xl mx-auto px-4 py-8 space-y-6">

          {/* Balance */}
          <div className="rounded-2xl border border-border bg-gradient-to-br from-amber-500/10 to-yellow-500/5 p-6">
            <div className="flex items-center gap-2 mb-3">
              <Coins size={18} className="text-primary" />
              <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Credit Balance</span>
            </div>
            <div className="text-4xl font-bold mb-1">1,450</div>
            <p className="text-xs text-muted-foreground mb-1">AI compute credits</p>
            <div className="mt-4 bg-muted/40 rounded-full h-2 overflow-hidden">
              <div className="h-full bg-primary rounded-full" style={{ width: '29%' }} />
            </div>
            <div className="flex justify-between text-[10px] text-muted-foreground mt-1">
              <span>1,450 / 5,000 monthly allocation</span>
              <span>29% used</span>
            </div>
          </div>

          {/* Earn more */}
          <div className="rounded-2xl border border-border bg-card p-5">
            <h2 className="font-semibold text-sm mb-4">Earn More Credits</h2>
            <div className="space-y-3">
              {EARN_OPTIONS.map(opt => (
                <button key={opt.label} className="w-full flex items-center gap-3 p-3 rounded-xl border border-border hover:border-primary/40 hover:bg-muted/30 transition-colors text-left">
                  <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center shrink-0">
                    <opt.icon size={15} className="text-primary" />
                  </div>
                  <div>
                    <div className="text-sm font-medium">{opt.label}</div>
                    <div className="text-[11px] text-muted-foreground">{opt.desc}</div>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Usage log */}
          <div className="rounded-2xl border border-border bg-card overflow-hidden">
            <div className="px-5 py-4 border-b border-border">
              <h2 className="font-semibold text-sm">Usage Log</h2>
            </div>
            <div className="divide-y divide-border">
              {MOCK_USAGE.map(u => (
                <div key={u.id} className="flex items-center gap-4 px-5 py-3">
                  <div className="flex-1 min-w-0">
                    <div className="text-sm truncate">{u.label}</div>
                    <div className="text-[11px] text-muted-foreground">{u.date}</div>
                  </div>
                  <div className={`text-sm font-semibold shrink-0 ${u.cost > 0 ? 'text-emerald-500' : 'text-foreground'}`}>
                    {u.cost > 0 ? '+' : ''}{u.cost}
                  </div>
                </div>
              ))}
            </div>
          </div>

        </div>
      </div>
    </AppShell>
  );
}
