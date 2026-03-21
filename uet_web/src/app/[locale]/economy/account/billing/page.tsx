'use client';

import AppShell from '@/components/layout/AppShell';
import { CreditCard, Download, CheckCircle } from 'lucide-react';

const MOCK_INVOICES = [
  { id: 'inv-001', date: 'Mar 1, 2026', desc: 'Pro Tier — Monthly', amount: '$29.00', status: 'paid' },
  { id: 'inv-002', date: 'Feb 1, 2026', desc: 'Pro Tier — Monthly', amount: '$29.00', status: 'paid' },
  { id: 'inv-003', date: 'Jan 1, 2026', desc: 'Pro Tier — Monthly', amount: '$29.00', status: 'paid' },
  { id: 'inv-004', date: 'Dec 1, 2025', desc: 'Pro Tier — Monthly', amount: '$29.00', status: 'paid' },
];

export default function AccountBillingPage() {
  return (
    <AppShell>
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-3xl mx-auto px-4 py-8 space-y-6">

          {/* Payment method */}
          <div className="rounded-2xl border border-border bg-card p-5">
            <div className="flex items-center gap-2 mb-4">
              <CreditCard size={16} className="text-primary" />
              <h2 className="font-semibold text-sm">Payment Method</h2>
            </div>
            <div className="flex items-center gap-4">
              <div className="w-12 h-8 rounded-lg bg-gradient-to-r from-blue-600 to-blue-400 flex items-center justify-center shrink-0">
                <span className="text-[9px] text-white font-bold">VISA</span>
              </div>
              <div>
                <div className="text-sm font-medium">•••• •••• •••• 4242</div>
                <div className="text-[11px] text-muted-foreground">Expires 12/27</div>
              </div>
              <button className="ml-auto text-xs text-primary hover:underline">Change</button>
            </div>
          </div>

          {/* Invoices */}
          <div className="rounded-2xl border border-border bg-card overflow-hidden">
            <div className="px-5 py-4 border-b border-border flex items-center justify-between">
              <h2 className="font-semibold text-sm">Billing History</h2>
              <span className="text-xs text-muted-foreground">{MOCK_INVOICES.length} invoices</span>
            </div>
            <div className="divide-y divide-border">
              {MOCK_INVOICES.map(inv => (
                <div key={inv.id} className="flex items-center gap-4 px-5 py-3.5">
                  <CheckCircle size={15} className="text-emerald-500 shrink-0" />
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-medium">{inv.desc}</div>
                    <div className="text-[11px] text-muted-foreground">{inv.date} · {inv.id}</div>
                  </div>
                  <div className="text-sm font-semibold shrink-0">{inv.amount}</div>
                  <button className="p-1.5 rounded-lg hover:bg-muted text-muted-foreground hover:text-foreground transition-colors">
                    <Download size={13} />
                  </button>
                </div>
              ))}
            </div>
          </div>

        </div>
      </div>
    </AppShell>
  );
}
