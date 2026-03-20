'use client';

import { useState } from 'react';
import { X, Minus, Send, Phone, Video, MoreHorizontal } from 'lucide-react';

interface FloatingChatProps {
  contact: {
    id: string;
    name: string;
    avatar?: string;
    online?: boolean;
  };
  onClose: () => void;
  onMinimize: () => void;
}

export default function FloatingChat({ contact, onClose, onMinimize }: FloatingChatProps) {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState<{ id: string; text: string; from: 'me' | 'them'; time: string }[]>([
    { id: '1', text: 'สวัสดีครับ 👋', from: 'them', time: '14:01' },
    { id: '2', text: 'สวัสดี! มีอะไรให้ช่วยไหม?', from: 'me', time: '14:02' },
  ]);

  function handleSend() {
    if (!message.trim()) return;
    setMessages(prev => [...prev, {
      id: Date.now().toString(),
      text: message.trim(),
      from: 'me',
      time: new Date().toLocaleTimeString('th-TH', { hour: '2-digit', minute: '2-digit' }),
    }]);
    setMessage('');
  }

  const initials = contact.name[0]?.toUpperCase() || 'U';

  return (
    <div className="w-80 h-[420px] rounded-t-xl border border-border bg-card shadow-2xl flex flex-col overflow-hidden">
      {/* Header */}
      <div className="flex items-center gap-2.5 px-3 py-2 bg-card border-b border-border shrink-0">
        <div className="relative">
          {contact.avatar ? (
            <img src={contact.avatar} className="w-8 h-8 rounded-full object-cover" />
          ) : (
            <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary font-bold text-xs">
              {initials}
            </div>
          )}
          {contact.online && (
            <span className="absolute bottom-0 right-0 w-2.5 h-2.5 rounded-full bg-green-500 border-2 border-card" />
          )}
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-sm font-semibold truncate">{contact.name}</p>
          <p className="text-[10px] text-muted-foreground">{contact.online ? 'ออนไลน์' : 'ออฟไลน์'}</p>
        </div>
        <div className="flex items-center gap-0.5">
          <button className="p-1.5 rounded-full hover:bg-muted text-muted-foreground transition-colors">
            <Phone size={14} />
          </button>
          <button className="p-1.5 rounded-full hover:bg-muted text-muted-foreground transition-colors">
            <Video size={14} />
          </button>
          <button onClick={onMinimize} className="p-1.5 rounded-full hover:bg-muted text-muted-foreground transition-colors">
            <Minus size={14} />
          </button>
          <button onClick={onClose} className="p-1.5 rounded-full hover:bg-muted text-muted-foreground hover:text-destructive transition-colors">
            <X size={14} />
          </button>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-3 space-y-2">
        {messages.map(msg => (
          <div key={msg.id} className={`flex ${msg.from === 'me' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[75%] px-3 py-2 rounded-2xl text-sm ${
              msg.from === 'me'
                ? 'bg-primary text-primary-foreground rounded-br-md'
                : 'bg-muted text-foreground rounded-bl-md'
            }`}>
              <p>{msg.text}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Input */}
      <div className="flex items-center gap-2 px-3 py-2 border-t border-border shrink-0">
        <input
          type="text"
          value={message}
          onChange={e => setMessage(e.target.value)}
          onKeyDown={e => { if (e.key === 'Enter') handleSend(); }}
          placeholder="Aa"
          className="flex-1 px-3 py-2 rounded-full bg-muted/50 text-sm outline-none placeholder:text-muted-foreground"
        />
        <button
          onClick={handleSend}
          disabled={!message.trim()}
          className="p-2 rounded-full text-primary hover:bg-primary/10 disabled:opacity-30 transition-colors"
        >
          <Send size={16} />
        </button>
      </div>
    </div>
  );
}
