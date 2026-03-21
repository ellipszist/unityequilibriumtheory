'use client';

import AppShell from '@/components/layout/AppShell';
import { useState } from 'react';
import { useParams } from 'next/navigation';

export default function NewProjectPage() {
  const params = useParams();
  const locale = (params?.locale as string) || 'en';
  const [name, setName] = useState('');
  const [desc, setDesc] = useState('');

  function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    alert('Project created: ' + name);
    window.location.href = '/' + locale + '/project';
  }

  return (
    <AppShell>
      <div className="flex-1 overflow-y-auto flex items-center justify-center">
        <div className="w-full max-w-md p-8 rounded-2xl border border-border bg-card shadow-lg">
          <h1 className="text-2xl font-bold mb-6">Create New Project</h1>
          <form onSubmit={handleCreate} className="space-y-4">
            <input type="text" placeholder="Project Name" value={name} onChange={e => setName(e.target.value)} className="w-full px-3 py-2 rounded-xl border border-border bg-background text-sm outline-none focus:border-primary/60" required />
            <textarea placeholder="Description" value={desc} onChange={e => setDesc(e.target.value)} className="w-full px-3 py-2 rounded-xl border border-border bg-background text-sm outline-none focus:border-primary/60 h-24 resize-none" />
            <button type="submit" className="w-full py-2 rounded-xl bg-primary text-primary-foreground text-sm font-semibold hover:bg-primary/90 transition-colors">Create Project</button>
          </form>
        </div>
      </div>
    </AppShell>
  );
}
