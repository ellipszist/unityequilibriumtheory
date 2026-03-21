'use client';

import AppShell from '@/components/layout/AppShell';
import { Wallet, ArrowDownLeft, ArrowUpRight, Plus, RefreshCw } from 'lucide-react';

const MOCK_TXS = [
  { id: 't1', type: 'credit', label: 'Credit top-up', amount: '+$50.00', date: 'Mar 20, 2026', status: 'completed' },
  { id: 't2', type: 'debit', label: 'AI compute usage', amount: '-$3.20', date: 'Mar 19, 2026', status: 'completed' },
  { id: 't3', type: 'debit', label: 'WorkChat session', amount: '-$0.80', date: 'Mar 18, 2026', status: 'completed' },
  { id: 't4', type: 'credit', label: 'Mining reward', amount: '+$12.00', date: 'Mar 17, 2026', status: 'completed' },
  { id: 't5', type: 'debit', label: 'Subscription renewal', amount: '-$29.00', date: 'Mar 15, 2026', status: 'completed' },
];

export default function AccountWalletPage() {
  return (
    <AppShell>
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-3xl mx-auto px-4 py-8 space-y-6">

          {/* Balance card */}
          <div className="rounded-2xl border border-border bg-gradient-to-br from-blue-500/10 to-indigo-500/5 p-6">
            <div className="flex items-center gap-2 mb-4">
              <Wallet size={18} className="text-primary" />
              <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Personal Wallet</span>
            </div>
            <div className="text-4xl font-bold mb-1">$150.00</div>
            <p className="text-xs text-muted-foreground mb-6">Available balance</p>
            <div className="flex gap-3">
              <button className="flex items-center gap-2 px-4 py-2 rounded-xl bg-primary text-primary-foreground text-xs font-semibold hover:bg-primary/90 transition-colors">
                <Plus size={14} /> Top Up
              </button>
              <button className="flex items-center gap-2 px-4 py-2 rounded-xl border border-border bg-card text-xs font-semibold hover:bg-accent transition-colors">
                <ArrowUpRight size={14} /> Withdraw
              </button>
              <button className="ml-auto flex items-center gap-1.5 px-3 py-2 rounded-xl border border-border text-xs text-muted-foreground hover:bg-accent transition-colors">
                <RefreshCw size={13} /> Refresh
              </button>
            </div>
          </div>

          {/* Transactions */}
          <div className="rounded-2xl border border-border bg-card overflow-hidden">
            <div className="px-5 py-4 border-b border-border flex items-center justify-between">
              <h2 className="font-semibold text-sm">Recent Transactions</h2>
              <span className="text-xs text-muted-foreground">Last 30 days</span>
            </div>
            <div className="divide-y divide-border">
              {MOCK_TXS.map(tx => (
                <div key={tx.id} className="flex items-center gap-4 px-5 py-3.5">
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${tx.type === 'credit' ? 'bg-emerald-500/10' : 'bg-red-500/10'}`}>
                    {tx.type === 'credit'
                      ? <ArrowDownLeft size={14} className="text-emerald-500" />
                      : <ArrowUpRight size={14} className="text-red-400" />}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-medium truncate">{tx.label}</div>
                    <div className="text-[11px] text-muted-foreground">{tx.date}</div>
                  </div>
                  <div className={`text-sm font-semibold shrink-0 ${tx.type === 'credit' ? 'text-emerald-500' : 'text-foreground'}`}>
                    {tx.amount}
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
