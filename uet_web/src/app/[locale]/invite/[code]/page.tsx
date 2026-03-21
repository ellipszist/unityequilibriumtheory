'use client';

import { useParams } from 'next/navigation';
import AppShell from '@/components/layout/AppShell';

export default function InvitePage() {
  const params = useParams();
  const code = params?.code as string;

  return (
    <AppShell>
      <div className="flex-1 flex items-center justify-center">
        <div className="max-w-md p-8 rounded-2xl border border-border bg-card shadow-lg text-center">
          <h1 className="text-2xl font-bold mb-4">Project Invitation</h1>
          <p className="text-sm text-muted-foreground mb-6">You have been invited to join a project. Code: <span className="font-mono text-primary">{code}</span></p>
          <button className="px-6 py-2 rounded-xl bg-primary text-primary-foreground text-sm font-semibold hover:bg-primary/90 transition-colors">Accept Invitation</button>
        </div>
      </div>
    </AppShell>
  );
}
