'use client';

import AppShell from '@/components/layout/AppShell';
import BentoGridLayout, { BentoCard } from '@/components/layout/BentoGridLayout';
import { Wallet, Key, CreditCard, Coins, Pickaxe, Store, UserCircle, TrendingUp, Activity } from 'lucide-react';
import Link from 'next/link';
import { useParams } from 'next/navigation';

const KPI_STATS = [
  { label: 'Total Value Locked', value: '$2.4M', delta: '+12.3%', up: true },
  { label: 'Active Nodes', value: '1,847', delta: '+5.1%', up: true },
  { label: 'Credits Issued', value: '48.2M', delta: '-2.0%', up: false },
  { label: 'API Calls / mo', value: '1.2B', delta: '+18.7%', up: true },
];

export default function EconomyPage() {
  const params = useParams();
  const locale = (params?.locale as string) || 'en';

  return (
    <AppShell>
      <BentoGridLayout columns={3}>

        {/* KPI Strip — spans full width */}
        <div className="col-span-1 sm:col-span-2 lg:col-span-3 rounded-xl border border-border bg-card p-5">
          <div className="flex items-center gap-2 mb-4">
            <Activity size={16} className="text-primary" />
            <h1 className="font-bold text-sm">Economy Dashboard</h1>
            <span className="ml-auto text-[10px] text-muted-foreground">System-wide metrics</span>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            {KPI_STATS.map(s => (
              <div key={s.label} className="space-y-1">
                <div className="text-[10px] text-muted-foreground uppercase tracking-wider">{s.label}</div>
                <div className="text-xl font-bold">{s.value}</div>
                <div className={`text-xs font-medium flex items-center gap-1 ${s.up ? 'text-emerald-500' : 'text-red-400'}`}>
                  <TrendingUp size={11} className={s.up ? '' : 'rotate-180'} /> {s.delta}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Global Wallet — spans 2 cols */}
        <BentoCard span={2} className="bg-gradient-to-br from-emerald-500/10 to-green-500/5">
          <Link href={`/${locale}/economy/wallet`} className="flex flex-col h-full">
            <div className="flex items-center gap-2 mb-3">
              <Wallet size={16} className="text-primary" />
              <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Global Wallet</span>
            </div>
            <div className="mt-auto">
              <div className="text-4xl font-bold mb-1">$2.4M</div>
              <p className="text-xs text-muted-foreground">System Treasury & Reserves</p>
            </div>
          </Link>
        </BentoCard>

        {/* API Keys */}
        <BentoCard>
          <Link href={`/${locale}/economy/apikey`} className="flex flex-col h-full">
            <div className="flex items-center gap-2 mb-3">
              <Key size={16} className="text-primary" />
              <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">API Keys</span>
            </div>
            <div className="mt-auto">
              <div className="text-2xl font-bold mb-1">1.2B<span className="text-sm font-normal text-muted-foreground"> / mo</span></div>
              <p className="text-xs text-muted-foreground">Global Request Volume</p>
            </div>
          </Link>
        </BentoCard>

        {/* Billing */}
        <BentoCard>
          <Link href={`/${locale}/economy/billing`} className="flex flex-col h-full">
            <div className="flex items-center gap-2 mb-3">
              <CreditCard size={16} className="text-primary" />
              <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Billing & Revenue</span>
            </div>
            <div className="mt-auto">
              <div className="text-2xl font-bold mb-1">$94.2K</div>
              <p className="text-xs text-muted-foreground">Platform Income (30d)</p>
            </div>
          </Link>
        </BentoCard>

        {/* Credits */}
        <BentoCard>
          <Link href={`/${locale}/economy/credits`} className="flex flex-col h-full">
            <div className="flex items-center gap-2 mb-3">
              <Coins size={16} className="text-primary" />
              <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Credit System</span>
            </div>
            <div className="mt-auto">
              <div className="text-2xl font-bold mb-1">48.2M</div>
              <p className="text-xs text-muted-foreground">Credits in Circulation</p>
            </div>
          </Link>
        </BentoCard>

        {/* Mining */}
        <BentoCard>
          <Link href={`/${locale}/economy/mining`} className="flex flex-col h-full">
            <div className="flex items-center gap-2 mb-3">
              <Pickaxe size={16} className="text-primary" />
              <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Mining Network</span>
            </div>
            <div className="mt-auto">
              <div className="text-2xl font-bold mb-1">1,847</div>
              <p className="text-xs text-muted-foreground">Active PoUW Nodes</p>
            </div>
          </Link>
        </BentoCard>

        {/* Market */}
        <BentoCard>
          <Link href={`/${locale}/economy/market`} className="flex flex-col h-full">
            <div className="flex items-center gap-2 mb-3">
              <Store size={16} className="text-primary" />
              <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Marketplace</span>
            </div>
            <div className="mt-auto">
              <div className="text-2xl font-bold mb-1">312</div>
              <p className="text-xs text-muted-foreground">Active Listings</p>
            </div>
          </Link>
        </BentoCard>

        {/* My Account CTA — spans full width */}
        <div className="col-span-1 sm:col-span-2 lg:col-span-3 rounded-xl border border-primary/30 bg-primary/5 p-5 hover:border-primary/60 transition-colors">
          <Link href={`/${locale}/economy/account`} className="flex items-center gap-4">
            <UserCircle size={28} className="text-primary shrink-0" />
            <div>
              <div className="font-bold">My Account</div>
              <p className="text-xs text-muted-foreground">Personal wallet, API keys, billing, credits, mining, market, and pricing</p>
            </div>
            <span className="ml-auto text-xs text-primary font-medium">Open →</span>
          </Link>
        </div>

      </BentoGridLayout>
    </AppShell>
  );
}
