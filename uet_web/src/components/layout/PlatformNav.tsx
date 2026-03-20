'use client';

import Link from 'next/link';
import { useParams, usePathname } from 'next/navigation';
import { Sparkles, Search, Bell } from 'lucide-react';
import { LocaleSwitcher } from '@/components/locale-switcher';
import { ThemeToggle } from '@/components/theme-toggle';
import { useState, useEffect } from 'react';

const NAV_ITEMS = [
  { href: '/feed', label: 'Feed' },
  { href: '/messages', label: 'Messages' },
  { href: '/workspaces', label: 'Workspaces' },
  { href: '/docs', label: 'Docs' },
  { href: '/chat', label: 'Workchat', icon: Sparkles },
];

export default function PlatformNav() {
  const params = useParams();
  const pathname = usePathname();
  const locale = (params?.locale as string) || 'en';
  const [userId, setUserId] = useState<string | null>(null);
  const [initials, setInitials] = useState('U');

  useEffect(() => {
    try {
      const stored = localStorage.getItem('user');
      if (stored) {
        const user = JSON.parse(stored);
        setUserId(user.id);
        setInitials((user.display_name || user.email)?.[0]?.toUpperCase() || 'U');
      }
    } catch {}
  }, []);

  function isActive(href: string) {
    return pathname?.includes(href);
  }

  return (
    <header className="sticky top-0 z-50 flex items-center justify-between h-14 px-6 border-b border-border bg-background/80 backdrop-blur-md">
      <div className="flex items-center gap-6">
        <Link href={`/${locale}`} className="flex items-center gap-2 font-bold text-base hover:opacity-80 transition-opacity">
          <img src="/logo.png" alt="UET" className="w-6 h-6 object-contain" />
          <span className="hidden sm:inline">UET</span>
        </Link>
        <nav className="hidden md:flex items-center gap-1">
          {NAV_ITEMS.map(item => {
            const Icon = item.icon;
            return (
              <Link
                key={item.href}
                href={`/${locale}${item.href}`}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
                  isActive(item.href)
                    ? 'text-primary bg-primary/10'
                    : 'text-muted-foreground hover:text-foreground hover:bg-muted'
                }`}
              >
                {Icon && <Icon size={13} />}
                {item.label}
              </Link>
            );
          })}
        </nav>
      </div>

      <div className="flex items-center gap-2">
        <Link
          href={`/${locale}/search`}
          className="p-2 rounded-lg hover:bg-muted text-muted-foreground hover:text-foreground transition-colors"
        >
          <Search size={16} />
        </Link>
        <button className="p-2 rounded-lg hover:bg-muted text-muted-foreground hover:text-foreground transition-colors relative">
          <Bell size={16} />
        </button>
        <LocaleSwitcher />
        <ThemeToggle />
        {userId ? (
          <Link
            href={`/${locale}/account`}
            className="w-7 h-7 rounded-full bg-gradient-to-br from-primary to-emerald-600 flex items-center justify-center text-primary-foreground text-xs font-bold ml-1"
          >
            {initials}
          </Link>
        ) : (
          <Link
            href={`/${locale}/auth/login`}
            className="px-3 py-1.5 rounded-lg bg-primary text-primary-foreground text-xs font-semibold hover:bg-primary/90 ml-1"
          >
            Sign In
          </Link>
        )}
      </div>
    </header>
  );
}
