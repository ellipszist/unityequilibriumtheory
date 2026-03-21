'use client';

import AppShell from '@/components/layout/AppShell';

export default function SettingsPage() {
  return (
    <AppShell>
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-2xl mx-auto px-4 py-8">
          <h1 className="text-2xl font-bold mb-6">Settings</h1>
          <div className="space-y-6">
            <div className="rounded-2xl border border-border bg-card p-5">
              <h2 className="font-semibold text-sm mb-3">Appearance</h2>
              <p className="text-xs text-muted-foreground">Theme and display preferences.</p>
            </div>
            <div className="rounded-2xl border border-border bg-card p-5">
              <h2 className="font-semibold text-sm mb-3">Notifications</h2>
              <p className="text-xs text-muted-foreground">Email and push notification settings.</p>
            </div>
            <div className="rounded-2xl border border-border bg-card p-5">
              <h2 className="font-semibold text-sm mb-3">Privacy & Security</h2>
              <p className="text-xs text-muted-foreground">Password, two-factor authentication, and data management.</p>
            </div>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
