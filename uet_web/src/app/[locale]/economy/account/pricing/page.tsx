'use client';

import AppShell from '@/components/layout/AppShell';
import { Tag, Check, Sparkles, Zap } from 'lucide-react';

const PLANS = [
  {
    id: 'free',
    name: 'Free',
    price: '$0',
    period: '/ mo',
    desc: 'For individual researchers getting started',
    current: false,
    features: ['500 credits/month', '3 projects', '1 API key', 'Community access', 'Basic WorkChat (GPT-3.5)'],
    cta: 'Downgrade',
    highlight: false,
  },
  {
    id: 'pro',
    name: 'Pro',
    price: '$29',
    period: '/ mo',
    desc: 'For active researchers and collaborators',
    current: true,
    features: ['5,000 credits/month', 'Unlimited projects', '5 API keys', 'Priority WorkChat (GPT-4o)', '2 mining nodes', 'Early access features'],
    cta: 'Current Plan',
    highlight: true,
  },
  {
    id: 'team',
    name: 'Team',
    price: '$99',
    period: '/ mo',
    desc: 'For research groups and institutions',
    current: false,
    features: ['25,000 credits/month', 'Unlimited everything', '20 API keys', 'All AI models', '10 mining nodes', 'Dedicated support', 'Custom integrations'],
    cta: 'Upgrade',
    highlight: false,
  },
];

export default function AccountPricingPage() {
  return (
    <AppShell>
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-4xl mx-auto px-4 py-8 space-y-6">

          <div className="flex items-center gap-2 mb-2">
            <Tag size={18} className="text-primary" />
            <div>
              <h1 className="text-xl font-bold">Subscription Plans</h1>
              <p className="text-xs text-muted-foreground">Currently on <strong>Pro Tier</strong> — renews Mar 1, 2026</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {PLANS.map(plan => (
              <div
                key={plan.id}
                className={`rounded-2xl border p-5 flex flex-col ${plan.highlight ? 'border-primary bg-primary/5' : 'border-border bg-card'}`}
              >
                <div className="flex items-center justify-between mb-1">
                  <div className="flex items-center gap-2">
                    {plan.id === 'pro' && <Sparkles size={14} className="text-primary" />}
                    {plan.id === 'team' && <Zap size={14} className="text-primary" />}
                    <span className="font-bold text-sm">{plan.name}</span>
                  </div>
                  {plan.current && (
                    <span className="text-[10px] bg-primary text-primary-foreground px-2 py-0.5 rounded-full font-medium">Active</span>
                  )}
                </div>
                <p className="text-[11px] text-muted-foreground mb-3">{plan.desc}</p>
                <div className="text-3xl font-bold mb-4">
                  {plan.price}<span className="text-sm font-normal text-muted-foreground">{plan.period}</span>
                </div>
                <ul className="space-y-2 flex-1 mb-5">
                  {plan.features.map(f => (
                    <li key={f} className="flex items-center gap-2 text-xs">
                      <Check size={12} className="text-emerald-500 shrink-0" />
                      {f}
                    </li>
                  ))}
                </ul>
                <button
                  disabled={plan.current}
                  className={`w-full py-2 rounded-xl text-xs font-semibold transition-colors ${plan.current
                    ? 'bg-muted text-muted-foreground cursor-default'
                    : plan.highlight
                      ? 'bg-primary text-primary-foreground hover:bg-primary/90'
                      : 'border border-border hover:bg-accent'
                  }`}
                >
                  {plan.cta}
                </button>
              </div>
            ))}
          </div>

        </div>
      </div>
    </AppShell>
  );
}
