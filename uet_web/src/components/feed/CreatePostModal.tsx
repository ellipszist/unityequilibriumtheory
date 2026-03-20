'use client';

import { useState, useRef, useEffect } from 'react';
import { X, Image, Smile, MapPin, Phone, MoreHorizontal, Globe, ChevronDown } from 'lucide-react';
import { useParams } from 'next/navigation';
import { useRouter } from 'next/navigation';

interface CreatePostModalProps {
  open: boolean;
  onClose: () => void;
  onPosted?: () => void;
}

export default function CreatePostModal({ open, onClose, onPosted }: CreatePostModalProps) {
  const params = useParams();
  const locale = (params?.locale as string) || 'en';
  const router = useRouter();
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [tags, setTags] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [userName, setUserName] = useState('');
  const [userInitials, setUserInitials] = useState('U');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    try {
      const stored = localStorage.getItem('user');
      if (stored) {
        const u = JSON.parse(stored);
        const name = u.display_name || u.name || u.email?.split('@')[0] || 'User';
        setUserName(name);
        setUserInitials(name[0]?.toUpperCase() || 'U');
      }
    } catch {}
  }, []);

  useEffect(() => {
    if (open) {
      setTimeout(() => textareaRef.current?.focus(), 100);
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
      setTitle('');
      setContent('');
      setTags('');
      setError('');
    }
    return () => { document.body.style.overflow = ''; };
  }, [open]);

  async function handleSubmit() {
    if (!content.trim()) return;
    setLoading(true);
    setError('');
    try {
      const token = localStorage.getItem('access_token');
      const res = await fetch('/api/posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...(token ? { Authorization: `Bearer ${token}` } : {}) },
        body: JSON.stringify({
          title: title.trim() || content.trim().slice(0, 80),
          content: content.trim(),
          tags: tags.split(',').map(t => t.trim()).filter(Boolean),
        }),
      });
      if (res.ok) {
        onClose();
        onPosted?.();
      } else {
        const d = await res.json().catch(() => ({}));
        setError(d.error || 'Failed to post');
      }
    } catch {
      setError('Network error');
    } finally {
      setLoading(false);
    }
  }

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4">
      {/* Backdrop */}
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={onClose} />

      {/* Modal */}
      <div className="relative w-full max-w-lg bg-card rounded-2xl shadow-2xl z-10 overflow-hidden">
        {/* Header */}
        <div className="relative flex items-center justify-center py-4 border-b border-border">
          <h2 className="text-base font-bold">Create post</h2>
          <button
            onClick={onClose}
            className="absolute right-4 w-8 h-8 rounded-full bg-muted flex items-center justify-center hover:bg-muted/80 transition-colors"
          >
            <X size={16} />
          </button>
        </div>

        {/* User + audience */}
        <div className="flex items-center gap-3 px-4 pt-4">
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary to-emerald-600 flex items-center justify-center text-white font-bold text-sm shrink-0">
            {userInitials}
          </div>
          <div>
            <p className="font-semibold text-sm">{userName}</p>
            <button className="flex items-center gap-1 text-xs bg-muted px-2 py-0.5 rounded-md mt-0.5 hover:bg-muted/80 transition-colors">
              <Globe size={11} /> Public <ChevronDown size={11} />
            </button>
          </div>
        </div>

        {/* Content input */}
        <div className="px-4 py-3">
          <textarea
            ref={textareaRef}
            value={content}
            onChange={e => setContent(e.target.value)}
            placeholder="What's on your mind?"
            rows={4}
            className="w-full resize-none bg-transparent text-lg placeholder:text-muted-foreground outline-none"
          />
          {/* Optional title */}
          {content.length > 100 && (
            <input
              type="text"
              value={title}
              onChange={e => setTitle(e.target.value)}
              placeholder="Add a title (optional)"
              className="w-full mt-1 px-0 py-1 border-t border-border bg-transparent text-sm outline-none placeholder:text-muted-foreground"
            />
          )}
          {/* Tags */}
          <input
            type="text"
            value={tags}
            onChange={e => setTags(e.target.value)}
            placeholder="Tags (comma separated, e.g. physics, UET)"
            className="w-full mt-2 px-0 py-1 border-t border-border bg-transparent text-xs outline-none placeholder:text-muted-foreground"
          />
        </div>

        {/* Add to post */}
        <div className="mx-4 mb-3 flex items-center justify-between border border-border rounded-xl px-4 py-2.5">
          <span className="text-sm font-medium text-muted-foreground">Add to your post</span>
          <div className="flex items-center gap-3">
            <button className="text-green-500 hover:opacity-70 transition-opacity" title="Photo/Video"><Image size={20} /></button>
            <button className="text-yellow-500 hover:opacity-70 transition-opacity" title="Emoji"><Smile size={20} /></button>
            <button className="text-red-500 hover:opacity-70 transition-opacity" title="Location"><MapPin size={20} /></button>
            <button className="text-blue-500 hover:opacity-70 transition-opacity" title="Contact"><Phone size={20} /></button>
            <button className="text-muted-foreground hover:opacity-70 transition-opacity" title="More"><MoreHorizontal size={20} /></button>
          </div>
        </div>

        {error && (
          <p className="px-4 pb-2 text-xs text-destructive">{error}</p>
        )}

        {/* Submit */}
        <div className="px-4 pb-4">
          <button
            onClick={handleSubmit}
            disabled={!content.trim() || loading}
            className="w-full py-2.5 rounded-xl bg-primary text-primary-foreground font-semibold text-sm hover:bg-primary/90 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? (
              <span className="flex items-center justify-center gap-2">
                <span className="animate-spin w-4 h-4 border-2 border-current border-t-transparent rounded-full" />
                Posting...
              </span>
            ) : 'Post'}
          </button>
        </div>
      </div>
    </div>
  );
}
