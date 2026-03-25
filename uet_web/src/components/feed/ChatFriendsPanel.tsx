'use client';

import { useState } from 'react';
import { Search, Send, Users, MessageCircle, Phone, Video, ArrowLeft } from 'lucide-react';

const MOCK_DMS = [
  { id: 'dm1', name: 'Dr. Smith', online: true, last: 'ผลลัพธ์ออกมาดีมากครับ!', time: '2m', unread: 2 },
  { id: 'dm2', name: 'Sarah Chen', online: true, last: 'ช่วยดู paper ที่ส่งไปด้วยนะคะ', time: '15m', unread: 0 },
  { id: 'dm3', name: 'Prof. Kumar', online: false, last: 'See you at the seminar.', time: '1h', unread: 0 },
  { id: 'dm4', name: 'Alex Wong', online: false, last: 'ขอบคุณครับ!', time: '3h', unread: 0 },
  { id: 'dm5', name: 'Maria Garcia', online: true, last: 'The equations look stable now.', time: '5h', unread: 1 },
];

const MOCK_GROUPS = [
  { id: 'g1', name: 'UET Community', members: 142, last: 'New paper posted in #research', time: '5m', unread: 8 },
  { id: 'g2', name: 'Physics Lab', members: 24, last: 'Simulation ready for review', time: '20m', unread: 3 },
  { id: 'g3', name: 'Research Team', members: 8, last: 'Meeting tomorrow at 10am', time: '1h', unread: 0 },
  { id: 'g4', name: 'AI Alignment WG', members: 31, last: 'Draft v2 is ready to review', time: '2h', unread: 0 },
];

const MOCK_MSGS: Record<string, { role: 'me' | 'other'; text: string; time: string }[]> = {
  dm1: [
    { role: 'other', text: 'สวัสดีครับ เห็น paper ใหม่ของคุณแล้ว!', time: '10:02' },
    { role: 'me', text: 'ขอบคุณครับ ยังแก้ไขอยู่เลย', time: '10:05' },
    { role: 'other', text: 'ผลลัพธ์ออกมาดีมากครับ!', time: '10:07' },
  ],
  g1: [
    { role: 'other', text: '[Research Team] New paper posted in #research', time: '09:55' },
    { role: 'other', text: '[Dr. Smith] ใครสนใจร่วม project ใหม่บ้าง?', time: '10:01' },
    { role: 'me', text: 'สนใจครับ! ส่งรายละเอียดมาได้เลย', time: '10:03' },
  ],
};

type Tab = 'dm' | 'groups';
type Conv = { id: string; name: string; isGroup?: boolean };

