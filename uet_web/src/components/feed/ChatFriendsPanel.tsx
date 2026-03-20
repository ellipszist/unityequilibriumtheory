'use client';

import { useState } from 'react';
import { Search, Phone, Video } from 'lucide-react';
import { useChatContext } from '@/components/chat/ChatProvider';

const MOCK_FRIENDS = [
  { id: '1', name: 'Dr. Smith', online: true },
  { id: '2', name: 'Research Team', online: true },
  { id: '3', name: 'Physics Lab', online: true },
  { id: '4', name: 'Sarah Chen', online: false },
  { id: '5', name: 'Prof. Kumar', online: false },
  { id: '6', name: 'UET Community', online: true },
  { id: '7', name: 'Alex Wong', online: false },
  { id: '8', name: 'Maria Garcia', online: true },
];

export default function ChatFriendsPanel() {
  const [search, setSearch] = useState('');
  const { openChat } = useChatContext();

  const filtered = MOCK_FRIENDS.filter(f =>
    f.name.toLowerCase().includes(search.toLowerCase())
  );
  const onlineFriends = filtered.filter(f => f.online);
  const offlineFriends = filtered.filter(f => !f.online);

  return (
    <div className="p-3">
      <div className="flex items-center justify-between mb-3 px-1">
        <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Contacts</h3>
        <div className="flex gap-1">
          <button className="p-1 rounded hover:bg-muted text-muted-foreground"><Video size={14} /></button>
          <button className="p-1 rounded hover:bg-muted text-muted-foreground"><Search size={14} /></button>
        </div>
      </div>

      <div className="relative mb-3">
        <Search size={13} className="absolute left-2.5 top-1/2 -translate-y-1/2 text-muted-foreground" />
        <input
          type="text"
          value={search}
          onChange={e => setSearch(e.target.value)}
          placeholder="Search friends..."
          className="w-full pl-8 pr-3 py-1.5 rounded-full bg-muted/50 text-xs outline-none focus:bg-muted placeholder:text-muted-foreground"
        />
      </div>

      {onlineFriends.length > 0 && (
        <div className="mb-4">
          <p className="text-[10px] text-muted-foreground font-medium px-1 mb-1">Online — {onlineFriends.length}</p>
          {onlineFriends.map(f => (
            <button
              key={f.id}
              onClick={() => openChat({ id: f.id, name: f.name, online: true })}
              className="w-full flex items-center gap-2.5 px-2 py-1.5 rounded-lg hover:bg-muted/50 transition-colors"
            >
              <div className="relative">
                <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary font-bold text-xs">
                  {f.name[0]}
                </div>
                <span className="absolute bottom-0 right-0 w-2.5 h-2.5 rounded-full bg-green-500 border-2 border-card" />
              </div>
              <span className="text-sm truncate">{f.name}</span>
            </button>
          ))}
        </div>
      )}

      {offlineFriends.length > 0 && (
        <div>
          <p className="text-[10px] text-muted-foreground font-medium px-1 mb-1">Offline — {offlineFriends.length}</p>
          {offlineFriends.map(f => (
            <button
              key={f.id}
              onClick={() => openChat({ id: f.id, name: f.name, online: false })}
              className="w-full flex items-center gap-2.5 px-2 py-1.5 rounded-lg hover:bg-muted/50 transition-colors"
            >
              <div className="w-8 h-8 rounded-full bg-muted flex items-center justify-center text-muted-foreground font-bold text-xs">
                {f.name[0]}
              </div>
              <span className="text-sm text-muted-foreground truncate">{f.name}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
