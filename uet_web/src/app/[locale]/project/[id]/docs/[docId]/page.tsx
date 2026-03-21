'use client';

import AppShell from '@/components/layout/AppShell';
import { useParams } from 'next/navigation';

export default function ProjectDocPage() {
  const params = useParams();
  const id = params?.id as string;
  const docId = params?.docId as string;

  return (
    <AppShell>
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-4xl mx-auto px-4 py-8">
          <h1 className="text-2xl font-bold mb-4">Document: {docId}</h1>
          <p className="text-sm text-muted-foreground mb-6">Project: {id} — Collaborative editor</p>
          <div className="rounded-2xl border border-border bg-card p-8 min-h-[400px] text-sm text-muted-foreground">
            Tiptap collaborative editor will render here.
          </div>
        </div>
      </div>
    </AppShell>
  );
}
