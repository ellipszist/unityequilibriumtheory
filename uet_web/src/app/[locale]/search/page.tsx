'use client';

import { useState, useEffect, useCallback } from 'react';
import Link from 'next/link';
import { useParams, useSearchParams } from 'next/navigation';
import { Search as SearchIcon, FileText, User, Hash, Clock } from 'lucide-react';
import { LocaleSwitcher } from '@/components/locale-switcher';
import { ThemeToggle } from '@/components/theme-toggle';

type SearchType = 'all' | 'posts' | 'users';

export default function SearchPage() {
  const params = useParams();
  const searchParams = useSearchParams();
  const locale = (params?.locale as string) || 'en';
  const initialQuery = searchParams.get('q') || '';

  const [query, setQuery] = useState(initialQuery);
  const [type, setType] = useState<SearchType>('all');
  const [results, setResults] = useState<{ posts: any[]; users: any[] }>({ posts: [], users: [] });
  const [loading, setLoading] = useState(false);

  const doSearch = useCallback(async (q: string) => {
    if (q.length < 2) { setResults({ posts: [], users: [] }); return; }
    setLoading(true);
    try {
      const res = await fetch(`/api/search?q=${encodeURIComponent(q)}&type=${type}`);
      if (res.ok) setResults(await res.json());
    } catch {}
    setLoading(false);
  }, [type]);

  useEffect(() => {
    const timer = setTimeout(() => { if (query.trim()) doSearch(query.trim()); }, 300);
    return () => clearTimeout(timer);
  }, [query, doSearch]);

  const types: { key: SearchType; label: string; icon: typeof FileText }[] = [
    { key: 'all', label: 'All', icon: SearchIcon },
    { key: 'posts', label: 'Posts', icon: FileText },
    { key: 'users', label: 'People', icon: User },
  ];

  return (
    <div className="flex flex-col min-h-screen bg-background text-foreground text-sm">
      <header className="sticky top-0 z-50 flex items-center justify-between h-14 px-6 border-b border-border bg-background/80 backdrop-blur-md">
        <div className="flex items-center gap-6">
          <Link href="/" className="flex items-center gap-2 font-bold text-base">
            <img src="/logo.png" alt="UET" className="w-6 h-6 object-contain" />
            <span className="hidden sm:inline">UET</span>
          </Link>
          <nav className="hidden md:flex items-center gap-6 text-xs text-muted-foreground font-medium">
            <Link href={`/${locale}/feed`} className="hover:text-foreground">Feed</Link>
            <Link href={`/${locale}/messages`} className="hover:text-foreground">Messages</Link>
            <Link href={`/${locale}/search`} className="text-primary font-semibold">Search</Link>
          </nav>
        </div>
        <div className="flex items-center gap-3">
          <LocaleSwitcher />
          <ThemeToggle />
        </div>
      </header>

      <div className="max-w-2xl mx-auto w-full py-8 px-4">
        {/* Search input */}
        <div className="relative mb-6">
          <SearchIcon size={18} className="absolute left-4 top-1/2 -translate-y-1/2 text-muted-foreground" />
          <input
            type="text"
            value={query}
            onChange={e => setQuery(e.target.value)}
            placeholder="Search posts, people, topics..."
            autoFocus
            className="w-full pl-12 pr-4 py-3 rounded-xl border border-border bg-background text-base outline-none focus:border-primary/50"
          />
        </div>

        {/* Type tabs */}
        <div className="flex items-center gap-1 mb-6 p-1 rounded-lg bg-muted/50 w-fit">
          {types.map(t => (
            <button
              key={t.key}
              onClick={() => setType(t.key)}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
                type === t.key ? 'bg-background text-foreground shadow-sm' : 'text-muted-foreground hover:text-foreground'
              }`}
            >
              <t.icon size={13} /> {t.label}
            </button>
          ))}
        </div>

        {loading && (
          <div className="flex justify-center py-8">
            <div className="animate-spin w-6 h-6 border-2 border-primary border-t-transparent rounded-full" />
          </div>
        )}

        {!loading && query.length >= 2 && (
          <div className="space-y-6">
            {/* Users */}
            {(type === 'all' || type === 'users') && results.users.length > 0 && (
              <div>
                <h2 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-3">People</h2>
                <div className="space-y-2">
                  {results.users.map((u: any) => {
                    const name = u.displayName || u.name || u.email.split('@')[0];
                    return (
                      <Link
                        key={u.id}
                        href={`/${locale}/profile/${u.id}`}
                        className="flex items-center gap-3 p-3 rounded-xl border border-border hover:border-primary/30 transition-colors"
                      >
                        {u.avatarUrl ? (
                          <img src={u.avatarUrl} className="w-9 h-9 rounded-full object-cover" />
                        ) : (
                          <div className="w-9 h-9 rounded-full bg-primary/10 flex items-center justify-center text-primary font-bold text-sm">
                            {name[0]?.toUpperCase()}
                          </div>
                        )}
                        <div>
                          <p className="font-semibold text-sm">{name}</p>
                          <p className="text-xs text-muted-foreground">{u.institution || u.email}</p>
                        </div>
                        {u.reputation > 0 && (
                          <span className="ml-auto text-xs text-primary font-medium">Rep: {u.reputation}</span>
                        )}
                      </Link>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Posts */}
            {(type === 'all' || type === 'posts') && results.posts.length > 0 && (
              <div>
                <h2 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-3">Posts</h2>
                <div className="space-y-2">
                  {results.posts.map((p: any) => {
                    const authorName = p.author?.displayName || p.author?.name || p.author?.email?.split('@')[0] || 'Unknown';
                    return (
                      <Link
                        key={p.id}
                        href={`/${locale}/post/${p.id}`}
                        className="block p-4 rounded-xl border border-border hover:border-primary/30 transition-colors"
                      >
                        <h3 className="font-semibold mb-1">{p.title}</h3>
                        <p className="text-xs text-muted-foreground line-clamp-2 mb-2">{p.content.slice(0, 200)}</p>
                        <div className="flex items-center gap-3 text-xs text-muted-foreground">
                          <span>{authorName}</span>
                          <span>{p.upvotes} upvotes</span>
                          <span>{p._count?.comments || 0} comments</span>
                          {p.tags?.[0] && <span className="text-primary">#{p.tags[0].name}</span>}
                          <span className="flex items-center gap-1 ml-auto"><Clock size={11} />{new Date(p.createdAt).toLocaleDateString()}</span>
                        </div>
                      </Link>
                    );
                  })}
                </div>
              </div>
            )}

            {/* No results */}
            {results.posts.length === 0 && results.users.length === 0 && (
              <div className="text-center py-12 text-muted-foreground">
                <SearchIcon size={40} className="mx-auto mb-3 opacity-30" />
                <p className="font-medium">No results for "{query}"</p>
                <p className="text-xs mt-1">Try different keywords or check your spelling</p>
              </div>
            )}
          </div>
        )}

        {!loading && query.length < 2 && (
          <div className="text-center py-16 text-muted-foreground">
            <SearchIcon size={40} className="mx-auto mb-3 opacity-20" />
            <p className="text-sm">Type at least 2 characters to search</p>
          </div>
        )}
      </div>
    </div>
  );
}
