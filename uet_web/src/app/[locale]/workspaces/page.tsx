'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { Plus, Users, Lock, Globe, Search } from 'lucide-react';
import { LocaleSwitcher } from '@/components/locale-switcher';
import { ThemeToggle } from '@/components/theme-toggle';

interface WorkspaceData {
  id: string;
  name: string;
  description: string | null;
  avatarUrl: string | null;
  isPublic: boolean;
  _count: { members: number; projects: number };
}

export default function WorkspacesPage() {
  const params = useParams();
  const locale = (params?.locale as string) || 'en';
  const [workspaces, setWorkspaces] = useState<WorkspaceData[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  useEffect(() => {
    fetch('/api/workspaces')
      .then(r => r.ok ? r.json() : [])
      .then(data => setWorkspaces(Array.isArray(data) ? data : []))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const filtered = workspaces.filter(w =>
    w.name.toLowerCase().includes(search.toLowerCase()) ||
    w.description?.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="flex flex-col min-h-screen bg-background text-foreground text-sm">
      {/* Header */}
      <header className="sticky top-0 z-50 flex items-center justify-between h-14 px-6 border-b border-border bg-background/80 backdrop-blur-md">
        <div className="flex items-center gap-6">
          <Link href="/" className="flex items-center gap-2 font-bold text-base hover:opacity-80 transition-opacity">
            <img src="/logo.png" alt="UET Logo" className="w-6 h-6 object-contain" />
            <span className="hidden sm:inline">UET Platform</span>
          </Link>
          <nav className="hidden md:flex items-center gap-6 text-xs text-muted-foreground font-medium">
            <Link href={`/${locale}/feed`} className="hover:text-foreground transition-colors">Feed</Link>
            <Link href={`/${locale}/messages`} className="hover:text-foreground transition-colors">Messages</Link>
            <Link href={`/${locale}/workspaces`} className="text-primary font-semibold">Workspaces</Link>
            <Link href={`/${locale}/chat`} className="hover:text-foreground transition-colors">Workchat</Link>
            <Link href={`/${locale}/account`} className="hover:text-foreground transition-colors">Account</Link>
          </nav>
        </div>
        <div className="flex items-center gap-3">
          <LocaleSwitcher />
          <ThemeToggle />
        </div>
      </header>

      <div className="max-w-4xl mx-auto w-full py-8 px-4">
        {/* Title + Create */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold mb-1">Workspaces</h1>
            <p className="text-muted-foreground text-sm">Collaborative research spaces with channels, docs, and task boards</p>
          </div>
          <Link
            href={`/${locale}/workspaces/new`}
            className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-primary text-primary-foreground text-xs font-semibold hover:bg-primary/90 transition-colors"
          >
            <Plus size={14} />
            New Workspace
          </Link>
        </div>

        {/* Search */}
        <div className="relative mb-6">
          <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
          <input
            type="text"
            value={search}
            onChange={e => setSearch(e.target.value)}
            placeholder="Search workspaces..."
            className="w-full pl-10 pr-4 py-2.5 rounded-lg border border-border bg-background text-sm outline-none focus:border-primary/50"
          />
        </div>

        {/* Workspace grid */}
        {loading ? (
          <div className="flex justify-center py-16">
            <div className="animate-spin w-6 h-6 border-2 border-primary border-t-transparent rounded-full" />
          </div>
        ) : filtered.length === 0 ? (
          <div className="text-center py-16 text-muted-foreground">
            <Users size={40} className="mx-auto mb-3 opacity-30" />
            <p className="text-base font-medium mb-1">No workspaces yet</p>
            <p className="text-xs mb-4">Create the first workspace to start collaborating!</p>
            <Link
              href={`/${locale}/workspaces/new`}
              className="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg bg-primary text-primary-foreground text-xs font-semibold hover:bg-primary/90 transition-colors"
            >
              <Plus size={14} /> Create Workspace
            </Link>
          </div>
        ) : (
          <div className="grid gap-4 sm:grid-cols-2">
            {filtered.map(ws => (
              <Link
                key={ws.id}
                href={`/${locale}/workspaces/${ws.id}`}
                className="block p-5 rounded-xl border border-border hover:border-primary/30 bg-card transition-colors group"
              >
                <div className="flex items-start gap-3 mb-3">
                  {ws.avatarUrl ? (
                    <img src={ws.avatarUrl} alt={ws.name} className="w-10 h-10 rounded-lg object-cover" />
                  ) : (
                    <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center text-primary font-bold text-sm">
                      {ws.name[0]?.toUpperCase()}
                    </div>
                  )}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <h3 className="font-semibold truncate group-hover:text-primary transition-colors">
                        {ws.name}
                      </h3>
                      {ws.isPublic ? (
                        <Globe size={12} className="text-muted-foreground shrink-0" />
                      ) : (
                        <Lock size={12} className="text-muted-foreground shrink-0" />
                      )}
                    </div>
                    {ws.description && (
                      <p className="text-xs text-muted-foreground line-clamp-2 mt-1">{ws.description}</p>
                    )}
                  </div>
                </div>
                <div className="flex items-center gap-4 text-xs text-muted-foreground">
                  <span className="flex items-center gap-1"><Users size={12} /> {ws._count.members} members</span>
                  <span>{ws._count.projects} projects</span>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
