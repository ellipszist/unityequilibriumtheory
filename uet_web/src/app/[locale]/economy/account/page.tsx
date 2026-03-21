'use client';

import AppShell from '@/components/layout/AppShell';
import BentoGridLayout, { BentoCard } from '@/components/layout/BentoGridLayout';
import { Wallet, Key, CreditCard, Coins, Pickaxe, Store, Tag, UserCircle } from 'lucide-react';
import Link from 'next/link';
import { useParams } from 'next/navigation';

export default function AccountDashboardPage() {
  const params = useParams();
  const locale = (params?.locale as string) || 'en';
  const base = `/${locale}/economy/account`;

  return (
    <AppShell>
      <BentoGridLayout columns={3}>

        {/* Header */}
        <div className="col-span-1 sm:col-span-2 lg:col-span-3 rounded-xl border border-border bg-card px-5 py-4 flex items-center gap-3">
          <UserCircle size={18} className="text-primary shrink-0" />
          <div>
            <h1 className="font-bold text-sm">My Account</h1>
            <p className="text-[11px] text-muted-foreground">Manage your personal resources, billing, API usage, and subscriptions.</p>
          </div>
        </div>

        {/* Personal Wallet — 2 cols */}
        <BentoCard span={2} className="bg-gradient-to-br from-blue-500/10 to-indigo-500/5">
          <Link href={`${base}/wallet`} className="flex flex-col h-full">
            <div className="flex items-center gap-2 mb-3">
              <Wallet size={16} className="text-primary" />
              <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Personal Wallet</span>
            </div>
            <div className="mt-auto">
              <div className="text-4xl font-bold mb-1">$150.00</div>
              <p className="text-xs text-muted-foreground">Your current balance</p>
            </div>
          </Link>
        </BentoCard>

        {/* Active Plan */}
        <BentoCard className="bg-gradient-to-br from-emerald-500/10 to-green-500/5">
          <Link href={`${base}/pricing`} className="flex flex-col h-full">
            <div className="flex items-center gap-2 mb-3">
              <Tag size={16} className="text-primary" />
              <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Active Plan</span>
            </div>
            <div className="mt-auto">
              <div className="text-2xl font-bold mb-1">Pro Tier</div>
              <p className="text-xs text-muted-foreground">Current Subscription</p>
            </div>
          </Link>
        </BentoCard>

        {/* API Keys */}
        <BentoCard>
          <Link href={`${base}/apikey`} className="flex flex-col h-full">
            <div className="flex items-center gap-2 mb-3">
              <Key size={16} className="text-primary" />
              <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">My API Keys</span>
            </div>
            <p className="text-xs text-muted-foreground mt-auto">Manage access tokens for UET services</p>
          </Link>
        </BentoCard>

        {/* Billing */}
        <BentoCard>
          <Link href={`${base}/billing`} className="flex flex-col h-full">
            <div className="flex items-center gap-2 mb-3">
              <CreditCard size={16} className="text-primary" />
              <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Billing History</span>
            </div>
            <p className="text-xs text-muted-foreground mt-auto">Invoices and payment records</p>
          </Link>
        </BentoCard>

        {/* Credits */}
        <BentoCard>
          <Link href={`${base}/credits`} className="flex flex-col h-full">
            <div className="flex items-center gap-2 mb-3">
              <Coins size={16} className="text-primary" />
              <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">My Credits</span>
            </div>
            <div className="mt-auto">
              <div className="text-2xl font-bold mb-1">1,450</div>
              <p className="text-xs text-muted-foreground">AI compute credits</p>
            </div>
          </Link>
        </BentoCard>

        {/* Mining */}
        <BentoCard>
          <Link href={`${base}/mining`} className="flex flex-col h-full">
            <div className="flex items-center gap-2 mb-3">
              <Pickaxe size={16} className="text-primary" />
              <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">My Nodes (Mining)</span>
            </div>
            <div className="mt-auto">
              <div className="text-2xl font-bold mb-1">2</div>
              <p className="text-xs text-muted-foreground">Active PoUW nodes</p>
            </div>
          </Link>
        </BentoCard>

        {/* Market */}
        <BentoCard>
          <Link href={`${base}/market`} className="flex flex-col h-full">
            <div className="flex items-center gap-2 mb-3">
              <Store size={16} className="text-primary" />
              <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">My Market Items</span>
            </div>
            <p className="text-xs text-muted-foreground mt-auto">Listed agents and models</p>
          </Link>
        </BentoCard>

      </BentoGridLayout>
    </AppShell>
  );
}
