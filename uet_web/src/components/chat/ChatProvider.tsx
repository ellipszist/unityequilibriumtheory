'use client';

import { createContext, useContext, useState, ReactNode } from 'react';
import FloatingChat from './FloatingChat';

interface ChatContact {
  id: string;
  name: string;
  avatar?: string;
  online?: boolean;
}

interface ChatContextType {
  openChat: (contact: ChatContact) => void;
  closeChat: (id: string) => void;
}

const ChatContext = createContext<ChatContextType>({
  openChat: () => {},
  closeChat: () => {},
});

export function useChatContext() {
  return useContext(ChatContext);
}

export function ChatProvider({ children }: { children: ReactNode }) {
  const [openChats, setOpenChats] = useState<ChatContact[]>([]);
  const [minimized, setMinimized] = useState<Set<string>>(new Set());

  function openChat(contact: ChatContact) {
    setOpenChats(prev => {
      if (prev.find(c => c.id === contact.id)) {
        // Already open, just un-minimize
        setMinimized(m => { const n = new Set(m); n.delete(contact.id); return n; });
        return prev;
      }
      // Max 3 open chats
      const next = [...prev, contact];
      if (next.length > 3) next.shift();
      return next;
    });
  }

  function closeChat(id: string) {
    setOpenChats(prev => prev.filter(c => c.id !== id));
    setMinimized(m => { const n = new Set(m); n.delete(id); return n; });
  }

  function minimizeChat(id: string) {
    setMinimized(m => {
      const n = new Set(m);
      if (n.has(id)) n.delete(id); else n.add(id);
      return n;
    });
  }

  return (
    <ChatContext.Provider value={{ openChat, closeChat }}>
      {children}

      {/* Floating chats — bottom right, stacked horizontally like Facebook */}
      <div className="fixed bottom-0 right-4 z-50 flex items-end gap-2">
        {openChats.map(contact => (
          <div key={contact.id}>
            {minimized.has(contact.id) ? (
              /* Minimized bubble */
              <button
                onClick={() => minimizeChat(contact.id)}
                className="relative w-12 h-12 rounded-full bg-primary/10 border-2 border-primary flex items-center justify-center text-primary font-bold text-sm mb-2 hover:scale-110 transition-transform shadow-lg"
                title={contact.name}
              >
                {contact.avatar ? (
                  <img src={contact.avatar} className="w-full h-full rounded-full object-cover" />
                ) : (
                  contact.name[0]?.toUpperCase()
                )}
                {contact.online && (
                  <span className="absolute bottom-0 right-0 w-3 h-3 rounded-full bg-green-500 border-2 border-card" />
                )}
              </button>
            ) : (
              <FloatingChat
                contact={contact}
                onClose={() => closeChat(contact.id)}
                onMinimize={() => minimizeChat(contact.id)}
              />
            )}
          </div>
        ))}
      </div>
    </ChatContext.Provider>
  );
}
