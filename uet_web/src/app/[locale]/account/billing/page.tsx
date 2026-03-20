'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { ArrowLeft, CreditCard, Zap, TrendingUp, ArrowUpRight, ArrowDownLeft, RefreshCw } from 'lucide-react';
import { ThemeToggle } from '@/components/theme-toggle';

interface CreditData {
  id: string;
  balance: number;
  lifetime: number;
  transactions: {
    id: string;
    amount: number;
    type: string;
    description: string | null;
    createdAt: string;
  }[];
}

export default function BillingPage() {
  const params = useParams();
  const locale = (params?.locale as string) || 'en';
  const [credits, setCredits] = useState<CreditData | null>(null);
  const [loading, setLoading] = useState(true);
  const [userId, setUserId] = useState<string | null>(null);

  useEffect(() => {
    try {
      const stored = localStorage.getItem('user');
      if (stored) {
        const user = JSON.parse(stored);
        setUserId(user.id);
        fetchCredits(user.id);
      } else {
        setLoading(false);
      }
    } catch { setLoading(false); }
  }, []);

  async function fetchCredits(uid: string) {
    try {
      const res = await fetch(`/api/credits?userId=${uid}`);
      if (res.ok) setCredits(await res.json());
    } catch {}
    setLoading(false);
  }

  const planTiers = [
    { name: 'Free', price: '$0', credits: '500/mo', current: true },
    { name: 'Pro', price: '$20/mo', credits: '50,000/mo', highlight: true },
    { name: 'Enterprise', price: 'Custom', credits: 'Unlimited' },
  ];

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="animate-spin w-8 h-8 border-2 border-primary border-t-transparent rounded-full" />
      </div>
    );
  }

  return (
    <div className="flex flex-col min-h-screen bg-background text-foreground text-sm">
      <header className="sticky top-0 z-50 flex items-center justify-between h-14 px-6 border-b border-border bg-background/80 backdrop-blur-md">
        <div className="flex items-center gap-4">
          <Link href={`/${locale}/account`} className="p-1.5 rounded-lg hover:bg-muted transition-colors">
            <ArrowLeft size={18} />
          </Link>
          <h1 className="font-semibold">Billing & Credits</h1>
        </div>
        <ThemeToggle />
      </header>

      <div className="max-w-2xl mx-auto w-full py-8 px-4 space-y-6">
        {/* Credit Balance Card */}
        <div className="rounded-xl border border-border bg-gradient-to-br from-primary/5 to-primary/10 p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-primary flex items-center justify-center">
                <Zap size={18} className="text-primary-foreground" />
              </div>
              <div>
                <p className="text-[10px] font-semibold tracking-widest text-muted-foreground uppercase">AI Credits</p>
                <p className="text-3xl font-extrabold text-primary">
                  {credits ? credits.balance.toLocaleString() : '0'}
                </p>
              </div>
            </div>
            <button
              onClick={() => userId && fetchCredits(userId)}
              className="p-2 rounded-lg hover:bg-muted text-muted-foreground hover:text-foreground transition-colors"
            >
              <RefreshCw size={14} />
            </button>
          </div>
          <div className="flex items-center gap-6 text-xs text-muted-foreground">
            <span className="flex items-center gap-1"><TrendingUp size={12} /> Lifetime: {credits?.lifetime.toLocaleString() || '0'} credits used</span>
          </div>
          <div className="mt-4 flex gap-3">
            <button className="px-4 py-2 rounded-lg bg-primary text-primary-foreground text-xs font-semibold hover:bg-primary/90 transition-colors flex items-center gap-1.5">
              <CreditCard size={13} /> Buy Credits
            </button>
            <button className="px-4 py-2 rounded-lg border border-border text-xs font-medium hover:bg-muted transition-colors">
              Exchange UET Coin
            </button>
          </div>
        </div>

        {/* Credit Costs */}
        <div className="rounded-xl border border-border p-5">
          <h2 className="font-semibold mb-4">Credit Costs</h2>
          <div className="grid grid-cols-2 gap-3">
            {[
              { action: 'Chat message (standard)', cost: '1-5' },
              { action: 'Chat message (reasoning)', cost: '5-20' },
              { action: 'Document ingestion (per page)', cost: '2' },
              { action: 'OmegaSearch query', cost: '1' },
              { action: 'Image generation', cost: '10' },
              { action: 'Voice transcription (per min)', cost: '5' },
            ].map(item => (
              <div key={item.action} className="flex items-center justify-between p-3 rounded-lg bg-muted/30">
                <span className="text-xs">{item.action}</span>
                <span className="text-xs font-semibold text-primary">{item.cost} cr</span>
              </div>
            ))}
          </div>
        </div>

        {/* Plan Comparison */}
        <div className="rounded-xl border border-border p-5">
          <h2 className="font-semibold mb-4">Plans</h2>
          <div className="grid grid-cols-3 gap-3">
            {planTiers.map(tier => (
              <div
                key={tier.name}
                className={`p-4 rounded-xl border text-center ${
                  tier.highlight ? 'border-primary bg-primary/5' : 'border-border'
                }`}
              >
                <h3 className="font-semibold mb-1">{tier.name}</h3>
                <p className="text-xl font-bold mb-1">{tier.price}</p>
                <p className="text-xs text-muted-foreground mb-3">{tier.credits}</p>
                <Link
                  href={`/${locale}/pricing`}
                  className={`block w-full py-1.5 rounded-lg text-xs font-medium transition-colors ${
                    tier.current
                      ? 'bg-muted text-muted-foreground'
                      : tier.highlight
                        ? 'bg-primary text-primary-foreground hover:bg-primary/90'
                        : 'border border-border hover:bg-muted'
                  }`}
                >
                  {tier.current ? 'Current' : tier.highlight ? 'Upgrade' : 'Contact'}
                </Link>
              </div>
            ))}
          </div>
        </div>

        {/* Transaction History */}
        <div className="rounded-xl border border-border p-5">
          <h2 className="font-semibold mb-4">Credit History</h2>
          {!credits || credits.transactions.length === 0 ? (
            <p className="text-center text-muted-foreground py-8 text-xs">No transactions yet</p>
          ) : (
            <div className="space-y-1">
              {credits.transactions.map(tx => {
                const isPositive = tx.amount > 0;
                return (
                  <div key={tx.id} className="flex items-center gap-3 p-3 rounded-lg hover:bg-muted/30 transition-colors">
                    <div className={`w-7 h-7 rounded-full flex items-center justify-center ${
                      isPositive ? 'bg-green-500/10 text-green-600' : 'bg-red-500/10 text-red-500'
                    }`}>
                      {isPositive ? <ArrowDownLeft size={13} /> : <ArrowUpRight size={13} />}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-xs font-medium">{tx.type.replace(/_/g, ' ')}</p>
                      {tx.description && <p className="text-[10px] text-muted-foreground truncate">{tx.description}</p>}
                    </div>
                    <div className="text-right">
                      <p className={`text-sm font-bold ${isPositive ? 'text-green-600' : 'text-red-500'}`}>
                        {isPositive ? '+' : ''}{tx.amount.toLocaleString()}
                      </p>
                      <p className="text-[10px] text-muted-foreground">{new Date(tx.createdAt).toLocaleDateString()}</p>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
