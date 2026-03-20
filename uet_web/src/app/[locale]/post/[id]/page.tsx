'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, ArrowBigUp, ArrowBigDown, MessageSquare, BadgeCheck, Clock, Send } from 'lucide-react';
import { LocaleSwitcher } from '@/components/locale-switcher';
import { ThemeToggle } from '@/components/theme-toggle';

interface PostDetail {
  id: string;
  title: string;
  content: string;
  upvotes: number;
  isVerified?: boolean;
  createdAt: string;
  author: { id: string; email: string; displayName?: string; avatarUrl?: string; institution?: string; reputation?: number };
  tags: { id: string; name: string }[];
}

interface CommentData {
  id: string;
  content: string;
  upvotes: number;
  createdAt: string;
  author: { id: string; email: string; displayName?: string; avatarUrl?: string };
}

export default function PostDetailPage() {
  const params = useParams();
  const locale = (params?.locale as string) || 'en';
  const postId = params?.id as string;

  const [post, setPost] = useState<PostDetail | null>(null);
  const [comments, setComments] = useState<CommentData[]>([]);
  const [loading, setLoading] = useState(true);
  const [commentText, setCommentText] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [currentUserId, setCurrentUserId] = useState<string | null>(null);
  const [votes, setVotes] = useState(0);
  const [userVote, setUserVote] = useState(0);

  useEffect(() => {
    try {
      const stored = localStorage.getItem('user');
      if (stored) setCurrentUserId(JSON.parse(stored).id);
    } catch {}
  }, []);

  useEffect(() => {
    if (!postId) return;
    Promise.all([
      fetch(`/api/posts/${postId}`).then(r => r.ok ? r.json() : null),
      fetch(`/api/posts/${postId}/comments`).then(r => r.ok ? r.json() : []),
    ]).then(([postData, commentsData]) => {
      if (postData) { setPost(postData); setVotes(postData.upvotes); }
      setComments(commentsData || []);
    }).catch(() => {})
      .finally(() => setLoading(false));
  }, [postId]);

  async function handleVote(value: number) {
    if (!currentUserId || !postId) return;
    try {
      const res = await fetch(`/api/posts/${postId}/upvote`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId: currentUserId, value }),
      });
      if (res.ok) {
        const data = await res.json();
        setVotes(prev => prev + (data.value - userVote));
        setUserVote(data.value);
      }
    } catch {}
  }

  async function submitComment() {
    if (!currentUserId || !commentText.trim() || !postId) return;
    setSubmitting(true);
    try {
      const res = await fetch(`/api/posts/${postId}/comments`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ authorId: currentUserId, content: commentText.trim() }),
      });
      if (res.ok) {
        const newComment = await res.json();
        setComments(prev => [...prev, newComment]);
        setCommentText('');
      }
    } catch {}
    setSubmitting(false);
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="animate-spin w-8 h-8 border-2 border-primary border-t-transparent rounded-full" />
      </div>
    );
  }

  if (!post) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center text-muted-foreground">
        Post not found
      </div>
    );
  }

  const authorName = post.author.displayName || post.author.email?.split('@')[0] || 'Unknown';
  const initials = authorName[0]?.toUpperCase() || 'U';

  return (
    <div className="flex flex-col min-h-screen bg-background text-foreground text-sm">
      <header className="sticky top-0 z-50 flex items-center justify-between h-14 px-6 border-b border-border bg-background/80 backdrop-blur-md">
        <div className="flex items-center gap-4">
          <Link href={`/${locale}/feed`} className="p-1.5 rounded-lg hover:bg-muted transition-colors">
            <ArrowLeft size={18} />
          </Link>
          <span className="font-semibold truncate max-w-xs">{post.title}</span>
        </div>
        <div className="flex items-center gap-3">
          <LocaleSwitcher />
          <ThemeToggle />
        </div>
      </header>

      <div className="max-w-2xl mx-auto w-full py-8 px-4">
        {/* Author */}
        <div className="flex items-center gap-3 mb-5">
          <Link href={`/${locale}/profile/${post.author.id}`}>
            {post.author.avatarUrl ? (
              <img src={post.author.avatarUrl} alt={authorName} className="w-10 h-10 rounded-full object-cover" />
            ) : (
              <div className="w-10 h-10 rounded-full bg-primary/20 flex items-center justify-center text-primary font-bold">
                {initials}
              </div>
            )}
          </Link>
          <div>
            <div className="flex items-center gap-2">
              <Link href={`/${locale}/profile/${post.author.id}`} className="font-semibold hover:text-primary">{authorName}</Link>
              {post.isVerified && <BadgeCheck size={14} className="text-primary" />}
            </div>
            <div className="flex items-center gap-2 text-xs text-muted-foreground">
              {post.author.institution && <span>{post.author.institution}</span>}
              <span className="flex items-center gap-1"><Clock size={11} />{new Date(post.createdAt).toLocaleDateString()}</span>
            </div>
          </div>
        </div>

        {/* Title + Content */}
        <h1 className="text-2xl font-bold mb-4">{post.title}</h1>
        <div className="prose prose-sm dark:prose-invert max-w-none mb-6 whitespace-pre-wrap">
          {post.content}
        </div>

        {/* Tags */}
        {post.tags.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mb-6">
            {post.tags.map(tag => (
              <Link key={tag.id} href={`/${locale}/feed?tag=${tag.name}`}
                className="text-xs px-2.5 py-0.5 rounded-full bg-primary/10 text-primary hover:bg-primary/20">
                #{tag.name}
              </Link>
            ))}
          </div>
        )}

        {/* Vote bar */}
        <div className="flex items-center gap-4 py-4 border-y border-border mb-8">
          <div className="flex items-center gap-1">
            <button onClick={() => handleVote(1)} className={`p-1.5 rounded hover:bg-primary/10 ${userVote === 1 ? 'text-primary' : 'text-muted-foreground'}`}>
              <ArrowBigUp size={20} />
            </button>
            <span className={`text-base font-bold min-w-[3ch] text-center ${votes > 0 ? 'text-primary' : votes < 0 ? 'text-destructive' : ''}`}>{votes}</span>
            <button onClick={() => handleVote(-1)} className={`p-1.5 rounded hover:bg-destructive/10 ${userVote === -1 ? 'text-destructive' : 'text-muted-foreground'}`}>
              <ArrowBigDown size={20} />
            </button>
          </div>
          <span className="flex items-center gap-1.5 text-muted-foreground">
            <MessageSquare size={16} /> {comments.length} comments
          </span>
        </div>

        {/* Comments */}
        <div className="space-y-4 mb-8">
          {comments.map(c => {
            const cName = (c.author as any).displayName || c.author.email?.split('@')[0] || 'User';
            const cInitial = cName[0]?.toUpperCase() || 'U';
            return (
              <div key={c.id} className="flex gap-3">
                <Link href={`/${locale}/profile/${c.author.id}`}>
                  {(c.author as any).avatarUrl ? (
                    <img src={(c.author as any).avatarUrl} className="w-8 h-8 rounded-full object-cover" />
                  ) : (
                    <div className="w-8 h-8 rounded-full bg-muted flex items-center justify-center text-xs font-bold text-muted-foreground">{cInitial}</div>
                  )}
                </Link>
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <Link href={`/${locale}/profile/${c.author.id}`} className="text-sm font-semibold hover:text-primary">{cName}</Link>
                    <span className="text-[11px] text-muted-foreground">{new Date(c.createdAt).toLocaleDateString()}</span>
                  </div>
                  <p className="text-sm leading-relaxed whitespace-pre-wrap">{c.content}</p>
                </div>
              </div>
            );
          })}
        </div>

        {/* Comment input */}
        {currentUserId ? (
          <div className="flex gap-3 items-start">
            <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center text-primary text-xs font-bold shrink-0">You</div>
            <div className="flex-1">
              <textarea
                value={commentText}
                onChange={e => setCommentText(e.target.value)}
                placeholder="Write a comment..."
                rows={3}
                className="w-full px-3 py-2.5 rounded-xl border border-border bg-background text-sm outline-none focus:border-primary/50 resize-none"
              />
              <div className="flex justify-end mt-2">
                <button
                  onClick={submitComment}
                  disabled={submitting || !commentText.trim()}
                  className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-primary text-primary-foreground text-xs font-semibold hover:bg-primary/90 disabled:opacity-40 transition-colors"
                >
                  {submitting ? <div className="animate-spin w-3.5 h-3.5 border-2 border-current border-t-transparent rounded-full" /> : <Send size={13} />}
                  Comment
                </button>
              </div>
            </div>
          </div>
        ) : (
          <div className="text-center py-6 text-muted-foreground">
            <Link href={`/${locale}/auth/login`} className="text-primary hover:underline">Sign in</Link> to leave a comment
          </div>
        )}
      </div>
    </div>
  );
}