export default function ChatFriendsPanel() {
  const [tab, setTab] = useState<Tab>('dm');
  const [search, setSearch] = useState('');
  const [activeConv, setActiveConv] = useState<Conv | null>(null);
  const [input, setInput] = useState('');
  const [localMsgs, setLocalMsgs] = useState(MOCK_MSGS);

  const dmFiltered = MOCK_DMS.filter(d => d.name.toLowerCase().includes(search.toLowerCase()));
  const grpFiltered = MOCK_GROUPS.filter(g => g.name.toLowerCase().includes(search.toLowerCase()));

  const messages = activeConv ? (localMsgs[activeConv.id] || []) : [];

  const sendMsg = () => {
    if (!input.trim() || !activeConv) return;
    const newMsg = { role: 'me' as const, text: input.trim(), time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) };
    setLocalMsgs(prev => ({ ...prev, [activeConv.id]: [...(prev[activeConv.id] || []), newMsg] }));
    setInput('');
  };

  if (activeConv) {
    return (
      <div className="flex flex-col h-full">
        {/* Conv header */}
        <div className="px-3 py-2.5 border-b border-border shrink-0 flex items-center gap-2">
          <button onClick={() => setActiveConv(null)} className="p-1 rounded hover:bg-muted text-muted-foreground">
            <ArrowLeft size={14} />
          </button>
          <div className="w-7 h-7 rounded-full bg-primary/10 flex items-center justify-center text-primary text-xs font-bold shrink-0">
            {activeConv.name[0]}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-xs font-semibold truncate">{activeConv.name}</p>
            <p className="text-[9px] text-muted-foreground">{activeConv.isGroup ? 'กลุ่ม' : 'ออนไลน์'}</p>
          </div>
          <div className="flex gap-0.5">
            <button className="p-1 rounded hover:bg-muted text-muted-foreground"><Phone size={13} /></button>
            <button className="p-1 rounded hover:bg-muted text-muted-foreground"><Video size={13} /></button>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto px-3 py-2 space-y-2">
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-muted-foreground/40 gap-2">
              <MessageCircle size={24} className="opacity-20" />
              <p className="text-[10px]">ยังไม่มีข้อความ</p>
            </div>
          ) : messages.map((m, i) => (
            <div key={i} className={`flex ${m.role === 'me' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-[80%] px-2.5 py-1.5 rounded-2xl text-[11px] leading-relaxed ${
                m.role === 'me'
                  ? 'bg-primary text-primary-foreground rounded-br-sm'
                  : 'bg-muted text-foreground rounded-bl-sm'
              }`}>
                {m.text}
                <span className="block text-[9px] opacity-60 mt-0.5 text-right">{m.time}</span>
              </div>
            </div>
          ))}
        </div>

        {/* Input */}
        <div className="px-2 py-2 border-t border-border shrink-0 flex items-center gap-1.5">
          <input
            type="text"
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && sendMsg()}
            placeholder="พิมพ์ข้อความ..."
            className="flex-1 text-xs bg-muted/40 border border-border rounded-full px-3 py-1.5 focus:outline-none focus:ring-1 focus:ring-primary"
          />
          <button
            onClick={sendMsg}
            disabled={!input.trim()}
            className="w-7 h-7 rounded-full bg-primary flex items-center justify-center text-primary-foreground disabled:opacity-40 transition-opacity"
          >
            <Send size={11} />
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="px-3 pt-3 pb-2 border-b border-border shrink-0">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-xs font-semibold">แชท</h3>
          <button className="p-1 rounded hover:bg-muted text-muted-foreground"><Video size={13} /></button>
        </div>

        {/* Search */}
        <div className="relative">
          <Search size={12} className="absolute left-2.5 top-1/2 -translate-y-1/2 text-muted-foreground" />
          <input
            type="text"
            value={search}
            onChange={e => setSearch(e.target.value)}
            placeholder="ค้นหา..."
            className="w-full pl-7 pr-3 py-1.5 rounded-full bg-muted/50 text-xs outline-none focus:bg-muted placeholder:text-muted-foreground"
          />
        </div>

        {/* Tabs */}
        <div className="flex gap-1 mt-2 bg-muted/40 rounded-lg p-0.5">
          <button
            onClick={() => setTab('dm')}
            className={`flex-1 flex items-center justify-center gap-1 text-[10px] py-1 rounded-md font-medium transition-all ${
              tab === 'dm' ? 'bg-background shadow-sm text-foreground' : 'text-muted-foreground'
            }`}
          >
            <MessageCircle size={10} /> DMs
          </button>
          <button
            onClick={() => setTab('groups')}
            className={`flex-1 flex items-center justify-center gap-1 text-[10px] py-1 rounded-md font-medium transition-all ${
              tab === 'groups' ? 'bg-background shadow-sm text-foreground' : 'text-muted-foreground'
            }`}
          >
            <Users size={10} /> กลุ่ม
          </button>
        </div>
      </div>

      {/* Conversation list */}
      <div className="flex-1 overflow-y-auto">
        {tab === 'dm' && (
          <div>
            {dmFiltered.map(d => (
              <button
                key={d.id}
                onClick={() => setActiveConv({ id: d.id, name: d.name })}
                className="w-full flex items-center gap-2.5 px-3 py-2.5 hover:bg-muted/40 transition-colors text-left"
              >
                <div className="relative shrink-0">
                  <div className="w-9 h-9 rounded-full bg-primary/10 flex items-center justify-center text-primary font-bold text-xs">
                    {d.name[0]}
                  </div>
                  {d.online && <span className="absolute bottom-0 right-0 w-2.5 h-2.5 rounded-full bg-green-500 border-2 border-background" />}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex justify-between items-baseline">
                    <span className="text-xs font-semibold truncate">{d.name}</span>
                    <span className="text-[9px] text-muted-foreground shrink-0 ml-1">{d.time}</span>
                  </div>
                  <p className="text-[10px] text-muted-foreground truncate">{d.last}</p>
                </div>
                {d.unread > 0 && (
                  <span className="shrink-0 w-4 h-4 rounded-full bg-primary text-primary-foreground text-[9px] flex items-center justify-center font-bold">
                    {d.unread}
                  </span>
                )}
              </button>
            ))}
          </div>
        )}

        {tab === 'groups' && (
          <div>
            {grpFiltered.map(g => (
              <button
                key={g.id}
                onClick={() => setActiveConv({ id: g.id, name: g.name, isGroup: true })}
                className="w-full flex items-center gap-2.5 px-3 py-2.5 hover:bg-muted/40 transition-colors text-left"
              >
                <div className="w-9 h-9 rounded-full bg-emerald-500/10 flex items-center justify-center shrink-0">
                  <Users size={14} className="text-emerald-600" />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex justify-between items-baseline">
                    <span className="text-xs font-semibold truncate">{g.name}</span>
                    <span className="text-[9px] text-muted-foreground shrink-0 ml-1">{g.time}</span>
                  </div>
                  <p className="text-[10px] text-muted-foreground truncate">{g.last}</p>
                  <p className="text-[9px] text-muted-foreground/60">{g.members} members</p>
                </div>
                {g.unread > 0 && (
                  <span className="shrink-0 w-4 h-4 rounded-full bg-primary text-primary-foreground text-[9px] flex items-center justify-center font-bold">
                    {g.unread}
                  </span>
                )}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
