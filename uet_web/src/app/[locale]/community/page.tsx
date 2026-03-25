'use client';

import { useEffect, useState } from 'react';
import AppShell from '@/components/layout/AppShell';
import ProfilePanel from '@/components/feed/ProfilePanel';
import ChatFriendsPanel from '@/components/feed/ChatFriendsPanel';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { Rss, PenLine, MessageSquare, Loader2, RefreshCw, ArrowUp } from 'lucide-react';

const FALLBACK_POSTS = [
  { id: '1', author: { displayName: 'Researcher Alpha', institution: 'MIT', avatarUrl: null }, createdAt: new Date(Date.now() - 7200000).toISOString(), title: null, content: 'Just published a new paper on AI alignment! Check it out in Project Alpha.', upvotes: 42, isVerified: true, _count: { comments: 8, votes: 42 }, tags: [{ name: 'alignment' }] },
  { id: '2', author: { displayName: 'Dr. Beta', institution: 'CERN', avatarUrl: null }, createdAt: new Date(Date.now() - 18000000).toISOString(), title: null, content: 'New simulation results for quantum entropy model V = E × I × γ. The stability index reached 99.8% across all test domains.', upvotes: 128, isVerified: true, _count: { comments: 23, votes: 128 }, tags: [{ name: 'physics' }, { name: 'simulation' }] },
  { id: '3', author: { displayName: 'Sarah Chen', institution: 'Stanford', avatarUrl: null }, createdAt: new Date(Date.now() - 86400000).toISOString(), title: null, content: 'Looking for collaborators on thermodynamic economics modeling. DM me if interested!', upvotes: 15, isVerified: false, _count: { comments: 4, votes: 15 }, tags: [{ name: 'collaboration' }] },
];

type FeedMode = 'latest' | 'trending';

function timeAgo(dateStr: string) {
  const diff = Date.now() - new Date(dateStr).getTime();
  const m = Math.floor(diff / 60000);
  if (m < 60) return `${m}m ago`;
  const h = Math.floor(m / 60);
  if (h < 24) return `${h}h ago`;
  return `${Math.floor(h / 24)}d ago`;
}

export default function CommunityPage() {
  const params = useParams();
  const locale = (params?.locale as string) || 'en';
  const [posts, setPosts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [mode, setMode] = useState<FeedMode>('latest');
  const [usingFallback, setUsingFallback] = useState(false);

  const fetchFeed = async (m: FeedMode = mode) => {
    setLoading(true);
    try {
      const res = await fetch(`/api/feed?mode=${m}&limit=20`);
      if (!res.ok) throw new Error('API error');
      const data = await res.json();
      if (data.posts && data.posts.length > 0) {
        setPosts(data.posts);
        setUsingFallback(false);
      } else {
        setPosts(FALLBACK_POSTS);
        setUsingFallback(true);
      }
    } catch {
      setPosts(FALLBACK_POSTS);
      setUsingFallback(true);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchFeed(); }, []);

  const switchMode = (m: FeedMode) => {
    setMode(m);
    fetchFeed(m);
  };

  return (
    <AppShell>
      <div className="flex-1 flex overflow-hidden">
        {/* Panel 1: Profile (IG style) — equal flex-1 */}
        <div className="flex-1 min-w-0 border-r border-border overflow-y-auto hidden md:block">
          <ProfilePanel />
        </div>

        {/* Panel 2: Feed — equal flex-1 */}
        <div className="flex-1 min-w-0 overflow-y-auto">
          <div className="max-w-2xl mx-auto p-4">
            {/* Header */}
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <Rss size={16} className="text-primary" />
                <h2 className="font-semibold text-sm">Community Feed</h2>
                {usingFallback && (
                  <span className="text-[9px] bg-amber-500/10 text-amber-600 px-1.5 py-0.5 rounded-full">Demo</span>
                )}
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => fetchFeed()}
                  className="p-1.5 rounded-lg hover:bg-muted text-muted-foreground transition-colors"
                  title="Refresh"
                >
                  <RefreshCw size={13} />
                </button>
                <Link
                  href={`/${locale}/community/new`}
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-primary text-primary-foreground text-xs font-medium hover:bg-primary/90 transition-colors"
                >
                  <PenLine size={13} /> New Post
                </Link>
              </div>
            </div>

            {/* Mode Tabs */}
            <div className="flex gap-1 mb-4 bg-muted/40 rounded-lg p-0.5 w-fit">
              {(['latest', 'trending'] as FeedMode[]).map(m => (
                <button
                  key={m}
                  onClick={() => switchMode(m)}
                  className={`px-3 py-1 rounded-md text-xs font-medium transition-all capitalize ${
                    mode === m ? 'bg-background shadow-sm text-foreground' : 'text-muted-foreground hover:text-foreground'
                  }`}
                >
                  {m === 'trending' ? '🔥 ' : '🕐 '}{m}
                </button>
              ))}
            </div>

            {/* Posts */}
            {loading ? (
              <div className="flex items-center justify-center py-16 text-muted-foreground">
                <Loader2 size={20} className="animate-spin" />
              </div>
            ) : (
              <div className="space-y-3">
                {posts.map(post => {
                  const authorName = post.author?.displayName || post.author?.email?.split('@')[0] || 'Anonymous';
                  const institution = post.author?.institution;
                  return (
                    <div key={post.id} className="p-4 rounded-xl border border-border bg-card hover:border-primary/40 transition-colors">
                      <div className="flex items-center gap-2.5 mb-2.5">
                        <div className="w-9 h-9 rounded-full bg-gradient-to-br from-primary/30 to-emerald-500/30 flex items-center justify-center text-xs font-bold shrink-0">
                          {authorName[0]?.toUpperCase()}
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-1.5 flex-wrap">
                            <span className="text-sm font-semibold truncate">{authorName}</span>
                            {post.isVerified && (
                              <span className="text-[9px] bg-primary/10 text-primary px-1.5 py-0.5 rounded-full font-medium shrink-0">Verified</span>
                            )}
                          </div>
                          <div className="text-[10px] text-muted-foreground">
                            {institution && `${institution} · `}{timeAgo(post.createdAt)}
                          </div>
                        </div>
                      </div>
                      {post.title && <p className="text-sm font-semibold mb-1">{post.title}</p>}
                      <p className="text-sm mb-3 leading-relaxed">{post.content}</p>
                      {post.tags?.length > 0 && (
                        <div className="flex flex-wrap gap-1 mb-3">
                          {post.tags.map((t: any) => (
                            <span key={t.name} className="text-[9px] bg-muted px-2 py-0.5 rounded-full text-muted-foreground">#{t.name}</span>
                          ))}
                        </div>
                      )}
                      <div className="flex items-center gap-4 text-xs text-muted-foreground">
                        <button className="flex items-center gap-1 hover:text-primary transition-colors">
                          <ArrowUp size={12} /> {post.upvotes ?? post._count?.votes ?? 0}
                        </button>
                        <button className="flex items-center gap-1 hover:text-primary transition-colors">
                          <MessageSquare size={12} /> {post._count?.comments ?? 0}
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </div>

        {/* Panel 3: Chat Community & Friends — equal flex-1 */}
        <div className="flex-1 min-w-0 border-l border-border overflow-y-auto hidden lg:block">
          <ChatFriendsPanel />
        </div>
      </div>
    </AppShell>
  );
}
