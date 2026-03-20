'use client';

import { useState, useEffect } from 'react';
import { useRouter, useParams } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, Users } from 'lucide-react';
import { ThemeToggle } from '@/components/theme-toggle';

export default function NewWorkspacePage() {
  const router = useRouter();
  const params = useParams();
  const locale = (params?.locale as string) || 'en';

  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [isPublic, setIsPublic] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [userId, setUserId] = useState<string | null>(null);

  useEffect(() => {
    try {
      const stored = localStorage.getItem('user');
      if (stored) setUserId(JSON.parse(stored).id);
    } catch {}
  }, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!name.trim() || !userId) {
      setError(!userId ? 'Please log in first' : 'Workspace name is required');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const res = await fetch('/api/workspaces', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: name.trim(),
          description: description.trim() || null,
          ownerId: userId,
          isPublic,
        }),
      });

      if (res.ok) {
        const ws = await res.json();
        router.push(`/${locale}/workspaces/${ws.id}`);
      } else {
        const data = await res.json();
        setError(data.error || 'Failed to create workspace');
      }
    } catch {
      setError('Network error');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col min-h-screen bg-background text-foreground text-sm">
      <header className="sticky top-0 z-50 flex items-center justify-between h-14 px-6 border-b border-border bg-background/80 backdrop-blur-md">
        <div className="flex items-center gap-4">
          <Link href={`/${locale}/workspaces`} className="p-1.5 rounded-lg hover:bg-muted transition-colors">
            <ArrowLeft size={18} />
          </Link>
          <h1 className="font-semibold">New Workspace</h1>
        </div>
        <ThemeToggle />
      </header>

      <div className="max-w-lg mx-auto w-full py-10 px-4">
        <div className="flex items-center gap-3 mb-8">
          <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center">
            <Users size={22} className="text-primary" />
          </div>
          <div>
            <h2 className="text-xl font-bold">Create a Workspace</h2>
            <p className="text-xs text-muted-foreground">A collaborative space with channels, docs, and tasks</p>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-5">
          {error && (
            <div className="p-3 rounded-lg bg-destructive/10 border border-destructive/30 text-destructive text-sm">
              {error}
            </div>
          )}

          <div>
            <label className="block text-xs font-medium text-muted-foreground mb-1.5">Workspace Name</label>
            <input
              type="text"
              value={name}
              onChange={e => setName(e.target.value)}
              placeholder="e.g. Quantum Physics Lab"
              maxLength={100}
              className="w-full px-3 py-2.5 rounded-lg border border-border bg-background text-sm outline-none focus:border-primary/50"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-muted-foreground mb-1.5">Description (optional)</label>
            <textarea
              value={description}
              onChange={e => setDescription(e.target.value)}
              placeholder="What is this workspace for?"
              rows={3}
              className="w-full px-3 py-2.5 rounded-lg border border-border bg-background text-sm outline-none focus:border-primary/50 resize-none"
            />
          </div>

          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={() => setIsPublic(!isPublic)}
              className={`relative w-10 h-5 rounded-full transition-colors ${isPublic ? 'bg-primary' : 'bg-muted'}`}
            >
              <div className={`absolute top-0.5 w-4 h-4 rounded-full bg-white shadow-sm transition-transform ${isPublic ? 'translate-x-5' : 'translate-x-0.5'}`} />
            </button>
            <span className="text-sm">{isPublic ? 'Public' : 'Private'} workspace</span>
          </div>

          <div className="flex items-center justify-between pt-4 border-t border-border">
            <Link href={`/${locale}/workspaces`} className="text-sm text-muted-foreground hover:text-foreground">
              Cancel
            </Link>
            <button
              type="submit"
              disabled={loading || !name.trim()}
              className="flex items-center gap-2 px-6 py-2.5 rounded-lg bg-primary text-primary-foreground font-semibold text-sm hover:bg-primary/90 disabled:opacity-40 transition-colors"
            >
              {loading && <div className="animate-spin w-4 h-4 border-2 border-current border-t-transparent rounded-full" />}
              Create Workspace
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
