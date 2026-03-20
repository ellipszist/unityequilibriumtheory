'use client';

import React, { useState } from 'react';
import AppShell from '@/components/layout/AppShell';
import SourcePanel from '@/components/workchat/SourcePanel';
import ChatPanel from '@/components/workchat/ChatPanel';
import OutputPanel from '@/components/workchat/OutputPanel';

export default function ChatPage() {
  const [sources, setSources] = useState<any[]>([]);
  const [isComputing, setIsComputing] = useState(false);
  const [miningStatus, setMiningStatus] = useState<any>(null);

  const handleSourceAdd = (source: any) => {
    setSources([...sources, source]);
  };

  return (
    <AppShell>
      {/* 3-panel layout: Source | Chat | Output */}
      <div className="flex flex-1 h-full w-full overflow-hidden">
        {/* Panel 1: Source (Left) */}
        <div className="w-1/4 min-w-[240px] max-w-[320px] border-r border-border h-full shrink-0">
          <SourcePanel sources={sources} onSourceAdd={handleSourceAdd} />
        </div>

        {/* Panel 2: Chat (Center) */}
        <div className="flex-1 border-r border-border h-full flex flex-col bg-muted/5 min-w-0">
          <ChatPanel
            activeSources={sources}
            setIsComputing={setIsComputing}
            setMiningStatus={setMiningStatus}
          />
        </div>

        {/* Panel 3: Output (Right) */}
        <div className="w-[320px] max-w-[380px] h-full bg-muted/10 shrink-0">
          <OutputPanel
            isComputing={isComputing}
            miningStatus={miningStatus}
          />
        </div>
      </div>
    </AppShell>
  );
}
