'use client';

import { useState, useEffect } from 'react';
import { useRouter, useParams } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, Save } from 'lucide-react';
import { ThemeToggle } from '@/components/theme-toggle';

export default function EditProfilePage() {
  const router = useRouter();
  const params = useParams();
  const locale = (params?.locale as string) || 'en';

  const [displayName, setDisplayName] = useState('');
  const [bio, setBio] = useState('');
  const [institution, setInstitution] = useState('');
  const [website, setWebsite] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [userId, setUserId] = useState<string | null>(null);

  useEffect(() => {
    try {
      const stored = localStorage.getItem('user');
      if (stored) {
        const user = JSON.parse(stored);
        setUserId(user.id);
        fetch(`/api/profile/${user.id}`)
          .then(r => r.ok ? r.json() : null)
          .then(data => {
            if (data) {
              setDisplayName(data.displayName || data.name || '');
              setBio(data.bio || '');
              setInstitution(data.institution || '');
              setWebsite(data.website || '');
            }
          });
      }
    } catch {}
  }, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!userId) return;
    setLoading(true);
    setError('');
    setSuccess(false);

    try {
      const res = await fetch('/api/profile', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId, displayName, bio, institution, website }),
      });
      if (res.ok) {
        setSuccess(true);
        setTimeout(() => router.push(`/${locale}/profile/${userId}`), 1500);
      } else {
        const data = await res.json();
        setError(data.error || 'Failed to update');
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
          <Link href={`/${locale}/profile/${userId || ''}`} className="p-1.5 rounded-lg hover:bg-muted transition-colors">
            <ArrowLeft size={18} />
          </Link>
          <h1 className="font-semibold">Edit Profile</h1>
        </div>
        <ThemeToggle />
      </header>

      <div className="max-w-lg mx-auto w-full py-10 px-4">
        <form onSubmit={handleSubmit} className="space-y-5">
          {error && (
            <div className="p-3 rounded-lg bg-destructive/10 border border-destructive/30 text-destructive text-sm">{error}</div>
          )}
          {success && (
            <div className="p-3 rounded-lg bg-green-500/10 border border-green-500/30 text-green-600 dark:text-green-400 text-sm">
              Profile updated! Redirecting...
            </div>
          )}

          <div>
            <label className="block text-xs font-medium text-muted-foreground mb-1.5">Display Name</label>
            <input
              type="text"
              value={displayName}
              onChange={e => setDisplayName(e.target.value)}
              placeholder="Your name"
              maxLength={100}
              className="w-full px-3 py-2.5 rounded-lg border border-border bg-background text-sm outline-none focus:border-primary/50"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-muted-foreground mb-1.5">Bio</label>
            <textarea
              value={bio}
              onChange={e => setBio(e.target.value)}
              placeholder="Tell others about your research interests..."
              rows={4}
              maxLength={500}
              className="w-full px-3 py-2.5 rounded-lg border border-border bg-background text-sm outline-none focus:border-primary/50 resize-none"
            />
            <p className="text-[11px] text-muted-foreground mt-1">{bio.length}/500</p>
          </div>

          <div>
            <label className="block text-xs font-medium text-muted-foreground mb-1.5">Institution</label>
            <input
              type="text"
              value={institution}
              onChange={e => setInstitution(e.target.value)}
              placeholder="University, Lab, or Organization"
              className="w-full px-3 py-2.5 rounded-lg border border-border bg-background text-sm outline-none focus:border-primary/50"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-muted-foreground mb-1.5">Website</label>
            <input
              type="url"
              value={website}
              onChange={e => setWebsite(e.target.value)}
              placeholder="https://your-website.com"
              className="w-full px-3 py-2.5 rounded-lg border border-border bg-background text-sm outline-none focus:border-primary/50"
            />
          </div>

          <div className="flex items-center justify-between pt-4 border-t border-border">
            <Link href={`/${locale}/profile/${userId || ''}`} className="text-sm text-muted-foreground hover:text-foreground">
              Cancel
            </Link>
            <button
              type="submit"
              disabled={loading}
              className="flex items-center gap-2 px-6 py-2.5 rounded-lg bg-primary text-primary-foreground font-semibold text-sm hover:bg-primary/90 disabled:opacity-40 transition-colors"
            >
              {loading ? <div className="animate-spin w-4 h-4 border-2 border-current border-t-transparent rounded-full" /> : <Save size={14} />}
              Save Changes
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
