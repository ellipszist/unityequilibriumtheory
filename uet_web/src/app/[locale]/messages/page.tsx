'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { MessageSquare, Hash, Users, Sparkles } from 'lucide-react';
import AppShell from '@/components/layout/AppShell';
import SidebarLayout from '@/components/layout/SidebarLayout';
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

  const sidebarContent = (
    <div className="flex flex-col h-full">
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
        <p className="text-xs text-muted-foreground px-3">Start a conversation from a user's profile page</p>
      </div>
      <div className="mt-auto p-4 border-t border-border">
        <Link href={`/${locale}/workspaces`} className="flex items-center gap-2 px-3 py-2 rounded-lg text-xs font-medium text-muted-foreground hover:text-foreground hover:bg-muted transition-colors">
          <Users size={14} /> Browse Workspaces
        </Link>
      </div>
    </div>
  );

  return (
    <AppShell>
      <SidebarLayout sidebar={sidebarContent}>
        {activeChannel ? (
          <EmbeddedChat channel={activeChannel} className="h-full rounded-none border-0" />
        ) : (
          <div className="h-full flex flex-col items-center justify-center text-muted-foreground">
            <MessageSquare size={48} className="mb-4 opacity-30" />
            <h3 className="text-lg font-semibold mb-1">Welcome to Messages</h3>
            <p className="text-sm">Select a channel from the sidebar to start chatting</p>
          </div>
        )}
      </SidebarLayout>
    </AppShell>
  );
}
