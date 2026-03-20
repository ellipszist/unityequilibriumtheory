'use client';

import React, { useState } from 'react';
import SourcePanel from './SourcePanel';
import ChatPanel from './ChatPanel';
import OutputPanel from './OutputPanel';

export default function WorkchatStudio() {
  const [sources, setSources] = useState<any[]>([]);
  const [isComputing, setIsComputing] = useState(false);
  const [miningStatus, setMiningStatus] = useState<any>(null);

  const handleSourceAdd = (source: any) => {
    setSources([...sources, source]);
  };

  return (
    <div className="flex h-full w-full bg-background overflow-hidden">
      {/* Panel 1: Source (Left) */}
      <div className="w-1/4 min-w-[250px] max-w-[350px] border-r border-border h-full">
        <SourcePanel sources={sources} onSourceAdd={handleSourceAdd} />
      </div>

      {/* Panel 2: Studio / Chat (Center) */}
      <div className="flex-1 border-r border-border h-full flex flex-col">
        <ChatPanel 
          activeSources={sources} 
          setIsComputing={setIsComputing}
          setMiningStatus={setMiningStatus}
        />
      </div>

      {/* Panel 3: Output / Dashboard (Right) */}
      <div className="w-1/3 min-w-[300px] max-w-[500px] h-full bg-muted/20">
        <OutputPanel 
          isComputing={isComputing}
          miningStatus={miningStatus}
        />
      </div>
    </div>
  );
}
