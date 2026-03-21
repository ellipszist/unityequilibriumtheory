'use client';

import AppShell from '@/components/layout/AppShell';
import { Store, Plus, Bot, FileText, TrendingUp, Eye } from 'lucide-react';

const MOCK_LISTINGS = [
  { id: 'item-1', name: 'UET Physics Agent v2', type: 'Agent', price: '120 credits', sales: 34, status: 'active', views: 218 },
  { id: 'item-2', name: 'Thermodynamics Prompt Pack', type: 'Prompt', price: '40 credits', sales: 91, status: 'active', views: 540 },
];

export default function AccountMarketPage() {
  return (
    <AppShell>
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-3xl mx-auto px-4 py-8 space-y-6">

          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Store size={18} className="text-primary" />
              <div>
                <h1 className="text-xl font-bold">My Market Items</h1>
                <p className="text-xs text-muted-foreground">Agents, prompts, and models you have listed</p>
              </div>
            </div>
            <button className="flex items-center gap-2 px-4 py-2 rounded-xl bg-primary text-primary-foreground text-xs font-semibold hover:bg-primary/90 transition-colors">
              <Plus size={14} /> New Listing
            </button>
          </div>

          {/* Sales summary */}
          <div className="grid grid-cols-3 gap-4">
            {[
              { label: 'Total Listings', value: '2', icon: Store },
              { label: 'Total Sales', value: '125', icon: TrendingUp },
              { label: 'Credits Earned', value: '9,640', icon: Bot },
            ].map(s => (
              <div key={s.label} className="rounded-2xl border border-border bg-card p-4 text-center">
                <s.icon size={16} className="text-primary mx-auto mb-2" />
                <div className="text-xl font-bold">{s.value}</div>
                <div className="text-[11px] text-muted-foreground">{s.label}</div>
              </div>
            ))}
          </div>

          {/* Listings */}
          <div className="rounded-2xl border border-border bg-card overflow-hidden">
            <div className="px-5 py-4 border-b border-border">
              <h2 className="font-semibold text-sm">Active Listings</h2>
            </div>
            <div className="divide-y divide-border">
              {MOCK_LISTINGS.map(item => (
                <div key={item.id} className="flex items-center gap-4 px-5 py-4">
                  <div className="w-9 h-9 rounded-xl bg-primary/10 flex items-center justify-center shrink-0">
                    {item.type === 'Agent' ? <Bot size={16} className="text-primary" /> : <FileText size={16} className="text-primary" />}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-semibold truncate">{item.name}</div>
                    <div className="flex items-center gap-3 text-[11px] text-muted-foreground mt-0.5">
                      <span>{item.type}</span>
                      <span>{item.price}</span>
                      <span className="flex items-center gap-1"><Eye size={10} /> {item.views} views</span>
                    </div>
                  </div>
                  <div className="text-right shrink-0">
                    <div className="text-sm font-semibold">{item.sales} sales</div>
                    <div className={`text-[10px] px-2 py-0.5 rounded-full inline-block mt-0.5 ${item.status === 'active' ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400' : 'bg-muted text-muted-foreground'}`}>
                      {item.status}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Empty state prompt */}
          <div className="rounded-2xl border border-dashed border-border bg-card p-8 text-center">
            <Store size={24} className="text-muted-foreground mx-auto mb-2" />
            <p className="text-sm font-medium mb-1">List your first item</p>
            <p className="text-xs text-muted-foreground mb-3">Sell AI agents, prompt packs, or fine-tuned models to the UET community</p>
            <button className="px-4 py-2 rounded-xl bg-primary text-primary-foreground text-xs font-semibold hover:bg-primary/90 transition-colors">
              Create Listing
            </button>
          </div>

        </div>
      </div>
    </AppShell>
  );
}
