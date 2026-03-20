'use client';

import { useState } from 'react';
import { MessageSquare, ExternalLink, Maximize2, Minimize2 } from 'lucide-react';

interface EmbeddedChatProps {
  channel?: string;
  className?: string;
}

const RC_URL = process.env.NEXT_PUBLIC_ROCKETCHAT_URL || 'http://localhost:3200';

export default function EmbeddedChat({ channel, className = '' }: EmbeddedChatProps) {
  const [isExpanded, setIsExpanded] = useState(false);
  const [isLoaded, setIsLoaded] = useState(false);

  const chatUrl = channel
    ? `${RC_URL}/channel/${channel}?layout=embedded`
    : `${RC_URL}?layout=embedded`;

  return (
    <div className={`flex flex-col bg-background border border-border rounded-xl overflow-hidden ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-2.5 border-b border-border bg-muted/30">
        <div className="flex items-center gap-2">
          <MessageSquare size={16} className="text-primary" />
          <span className="text-sm font-semibold">
            {channel ? `#${channel}` : 'Messages'}
          </span>
        </div>
        <div className="flex items-center gap-1">
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="p-1.5 rounded-md hover:bg-muted text-muted-foreground hover:text-foreground transition-colors"
            title={isExpanded ? 'Collapse' : 'Expand'}
          >
            {isExpanded ? <Minimize2 size={14} /> : <Maximize2 size={14} />}
          </button>
          <a
            href={channel ? `${RC_URL}/channel/${channel}` : RC_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="p-1.5 rounded-md hover:bg-muted text-muted-foreground hover:text-foreground transition-colors"
            title="Open in new tab"
          >
            <ExternalLink size={14} />
          </a>
        </div>
      </div>

      {/* Chat iframe */}
      <div className={`relative transition-all duration-300 ${isExpanded ? 'h-[80vh]' : 'h-[500px]'}`}>
        {!isLoaded && (
          <div className="absolute inset-0 flex flex-col items-center justify-center bg-muted/20">
            <div className="animate-spin w-6 h-6 border-2 border-primary border-t-transparent rounded-full mb-3" />
            <p className="text-xs text-muted-foreground">Connecting to chat...</p>
          </div>
        )}
        <iframe
          src={chatUrl}
          className="w-full h-full border-0"
          onLoad={() => setIsLoaded(true)}
          allow="camera; microphone; fullscreen"
        />
      </div>
    </div>
  );
}
