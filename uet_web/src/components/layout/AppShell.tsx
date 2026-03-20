'use client';

import { ReactNode } from 'react';
import Link from 'next/link';
import { useParams, usePathname } from 'next/navigation';
import { Sparkles, Home, Newspaper, FolderKanban, Search } from 'lucide-react';
import MenuPopover from '@/components/layout/MenuPopover';
import MessengerPopover from '@/components/chat/MessengerPopover';
import NotificationBell from '@/components/layout/NotificationBell';
import ProfilePopover from '@/components/layout/ProfilePopover';
import { useChatContext } from '@/components/chat/ChatProvider';

const NAV_LINKS = [
  { href: '/feed', label: 'Feed', icon: Home },
  { href: '/workspaces', label: 'Projects', icon: FolderKanban },
  { href: '/chat', label: 'Workchat', icon: Sparkles },
  { href: '/news', label: 'News', icon: Newspaper },
];

interface AppShellProps {
  children: ReactNode;
  hideNav?: boolean;
}

export default function AppShell({ children, hideNav = false }: AppShellProps) {
  const params = useParams();
  const pathname = usePathname();
  const locale = (params?.locale as string) || 'en';
  const { openChat } = useChatContext();

  function isActive(href: string) {
    return pathname?.includes(href);
  }

  if (hideNav) return <>{children}</>;

  return (
    <div className="flex flex-col h-screen bg-background text-foreground">
      {/* Universal Navbar */}
      <nav className="shrink-0 h-14 flex items-center justify-between px-4 border-b border-border bg-background/80 backdrop-blur-md z-50">
        {/* Left: Logo */}
        <Link href={`/${locale}`} className="flex items-center gap-2 font-bold text-base hover:opacity-80 transition-opacity shrink-0">
          <img src="/logo.png" alt="UET" className="w-7 h-7 object-contain" />
          <span className="hidden sm:inline text-sm">UET</span>
        </Link>

        {/* Center: Nav links */}
        <div className="hidden md:flex items-center gap-1 mx-4">
          {NAV_LINKS.map(item => {
            const Icon = item.icon;
            const active = isActive(item.href);
            return (
              <Link
                key={item.href}
                href={`/${locale}${item.href}`}
                className={`flex items-center gap-1.5 px-4 py-2 rounded-lg text-xs font-medium transition-colors ${
                  active
                    ? 'text-primary bg-primary/10'
                    : 'text-muted-foreground hover:text-foreground hover:bg-muted'
                }`}
              >
                <Icon size={15} />
                {item.label}
              </Link>
            );
          })}
        </div>

        {/* Right: FB-style action icons */}
        <div className="flex items-center gap-1.5 shrink-0">
          <MenuPopover />
          <Link
            href={`/${locale}/search`}
            className="w-9 h-9 rounded-full bg-muted/50 hover:bg-muted flex items-center justify-center transition-colors"
            title="Search"
          >
            <Search size={16} className="text-muted-foreground" />
          </Link>
          <MessengerPopover onOpenChat={(contact) => openChat(contact)} />
          <NotificationBell />
          <ProfilePopover />
        </div>
      </nav>

      {/* Page content */}
      <div className="flex-1 overflow-hidden">
        {children}
      </div>

      {/* Mobile bottom nav */}
      <div className="md:hidden shrink-0 flex border-t border-border bg-card">
        {NAV_LINKS.slice(0, 5).map(item => {
          const Icon = item.icon;
          const active = isActive(item.href);
          return (
            <Link
              key={item.href}
              href={`/${locale}${item.href}`}
              className={`flex-1 flex flex-col items-center gap-0.5 py-2 text-[10px] font-medium transition-colors ${
                active ? 'text-primary' : 'text-muted-foreground'
              }`}
            >
              <Icon size={18} />
              {item.label}
            </Link>
          );
        })}
      </div>
    </div>
  );
}
