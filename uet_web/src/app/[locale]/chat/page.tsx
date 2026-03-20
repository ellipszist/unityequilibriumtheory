'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { LocaleSwitcher } from "@/components/locale-switcher";
import { ThemeToggle } from "@/components/theme-toggle";
import SourcePanel from '@/components/workchat/SourcePanel';
import ChatPanel from '@/components/workchat/ChatPanel';
import OutputPanel from '@/components/workchat/OutputPanel';

export default function ChatPage() {
  const params = useParams();
  const locale = params?.locale as string || 'en';
  
  const [sources, setSources] = useState<any[]>([]);
  const [isComputing, setIsComputing] = useState(false);
  const [miningStatus, setMiningStatus] = useState<any>(null);

  const handleSourceAdd = (source: any) => {
    setSources([...sources, source]);
  };

  return (
    <div className="flex flex-col h-screen w-full bg-background overflow-hidden text-sm">
      {/* Header (Matched with user image) */}
      <header className="flex items-center justify-between h-14 px-6 border-b border-border bg-background shrink-0">
        <div className="flex items-center gap-6">
          <Link href="/" className="flex items-center gap-2 font-bold text-base hover:opacity-80 transition-opacity">
            <img src="/logo.png" alt="UET Logo" className="w-6 h-6 object-contain" />
            <span className="hidden sm:inline">UET Platform</span>
          </Link>
          <nav className="hidden md:flex items-center gap-6 text-xs text-muted-foreground font-medium">
            <Link href={`/${locale}/docs`} className="hover:text-foreground transition-colors">Docs</Link>
            <Link href={`/${locale}/chat`} className="text-primary font-semibold">Workchat Studio</Link>
            <Link href={`/${locale}/topics`} className="hover:text-foreground transition-colors">News</Link>
            <Link href={`/${locale}/account`} className="hover:text-foreground transition-colors">Overview</Link>
          </nav>
        </div>
        
        <div className="flex items-center gap-3">
          <LocaleSwitcher />
          <ThemeToggle />
        </div>
      </header>

      {/* Main Studio Area */}
      <div className="flex h-[calc(100vh-56px)] w-full overflow-hidden">
        {/* Panel 1: Source (Left) */}
        <div className="w-1/4 min-w-[280px] max-w-[350px] border-r border-border h-full">
          <SourcePanel sources={sources} onSourceAdd={handleSourceAdd} />
        </div>

        {/* Panel 2: Studio / Chat (Center) */}
        <div className="flex-1 border-r border-border h-full flex flex-col bg-muted/5">
          <ChatPanel 
            activeSources={sources} 
            setIsComputing={setIsComputing}
            setMiningStatus={setMiningStatus}
          />
        </div>

        {/* Panel 3: Output / Dashboard (Right) */}
        <div className="w-1/3 min-w-[300px] max-w-[400px] h-full bg-muted/10">
          <OutputPanel 
            isComputing={isComputing}
            miningStatus={miningStatus}
          />
        </div>
      </div>
    </div>
  );
}
