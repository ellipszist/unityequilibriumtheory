'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import Link from 'next/link';
import { useParams, useSearchParams } from 'next/navigation';
import { PenSquare, TrendingUp, Clock, Users, Sparkles } from 'lucide-react';
import { LocaleSwitcher } from '@/components/locale-switcher';
import { ThemeToggle } from '@/components/theme-toggle';
import FeedCard from '@/components/feed/FeedCard';

type FeedMode = 'latest' | 'trending' | 'following';

interface PostData {
  id: string;
  title: string;
  content: string;
  upvotes: number;
  isVerified?: boolean;
  createdAt: string;
  author: {
    id: string;
    email: string;
    displayName?: string | null;
    avatarUrl?: string | null;
    institution?: string | null;
    reputation?: number;
  };
  tags: { id: string; name: string }[];
  _count: { comments: number; votes: number };
}

export default function FeedPage() {
  const params = useParams();
  const searchParams = useSearchParams();
  const locale = (params?.locale as string) || 'en';
  const tagFilter = searchParams.get('tag');

  const [posts, setPosts] = useState<PostData[]>([]);
  const [mode, setMode] = useState<FeedMode>('latest');
  const [loading, setLoading] = useState(true);
  const [hasMore, setHasMore] = useState(false);
  const [cursor, setCursor] = useState<string | null>(null);
  const [currentUserId, setCurrentUserId] = useState<string | undefined>();
  const observerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    try {
      const stored = localStorage.getItem('user');
      if (stored) {
        const user = JSON.parse(stored);
        setCurrentUserId(user.id);
      }
    } catch { /* not logged in */ }
  }, []);

  const fetchPosts = useCallback(async (reset = false) => {
    setLoading(true);
    const params = new URLSearchParams();
    params.set('mode', mode);
    params.set('limit', '20');
    if (tagFilter) params.set('tag', tagFilter);
    if (currentUserId) params.set('userId', currentUserId);
    if (!reset && cursor) params.set('cursor', cursor);

    try {
      const res = await fetch(`/api/feed?${params.toString()}`);
      if (res.ok) {
        const data = await res.json();
        setPosts(prev => reset ? data.posts : [...prev, ...data.posts]);
        setCursor(data.nextCursor);
        setHasMore(data.hasMore);
      }
    } catch (err) {
      console.error('Feed fetch error:', err);
    } finally {
      setLoading(false);
    }
  }, [mode, tagFilter, cursor, currentUserId]);

  useEffect(() => {
    setPosts([]);
    setCursor(null);
    fetchPosts(true);
  }, [mode, tagFilter]);

  // Infinite scroll observer
  useEffect(() => {
    if (!observerRef.current || !hasMore) return;
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting && !loading) fetchPosts(); },
      { threshold: 0.5 }
    );
    observer.observe(observerRef.current);
    return () => observer.disconnect();
  }, [hasMore, loading, fetchPosts]);

  const modes: { key: FeedMode; label: string; icon: typeof Clock }[] = [
    { key: 'latest', label: 'Latest', icon: Clock },
    { key: 'trending', label: 'Trending', icon: TrendingUp },
    { key: 'following', label: 'Following', icon: Users },
  ];

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
            <Link href={`/${locale}/docs`} className="hover:text-foreground transition-colors">Docs</Link>
            <Link href={`/${locale}/feed`} className="text-primary font-semibold">Feed</Link>
            <Link href={`/${locale}/chat`} className="hover:text-foreground transition-colors flex items-center gap-1">
              <Sparkles className="w-3.5 h-3.5" /> Workchat
            </Link>
            <Link href={`/${locale}/topics`} className="hover:text-foreground transition-colors">Topics</Link>
            <Link href={`/${locale}/account`} className="hover:text-foreground transition-colors">Account</Link>
          </nav>
        </div>
        <div className="flex items-center gap-3">
          <LocaleSwitcher />
          <ThemeToggle />
        </div>
      </header>

      <div className="max-w-2xl mx-auto w-full py-6 px-4">
        {/* Top bar: mode tabs + create button */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-1 p-1 rounded-lg bg-muted/50">
            {modes.map(({ key, label, icon: Icon }) => (
              <button
                key={key}
                onClick={() => setMode(key)}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
                  mode === key
                    ? 'bg-background text-foreground shadow-sm'
                    : 'text-muted-foreground hover:text-foreground'
                }`}
              >
                <Icon size={13} />
                {label}
              </button>
            ))}
          </div>

          <Link
            href={`/${locale}/feed/new`}
            className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-primary text-primary-foreground text-xs font-semibold hover:bg-primary/90 transition-colors"
          >
            <PenSquare size={14} />
            New Post
          </Link>
        </div>

        {/* Tag filter indicator */}
        {tagFilter && (
          <div className="flex items-center gap-2 mb-4 text-sm">
            <span className="text-muted-foreground">Filtering by:</span>
            <span className="px-2.5 py-0.5 rounded-full bg-primary/10 text-primary text-xs font-medium">
              #{tagFilter}
            </span>
            <Link href={`/${locale}/feed`} className="text-xs text-muted-foreground hover:text-foreground ml-1">
              Clear
            </Link>
          </div>
        )}

        {/* Feed */}
        <div className="space-y-4">
          {posts.map(post => (
            <FeedCard key={post.id} post={post} currentUserId={currentUserId} />
          ))}

          {loading && (
            <div className="flex justify-center py-8">
              <div className="animate-spin w-6 h-6 border-2 border-primary border-t-transparent rounded-full" />
            </div>
          )}

          {!loading && posts.length === 0 && (
            <div className="text-center py-16 text-muted-foreground">
              <PenSquare size={32} className="mx-auto mb-3 opacity-40" />
              <p className="text-base font-medium mb-1">No posts yet</p>
              <p className="text-xs">Be the first to share your research!</p>
            </div>
          )}

          {/* Infinite scroll trigger */}
          {hasMore && <div ref={observerRef} className="h-4" />}
        </div>
      </div>
    </div>
  );
}
