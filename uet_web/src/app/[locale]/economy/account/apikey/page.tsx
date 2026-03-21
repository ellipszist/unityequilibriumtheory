'use client';

import AppShell from '@/components/layout/AppShell';
import { Key, Copy, Trash2, Plus, Eye, EyeOff } from 'lucide-react';
import { useState } from 'react';

const MOCK_KEYS = [
  { id: 'k1', name: 'Production Key', key: 'uet-sk-prod-••••••••••••3a2f', created: 'Jan 15, 2026', lastUsed: '2 hours ago', active: true },
  { id: 'k2', name: 'Development Key', key: 'uet-sk-dev-••••••••••••8c1d', created: 'Feb 3, 2026', lastUsed: '3 days ago', active: true },
  { id: 'k3', name: 'Test Key (inactive)', key: 'uet-sk-test-••••••••••••5e7b', created: 'Dec 1, 2025', lastUsed: 'Never', active: false },
];

export default function AccountApikeyPage() {
  const [revealed, setRevealed] = useState<string | null>(null);

  return (
    <AppShell>
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-3xl mx-auto px-4 py-8 space-y-6">

          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-xl font-bold">API Keys</h1>
              <p className="text-xs text-muted-foreground mt-0.5">Manage access tokens for UET services</p>
            </div>
            <button className="flex items-center gap-2 px-4 py-2 rounded-xl bg-primary text-primary-foreground text-xs font-semibold hover:bg-primary/90 transition-colors">
              <Plus size={14} /> Generate New Key
            </button>
          </div>

          <div className="rounded-2xl border border-border bg-card overflow-hidden">
            <div className="px-5 py-4 border-b border-border">
              <h2 className="font-semibold text-sm">Active Keys</h2>
            </div>
            <div className="divide-y divide-border">
              {MOCK_KEYS.map(k => (
                <div key={k.id} className="px-5 py-4">
                  <div className="flex items-start justify-between gap-3 mb-2">
                    <div className="flex items-center gap-2">
                      <Key size={14} className={k.active ? 'text-primary' : 'text-muted-foreground'} />
                      <span className="text-sm font-medium">{k.name}</span>
                      {!k.active && <span className="text-[10px] bg-muted text-muted-foreground px-1.5 py-0.5 rounded-full">Inactive</span>}
                    </div>
                    <div className="flex items-center gap-1">
                      <button
                        onClick={() => setRevealed(revealed === k.id ? null : k.id)}
                        className="p-1.5 rounded-lg hover:bg-muted text-muted-foreground hover:text-foreground transition-colors"
                      >
                        {revealed === k.id ? <EyeOff size={13} /> : <Eye size={13} />}
                      </button>
                      <button className="p-1.5 rounded-lg hover:bg-muted text-muted-foreground hover:text-foreground transition-colors">
                        <Copy size={13} />
                      </button>
                      <button className="p-1.5 rounded-lg hover:bg-red-500/10 text-muted-foreground hover:text-red-400 transition-colors">
                        <Trash2 size={13} />
                      </button>
                    </div>
                  </div>
                  <div className="font-mono text-xs text-muted-foreground bg-muted/40 rounded-lg px-3 py-2 mb-2">
                    {revealed === k.id ? k.key.replace(/••+/, 'sk_live_abc123xyz') : k.key}
                  </div>
                  <div className="flex gap-4 text-[10px] text-muted-foreground">
                    <span>Created {k.created}</span>
                    <span>Last used: {k.lastUsed}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="rounded-2xl border border-amber-500/20 bg-amber-500/5 p-4">
            <p className="text-xs text-amber-600 dark:text-amber-400">
              <strong>Security:</strong> Never share your API keys in public repositories or client-side code. Rotate keys immediately if compromised.
            </p>
          </div>

        </div>
      </div>
    </AppShell>
  );
}
