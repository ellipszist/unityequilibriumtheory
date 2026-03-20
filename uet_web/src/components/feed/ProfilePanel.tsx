'use client';

import Link from 'next/link';
import { useParams } from 'next/navigation';
import { useState, useEffect } from 'react';
import { Settings, CreditCard, Plus } from 'lucide-react';

export default function ProfilePanel() {
  const params = useParams();
  const locale = (params?.locale as string) || 'en';
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    try {
      const stored = localStorage.getItem('user');
      if (stored) setUser(JSON.parse(stored));
    } catch {}
  }, []);

  const name = user?.display_name || user?.name || user?.email?.split('@')[0] || 'Guest';
  const initials = name[0]?.toUpperCase() || 'G';

  return (
    <div className="p-4 space-y-4">
      {/* Profile card */}
      <Link href={`/${locale}/account`} className="flex items-center gap-3 p-3 rounded-xl hover:bg-muted/50 transition-colors">
        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary to-emerald-600 flex items-center justify-center text-white font-bold text-sm shrink-0">
          {initials}
        </div>
        <div className="flex-1 min-w-0">
          <p className="font-semibold text-sm truncate">{name}</p>
          <p className="text-[11px] text-muted-foreground">View your profile</p>
        </div>
      </Link>

      {/* Stories placeholder */}
      <div>
        <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-3 px-1">Stories</h3>
        <div className="flex gap-2 overflow-x-auto pb-2">
          <button className="shrink-0 w-16 h-24 rounded-xl border-2 border-dashed border-muted-foreground/30 flex flex-col items-center justify-center gap-1 hover:border-primary/50 hover:bg-primary/5 transition-colors">
            <Plus size={16} className="text-muted-foreground" />
            <span className="text-[9px] text-muted-foreground">Add</span>
          </button>
          {[1, 2, 3].map(i => (
            <div key={i} className="shrink-0 w-16 h-24 rounded-xl bg-gradient-to-b from-primary/20 to-primary/5 border border-border flex items-end justify-center pb-1.5">
              <span className="text-[9px] text-muted-foreground">User {i}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Quick links */}
      <div className="space-y-0.5">
        <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2 px-1">Quick Links</h3>
        <Link href={`/${locale}/workspaces`} className="flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm hover:bg-muted/50 transition-colors text-muted-foreground hover:text-foreground">
          <Settings size={16} /> Projects
        </Link>
        <Link href={`/${locale}/account/billing`} className="flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm hover:bg-muted/50 transition-colors text-muted-foreground hover:text-foreground">
          <CreditCard size={16} /> Credits & Billing
        </Link>
      </div>
    </div>
  );
}
