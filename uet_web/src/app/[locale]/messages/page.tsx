'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { MessageSquare, Hash, Users, Sparkles } from 'lucide-react';
import { LocaleSwitcher } from '@/components/locale-switcher';
import { ThemeToggle } from '@/components/theme-toggle';
import EmbeddedChat from '@/components/chat/EmbeddedChat';

const DEFAULT_CHANNELS = [
  { name: 'general', icon: Hash, desc: 'Platform-wide discussion' },
  { name: 'research', icon: Hash, desc: 'General research discussion' },
  { name: 'help', icon: MessageSquare, desc: 'Get help with the platform' },
  { name: 'ai-chat', icon: Sparkles, desc: 'Interact with UET AI Agent' },
];

export default function MessagesPage() {
  const params = useParams();
  const locale = (params?.locale as string) || 'en';
  const [activeChannel, setActiveChannel] = useState<string | undefined>(undefined);

  return (
    <div className="flex flex-col h-screen bg-background text-foreground text-sm">
      {/* Header */}
      <header className="shrink-0 flex items-center justify-between h-14 px-6 border-b border-border bg-background/80 backdrop-blur-md">
        <div className="flex items-center gap-6">
          <Link href="/" className="flex items-center gap-2 font-bold text-base hover:opacity-80 transition-opacity">
            <img src="/logo.png" alt="UET Logo" className="w-6 h-6 object-contain" />
            <span className="hidden sm:inline">UET Platform</span>
          </Link>
          <nav className="hidden md:flex items-center gap-6 text-xs text-muted-foreground font-medium">
            <Link href={`/${locale}/feed`} className="hover:text-foreground transition-colors">Feed</Link>
            <Link href={`/${locale}/docs`} className="hover:text-foreground transition-colors">Docs</Link>
            <Link href={`/${locale}/messages`} className="text-primary font-semibold">Messages</Link>
            <Link href={`/${locale}/chat`} className="hover:text-foreground transition-colors">Workchat</Link>
            <Link href={`/${locale}/account`} className="hover:text-foreground transition-colors">Account</Link>
          </nav>
        </div>
        <div className="flex items-center gap-3">
          <LocaleSwitcher />
          <ThemeToggle />
        </div>
      </header>

      {/* Main: sidebar + chat */}
      <div className="flex flex-1 overflow-hidden">
        {/* Channel sidebar */}
        <aside className="w-60 shrink-0 border-r border-border bg-muted/20 flex flex-col">
          <div className="p-4">
            <h2 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-3">Channels</h2>
            <div className="space-y-0.5">
              {DEFAULT_CHANNELS.map(ch => (
                <button
                  key={ch.name}
                  onClick={() => setActiveChannel(ch.name)}
                  className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm transition-colors ${
                    activeChannel === ch.name
                      ? 'bg-primary/10 text-primary font-medium'
                      : 'text-muted-foreground hover:text-foreground hover:bg-muted'
                  }`}
                >
                  <ch.icon size={15} />
                  <span className="truncate">{ch.name}</span>
                </button>
              ))}
            </div>
          </div>

          <div className="p-4 border-t border-border">
            <h2 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-3">Direct Messages</h2>
            <p className="text-xs text-muted-foreground px-3">
              Start a conversation from a user's profile page
            </p>
          </div>

          <div className="mt-auto p-4 border-t border-border">
            <Link
              href={`/${locale}/workspaces`}
              className="flex items-center gap-2 px-3 py-2 rounded-lg text-xs font-medium text-muted-foreground hover:text-foreground hover:bg-muted transition-colors"
            >
              <Users size={14} />
              Browse Workspaces
            </Link>
          </div>
        </aside>

        {/* Chat area */}
        <main className="flex-1 flex flex-col">
          {activeChannel ? (
            <EmbeddedChat channel={activeChannel} className="flex-1 rounded-none border-0" />
          ) : (
            <div className="flex-1 flex flex-col items-center justify-center text-muted-foreground">
              <MessageSquare size={48} className="mb-4 opacity-30" />
              <h3 className="text-lg font-semibold mb-1">Welcome to Messages</h3>
              <p className="text-sm">Select a channel from the sidebar to start chatting</p>
              <p className="text-xs mt-6 max-w-sm text-center opacity-60">
                Powered by Rocket.Chat — real-time messaging with channels, DMs, file sharing, and video calls.
              </p>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
