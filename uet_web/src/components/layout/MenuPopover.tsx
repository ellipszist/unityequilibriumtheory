'use client';

import { useState, useRef, useEffect } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import {
  LayoutGrid, Users, BookOpen, Newspaper, FlaskConical,
  FolderKanban, Sparkles, MessageSquare, Bell, CreditCard,
  Terminal, Github, ExternalLink, Zap, Search
} from 'lucide-react';

const MENU_SECTIONS = [
  {
    title: 'Platform',
    items: [
      { icon: Newspaper, label: 'News', desc: 'Latest UET research updates', href: '/news', color: 'text-blue-500', bg: 'bg-blue-500/10' },
      { icon: FolderKanban, label: 'Projects', desc: 'Collaborative research workspaces', href: '/workspaces', color: 'text-orange-500', bg: 'bg-orange-500/10' },
      { icon: Users, label: 'Community', desc: 'Connect with researchers', href: '/feed', color: 'text-green-500', bg: 'bg-green-500/10' },
      { icon: MessageSquare, label: 'Messages', desc: 'Channels and direct messages', href: '/messages', color: 'text-sky-500', bg: 'bg-sky-500/10' },
    ],
  },
  {
    title: 'Tools',
    items: [
      { icon: Sparkles, label: 'Workchat', desc: 'AI-powered research assistant', href: '/chat', color: 'text-primary', bg: 'bg-primary/10' },
      { icon: Search, label: 'Search', desc: 'Search across all content', href: '/search', color: 'text-muted-foreground', bg: 'bg-muted' },
      { icon: Bell, label: 'Notifications', desc: 'Your activity and updates', href: '#', color: 'text-yellow-500', bg: 'bg-yellow-500/10' },
      { icon: CreditCard, label: 'Credits', desc: 'Manage your UET credits', href: '/account/billing', color: 'text-emerald-500', bg: 'bg-emerald-500/10' },
    ],
  },
  {
    title: 'More from UET',
    items: [
      {
        icon: BookOpen,
        label: 'Documentation',
        desc: 'Guides, API reference & tutorials',
        href: '/docs',
        color: 'text-indigo-500',
        bg: 'bg-indigo-500/10',
      },
      {
        icon: Github,
        label: 'GitHub',
        desc: 'View source code on GitHub',
        href: 'https://github.com/unityequilibrium/UnityEquilibriumTheory',
        external: true,
        color: 'text-foreground',
        bg: 'bg-muted',
      },
      {
        icon: Terminal,
        label: 'Install Library',
        desc: 'pip install git+https://github.com/unityequilibrium/UnityEquilibriumTheory.git',
        href: 'https://github.com/unityequilibrium/UnityEquilibriumTheory',
        external: true,
        color: 'text-green-600',
        bg: 'bg-green-500/10',
        mono: true,
      },
      {
        icon: Zap,
        label: 'Developer API',
        desc: 'REST & WebSocket API for developers',
        href: '/docs/api',
        color: 'text-amber-500',
        bg: 'bg-amber-500/10',
      },
    ],
  },
];

export default function MenuPopover() {
  const params = useParams();
  const locale = (params?.locale as string) || 'en';
  const [open, setOpen] = useState(false);
  const [search, setSearch] = useState('');
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false);
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const filteredSections = search.trim()
    ? MENU_SECTIONS.map(s => ({
        ...s,
        items: s.items.filter(
          i => i.label.toLowerCase().includes(search.toLowerCase()) ||
               i.desc.toLowerCase().includes(search.toLowerCase())
        ),
      })).filter(s => s.items.length > 0)
    : MENU_SECTIONS;

  return (
    <div ref={ref} className="relative">
      <button
        onClick={() => setOpen(!open)}
        className={`w-9 h-9 rounded-full flex items-center justify-center transition-colors ${
          open
            ? 'bg-primary/10 text-primary'
            : 'bg-muted/50 hover:bg-muted text-muted-foreground hover:text-foreground'
        }`}
        title="Menu"
      >
        <LayoutGrid size={17} />
      </button>

      {open && (
        <div className="absolute right-0 top-full mt-2 w-[340px] rounded-2xl border border-border bg-card shadow-2xl z-50 overflow-hidden">
          {/* Header */}
          <div className="p-3 border-b border-border">
            <h3 className="text-lg font-bold px-1 mb-2">Menu</h3>
            <div className="relative">
              <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
              <input
                type="text"
                value={search}
                onChange={e => setSearch(e.target.value)}
                placeholder="Search menu..."
                className="w-full pl-9 pr-3 py-2 rounded-full bg-muted/50 text-xs outline-none focus:bg-muted placeholder:text-muted-foreground"
              />
            </div>
          </div>

          {/* Sections */}
          <div className="max-h-[480px] overflow-y-auto p-3 space-y-4">
            {filteredSections.map(section => (
              <div key={section.title}>
                <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wider px-2 mb-1.5">
                  {section.title}
                </p>
                <div className="space-y-0.5">
                  {section.items.map(item => {
                    const Icon = item.icon;
                    const href = item.external ? item.href : `/${locale}${item.href}`;
                    const Tag = item.external ? 'a' : Link;
                    const extraProps = item.external
                      ? { href, target: '_blank', rel: 'noopener noreferrer' }
                      : { href };

                    return (
                      <Tag
                        key={item.label}
                        {...(extraProps as any)}
                        onClick={() => setOpen(false)}
                        className="flex items-center gap-3 px-3 py-2.5 rounded-xl hover:bg-muted/60 transition-colors"
                      >
                        <div className={`w-10 h-10 rounded-full ${item.bg} flex items-center justify-center shrink-0`}>
                          <Icon size={18} className={item.color} />
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium flex items-center gap-1">
                            {item.label}
                            {item.external && <ExternalLink size={10} className="text-muted-foreground" />}
                          </p>
                          <p className={`text-xs text-muted-foreground truncate ${(item as any).mono ? 'font-mono' : ''}`}>
                            {item.desc}
                          </p>
                        </div>
                      </Tag>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
