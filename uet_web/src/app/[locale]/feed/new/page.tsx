'use client';

import { useState, useEffect } from 'react';
import { useRouter, useParams } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, Send, X, Plus } from 'lucide-react';
import { ThemeToggle } from '@/components/theme-toggle';

export default function NewPostPage() {
  const router = useRouter();
  const params = useParams();
  const locale = (params?.locale as string) || 'en';

  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [tagInput, setTagInput] = useState('');
  const [tags, setTags] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [userId, setUserId] = useState<string | null>(null);

  useEffect(() => {
    try {
      const stored = localStorage.getItem('user');
      if (stored) {
        const user = JSON.parse(stored);
        setUserId(user.id);
      }
    } catch { /* not logged in */ }
  }, []);

  function addTag() {
    const tag = tagInput.trim().toLowerCase().replace(/[^a-z0-9-_]/g, '');
    if (tag && !tags.includes(tag) && tags.length < 5) {
      setTags([...tags, tag]);
      setTagInput('');
    }
  }

  function removeTag(tag: string) {
    setTags(tags.filter(t => t !== tag));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!title.trim() || !content.trim()) {
      setError('Title and content are required');
      return;
    }
    if (!userId) {
      setError('Please log in to post');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const res = await fetch('/api/posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: title.trim(),
          content: content.trim(),
          authorId: userId,
          tags,
        }),
      });

      if (res.ok) {
        router.push(`/${locale}/feed`);
      } else {
        const data = await res.json();
        setError(data.error || 'Failed to create post');
      }
    } catch {
      setError('Network error');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col min-h-screen bg-background text-foreground text-sm">
      {/* Header */}
      <header className="sticky top-0 z-50 flex items-center justify-between h-14 px-6 border-b border-border bg-background/80 backdrop-blur-md">
        <div className="flex items-center gap-4">
          <Link href={`/${locale}/feed`} className="p-1.5 rounded-lg hover:bg-muted transition-colors">
            <ArrowLeft size={18} />
          </Link>
          <h1 className="font-semibold">New Post</h1>
        </div>
        <ThemeToggle />
      </header>

      <div className="max-w-2xl mx-auto w-full py-8 px-4">
        <form onSubmit={handleSubmit} className="space-y-5">
          {error && (
            <div className="p-3 rounded-lg bg-destructive/10 border border-destructive/30 text-destructive text-sm">
              {error}
            </div>
          )}

          {/* Title */}
          <div>
            <input
              type="text"
              value={title}
              onChange={e => setTitle(e.target.value)}
              placeholder="Post title..."
              maxLength={200}
              className="w-full text-2xl font-bold bg-transparent border-none outline-none placeholder:text-muted-foreground/50"
            />
          </div>

          {/* Content */}
          <div>
            <textarea
              value={content}
              onChange={e => setContent(e.target.value)}
              placeholder="Share your research, findings, or insights... (Markdown supported)"
              rows={12}
              className="w-full bg-transparent border border-border rounded-xl p-4 text-sm leading-relaxed outline-none focus:border-primary/50 resize-none placeholder:text-muted-foreground/50"
            />
            <p className="text-xs text-muted-foreground mt-1.5">
              Supports Markdown and LaTeX (wrap with $..$ for inline, $$...$$ for block)
            </p>
          </div>

          {/* Tags */}
          <div>
            <label className="block text-xs font-medium text-muted-foreground mb-2">
              Tags (up to 5)
            </label>
            <div className="flex flex-wrap items-center gap-2 mb-2">
              {tags.map(tag => (
                <span key={tag} className="flex items-center gap-1 px-2.5 py-1 rounded-full bg-primary/10 text-primary text-xs">
                  #{tag}
                  <button type="button" onClick={() => removeTag(tag)} className="hover:text-destructive">
                    <X size={12} />
                  </button>
                </span>
              ))}
            </div>
            {tags.length < 5 && (
              <div className="flex gap-2">
                <input
                  type="text"
                  value={tagInput}
                  onChange={e => setTagInput(e.target.value)}
                  onKeyDown={e => { if (e.key === 'Enter') { e.preventDefault(); addTag(); } }}
                  placeholder="Add tag..."
                  className="flex-1 px-3 py-2 rounded-lg border border-border bg-transparent text-sm outline-none focus:border-primary/50"
                />
                <button
                  type="button"
                  onClick={addTag}
                  className="px-3 py-2 rounded-lg border border-border hover:bg-muted text-muted-foreground hover:text-foreground transition-colors"
                >
                  <Plus size={16} />
                </button>
              </div>
            )}
          </div>

          {/* Submit */}
          <div className="flex items-center justify-between pt-4 border-t border-border">
            <Link
              href={`/${locale}/feed`}
              className="text-sm text-muted-foreground hover:text-foreground transition-colors"
            >
              Cancel
            </Link>
            <button
              type="submit"
              disabled={loading || !title.trim() || !content.trim()}
              className="flex items-center gap-2 px-6 py-2.5 rounded-lg bg-primary text-primary-foreground font-semibold text-sm hover:bg-primary/90 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? (
                <div className="animate-spin w-4 h-4 border-2 border-current border-t-transparent rounded-full" />
              ) : (
                <Send size={14} />
              )}
              Publish
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
