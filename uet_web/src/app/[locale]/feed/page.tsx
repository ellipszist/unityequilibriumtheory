'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import Link from 'next/link';
import { useParams, useSearchParams } from 'next/navigation';
import { PenSquare, TrendingUp, Clock, Users, User, MessageCircle } from 'lucide-react';
import CreatePostModal from '@/components/feed/CreatePostModal';
import AppShell from '@/components/layout/AppShell';
import ThreePanelLayout from '@/components/layout/ThreePanelLayout';
import ProfilePanel from '@/components/feed/ProfilePanel';
import ChatFriendsPanel from '@/components/feed/ChatFriendsPanel';
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

  const [showCreateModal, setShowCreateModal] = useState(false);

  const modes: { key: FeedMode; label: string; icon: typeof Clock }[] = [
    { key: 'latest', label: 'Latest', icon: Clock },
    { key: 'trending', label: 'Trending', icon: TrendingUp },
    { key: 'following', label: 'Following', icon: Users },
  ];

  return (
    <AppShell>
      <ThreePanelLayout
        left={<ProfilePanel />}
        right={<ChatFriendsPanel />}
        leftTitle="Profile"
        rightTitle="Chat"
        leftIcon={<User size={18} />}
        rightIcon={<MessageCircle size={18} />}
        leftDefaultWidth={260}
        rightDefaultWidth={280}
        center={
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

          <button
            onClick={() => setShowCreateModal(true)}
            className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-primary text-primary-foreground text-xs font-semibold hover:bg-primary/90 transition-colors"
          >
            <PenSquare size={14} />
            New Post
          </button>
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
        }
      />
      <CreatePostModal
        open={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        onPosted={() => { setShowCreateModal(false); fetchPosts(); }}
      />
    </AppShell>
  );
}
