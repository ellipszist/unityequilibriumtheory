'use client';

import { ReactNode, useState } from 'react';
import Link from 'next/link';
import { useParams, usePathname } from 'next/navigation';
import { Sparkles, Home, Newspaper, FolderKanban, Wallet } from 'lucide-react';
import MenuPopover from '@/components/layout/MenuPopover';
import MessengerPopover from '@/components/chat/MessengerPopover';
import NotificationBell from '@/components/layout/NotificationBell';
import ProfilePopover from '@/components/layout/ProfilePopover';
import ChatHistorySidebar from '@/components/chat/ChatHistorySidebar';
import { useChatContext } from '@/components/chat/ChatProvider';

const NAV_LINKS = [
  { href: '/news', label: 'News', icon: Newspaper },
  { href: '/workchat', label: 'WorkChat', icon: Sparkles },
  { href: '/community', label: 'Community', icon: Home },
  { href: '/project', label: 'Project', icon: FolderKanban },
  { href: '/economy', label: 'Economy', icon: Wallet },
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
  const [chatHistoryOpen, setChatHistoryOpen] = useState(false);

  function isActive(href: string) {
    return pathname?.includes(href);
  }

  if (hideNav) return <>{children}</>;

  return (
    <div className="flex flex-col h-screen bg-background text-foreground">
      {/* Universal Navbar */}
      <nav className="shrink-0 h-14 flex items-center justify-between px-4 border-b border-border bg-background/80 backdrop-blur-md z-50">
        {/* Left: Logo → toggles Chat History sidebar */}
        <button
          onClick={() => setChatHistoryOpen(v => !v)}
          className={`flex items-center gap-2 font-bold text-base transition-opacity shrink-0 rounded-lg px-2 py-1 ${
            chatHistoryOpen ? 'opacity-100 bg-primary/10 text-primary' : 'hover:opacity-80'
          }`}
          title="Chat History"
        >
          <img src="/logo.png" alt="UET" className="w-7 h-7 object-contain" />
          <span className="hidden sm:inline text-sm">UET</span>
        </button>

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
          <MessengerPopover onOpenChat={(contact) => openChat(contact)} />
          <NotificationBell />
          <ProfilePopover />
        </div>
      </nav>

      {/* Page content — shifts left when chat history open */}
      <div className={`flex-1 overflow-hidden transition-[margin] duration-200 ${chatHistoryOpen ? 'mr-72' : 'mr-0'}`}>
        {children}
      </div>

      {/* Chat History Sidebar (right, persistent across all pages) */}
      <ChatHistorySidebar
        open={chatHistoryOpen}
        onClose={() => setChatHistoryOpen(false)}
      />

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
