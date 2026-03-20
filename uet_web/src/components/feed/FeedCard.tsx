'use client';

import Link from 'next/link';
import { ArrowBigUp, ArrowBigDown, MessageSquare, BadgeCheck, Clock } from 'lucide-react';
import { useState } from 'react';

interface FeedCardProps {
  post: {
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
  };
  currentUserId?: string;
}

export default function FeedCard({ post, currentUserId }: FeedCardProps) {
  const [votes, setVotes] = useState(post.upvotes);
  const [userVote, setUserVote] = useState<number>(0);

  const authorName = post.author.displayName || post.author.email.split('@')[0];
  const initials = authorName[0]?.toUpperCase() || 'U';
  const timeAgo = getTimeAgo(post.createdAt);
  const excerpt = post.content.length > 280 ? post.content.slice(0, 280) + '...' : post.content;

  async function handleVote(value: number) {
    if (!currentUserId) return;
    const newValue = userVote === value ? 0 : value;
    
    try {
      const res = await fetch(`/api/posts/${post.id}/upvote`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId: currentUserId, value }),
      });
      if (res.ok) {
        const data = await res.json();
        setUserVote(data.value);
        setVotes(prev => prev + (data.value - userVote));
      }
    } catch { /* ignore */ }
  }

  return (
    <article className="rounded-xl border border-border bg-card hover:border-primary/30 transition-colors">
      <div className="p-5">
        {/* Author row */}
        <div className="flex items-center gap-3 mb-3">
          <Link href={`/profile/${post.author.id}`}>
            {post.author.avatarUrl ? (
              <img src={post.author.avatarUrl} alt={authorName} className="w-9 h-9 rounded-full object-cover" />
            ) : (
              <div className="w-9 h-9 rounded-full bg-primary/20 flex items-center justify-center text-primary text-sm font-bold">
                {initials}
              </div>
            )}
          </Link>
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2">
              <Link href={`/profile/${post.author.id}`} className="text-sm font-semibold hover:text-primary transition-colors truncate">
                {authorName}
              </Link>
              {post.isVerified && (
                <BadgeCheck size={14} className="text-primary shrink-0" />
              )}
            </div>
            <div className="flex items-center gap-2 text-xs text-muted-foreground">
              {post.author.institution && <span>{post.author.institution}</span>}
              <span className="flex items-center gap-1"><Clock size={11} />{timeAgo}</span>
            </div>
          </div>
        </div>

        {/* Content */}
        <Link href={`/post/${post.id}`} className="block group">
          <h3 className="text-base font-semibold mb-1.5 group-hover:text-primary transition-colors">
            {post.title}
          </h3>
          <p className="text-sm text-muted-foreground leading-relaxed whitespace-pre-wrap">
            {excerpt}
          </p>
        </Link>

        {/* Tags */}
        {post.tags.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mt-3">
            {post.tags.map(tag => (
              <Link
                key={tag.id}
                href={`/feed?tag=${tag.name}`}
                className="text-[11px] px-2 py-0.5 rounded-full bg-primary/10 text-primary hover:bg-primary/20 transition-colors"
              >
                #{tag.name}
              </Link>
            ))}
          </div>
        )}
      </div>

      {/* Actions bar */}
      <div className="flex items-center gap-4 px-5 py-2.5 border-t border-border text-muted-foreground">
        <div className="flex items-center gap-1">
          <button
            onClick={() => handleVote(1)}
            className={`p-1 rounded hover:bg-primary/10 transition-colors ${userVote === 1 ? 'text-primary' : ''}`}
          >
            <ArrowBigUp size={18} />
          </button>
          <span className={`text-sm font-medium min-w-[2ch] text-center ${votes > 0 ? 'text-primary' : votes < 0 ? 'text-destructive' : ''}`}>
            {votes}
          </span>
          <button
            onClick={() => handleVote(-1)}
            className={`p-1 rounded hover:bg-destructive/10 transition-colors ${userVote === -1 ? 'text-destructive' : ''}`}
          >
            <ArrowBigDown size={18} />
          </button>
        </div>

        <Link href={`/post/${post.id}`} className="flex items-center gap-1.5 text-sm hover:text-primary transition-colors">
          <MessageSquare size={15} />
          <span>{post._count.comments}</span>
        </Link>

        {post.author.reputation !== undefined && post.author.reputation > 0 && (
          <span className="ml-auto text-[11px] text-muted-foreground">
            Rep: {post.author.reputation}
          </span>
        )}
      </div>
    </article>
  );
}

function getTimeAgo(dateStr: string): string {
  const diff = Date.now() - new Date(dateStr).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return 'just now';
  if (mins < 60) return `${mins}m`;
  const hours = Math.floor(mins / 60);
  if (hours < 24) return `${hours}h`;
  const days = Math.floor(hours / 24);
  if (days < 30) return `${days}d`;
  return new Date(dateStr).toLocaleDateString();
}
