'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, MapPin, LinkIcon, Calendar, Users, FileText, BadgeCheck } from 'lucide-react';
import { LocaleSwitcher } from '@/components/locale-switcher';
import { ThemeToggle } from '@/components/theme-toggle';

interface ProfileData {
  id: string;
  email: string;
  name?: string | null;
  displayName?: string | null;
  bio?: string | null;
  avatarUrl?: string | null;
  institution?: string | null;
  website?: string | null;
  reputation: number;
  createdAt: string;
  followersCount: number;
  followingCount: number;
  _count: { posts: number; comments: number };
  recentPosts: {
    id: string;
    title: string;
    content: string;
    upvotes: number;
    createdAt: string;
    tags: { id: string; name: string }[];
    _count: { comments: number };
  }[];
}

export default function ProfilePage() {
  const params = useParams();
  const locale = (params?.locale as string) || 'en';
  const userId = params?.userId as string;

  const [profile, setProfile] = useState<ProfileData | null>(null);
  const [loading, setLoading] = useState(true);
  const [isFollowing, setIsFollowing] = useState(false);
  const [currentUserId, setCurrentUserId] = useState<string | null>(null);

  useEffect(() => {
    try {
      const stored = localStorage.getItem('user');
      if (stored) setCurrentUserId(JSON.parse(stored).id);
    } catch {}
  }, []);

  useEffect(() => {
    if (!userId) return;
    fetch(`/api/profile/${userId}`)
      .then(r => r.ok ? r.json() : null)
      .then(data => { if (data) setProfile(data); })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [userId]);

  async function toggleFollow() {
    if (!currentUserId || !userId || currentUserId === userId) return;
    try {
      if (isFollowing) {
        await fetch(`/api/follow/${userId}?followerId=${currentUserId}`, { method: 'DELETE' });
        setIsFollowing(false);
        if (profile) setProfile({ ...profile, followersCount: profile.followersCount - 1 });
      } else {
        await fetch(`/api/follow/${userId}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ followerId: currentUserId }),
        });
        setIsFollowing(true);
        if (profile) setProfile({ ...profile, followersCount: profile.followersCount + 1 });
      }
    } catch {}
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="animate-spin w-8 h-8 border-2 border-primary border-t-transparent rounded-full" />
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center text-muted-foreground">
        User not found
      </div>
    );
  }

  const displayName = profile.displayName || profile.name || profile.email.split('@')[0];
  const initials = displayName[0]?.toUpperCase() || 'U';
  const joinDate = new Date(profile.createdAt).toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
  const isOwnProfile = currentUserId === userId;

  return (
    <div className="flex flex-col min-h-screen bg-background text-foreground text-sm">
      {/* Header */}
      <header className="sticky top-0 z-50 flex items-center justify-between h-14 px-6 border-b border-border bg-background/80 backdrop-blur-md">
        <div className="flex items-center gap-4">
          <Link href={`/${locale}/feed`} className="p-1.5 rounded-lg hover:bg-muted transition-colors">
            <ArrowLeft size={18} />
          </Link>
          <h1 className="font-semibold">{displayName}</h1>
        </div>
        <div className="flex items-center gap-3">
          <LocaleSwitcher />
          <ThemeToggle />
        </div>
      </header>

      <div className="max-w-2xl mx-auto w-full py-8 px-4">
        {/* Profile header */}
        <div className="flex items-start gap-5 mb-6">
          {profile.avatarUrl ? (
            <img src={profile.avatarUrl} alt={displayName} className="w-20 h-20 rounded-full object-cover" />
          ) : (
            <div className="w-20 h-20 rounded-full bg-primary/20 flex items-center justify-center text-primary text-2xl font-bold shrink-0">
              {initials}
            </div>
          )}

          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-1">
              <h2 className="text-xl font-bold truncate">{displayName}</h2>
              {profile.reputation > 100 && <BadgeCheck size={18} className="text-primary shrink-0" />}
            </div>

            <p className="text-muted-foreground text-xs mb-3">@{profile.email.split('@')[0]}</p>

            {profile.bio && (
              <p className="text-sm leading-relaxed mb-3">{profile.bio}</p>
            )}

            <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-muted-foreground">
              {profile.institution && (
                <span className="flex items-center gap-1"><MapPin size={12} />{profile.institution}</span>
              )}
              {profile.website && (
                <a href={profile.website} target="_blank" rel="noopener" className="flex items-center gap-1 hover:text-primary">
                  <LinkIcon size={12} />{profile.website.replace(/https?:\/\//, '')}
                </a>
              )}
              <span className="flex items-center gap-1"><Calendar size={12} />Joined {joinDate}</span>
            </div>
          </div>
        </div>

        {/* Stats + Follow button */}
        <div className="flex items-center gap-6 mb-8 pb-6 border-b border-border">
          <div className="flex items-center gap-4 text-sm">
            <span><strong>{profile.followingCount}</strong> <span className="text-muted-foreground">Following</span></span>
            <span><strong>{profile.followersCount}</strong> <span className="text-muted-foreground">Followers</span></span>
            <span><strong>{profile._count.posts}</strong> <span className="text-muted-foreground">Posts</span></span>
            <span className="text-muted-foreground">Rep: <strong className="text-primary">{profile.reputation}</strong></span>
          </div>

          {!isOwnProfile && currentUserId && (
            <button
              onClick={toggleFollow}
              className={`ml-auto px-4 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                isFollowing
                  ? 'border border-border text-muted-foreground hover:border-destructive hover:text-destructive'
                  : 'bg-primary text-primary-foreground hover:bg-primary/90'
              }`}
            >
              {isFollowing ? 'Unfollow' : 'Follow'}
            </button>
          )}

          {isOwnProfile && (
            <Link
              href={`/${locale}/profile/edit`}
              className="ml-auto px-4 py-1.5 rounded-lg border border-border text-xs font-semibold hover:bg-muted transition-colors"
            >
              Edit Profile
            </Link>
          )}
        </div>

        {/* Recent posts */}
        <div>
          <h3 className="font-semibold mb-4 flex items-center gap-2">
            <FileText size={16} /> Recent Posts
          </h3>

          {profile.recentPosts.length === 0 ? (
            <p className="text-center text-muted-foreground py-8">No posts yet</p>
          ) : (
            <div className="space-y-3">
              {profile.recentPosts.map(post => (
                <Link
                  key={post.id}
                  href={`/${locale}/post/${post.id}`}
                  className="block p-4 rounded-xl border border-border hover:border-primary/30 transition-colors"
                >
                  <h4 className="font-semibold mb-1">{post.title}</h4>
                  <p className="text-xs text-muted-foreground line-clamp-2 mb-2">
                    {post.content.slice(0, 200)}
                  </p>
                  <div className="flex items-center gap-3 text-xs text-muted-foreground">
                    <span>{post.upvotes} upvotes</span>
                    <span>{post._count.comments} comments</span>
                    {post.tags.length > 0 && (
                      <span className="text-primary">#{post.tags[0].name}</span>
                    )}
                    <span className="ml-auto">{new Date(post.createdAt).toLocaleDateString()}</span>
                  </div>
                </Link>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
