'use client';

import { useState, useEffect, useCallback } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import {
  MessageSquare, Plus, X, Bot, Clock, Sparkles,
  ChevronRight, Search, Loader2,
} from 'lucide-react';

interface ChatSession {
  id: string;
  title: string;
  model: string;
  messageCount: number;
  projectScope: string | null;
  createdAt: string;
  updatedAt: string;
}

interface ChatHistorySidebarProps {
  open: boolean;
  onClose: () => void;
}

const MODEL_BADGE: Record<string, { label: string; color: string }> = {
  'uet-agent':      { label: 'UET', color: 'bg-primary/15 text-primary' },
  'uet-agent-fast': { label: 'Fast', color: 'bg-emerald-500/15 text-emerald-600' },
  'glm-4.7-flash':  { label: 'GLM', color: 'bg-blue-500/15 text-blue-600' },
  'qwen-2.5-7b':    { label: 'Qwen', color: 'bg-purple-500/15 text-purple-600' },
};

function groupByDate(sessions: ChatSession[]) {
  const now = new Date();
  const today = now.toDateString();
  const yesterday = new Date(now.getTime() - 86400000).toDateString();
  const last7 = new Date(now.getTime() - 7 * 86400000);

  const groups: Record<string, ChatSession[]> = {
    'วันนี้': [],
    'เมื่อวาน': [],
    '7 วันที่ผ่านมา': [],
    'เก่ากว่านั้น': [],
  };

  for (const s of sessions) {
    const d = new Date(s.updatedAt);
    if (d.toDateString() === today) groups['วันนี้'].push(s);
    else if (d.toDateString() === yesterday) groups['เมื่อวาน'].push(s);
    else if (d >= last7) groups['7 วันที่ผ่านมา'].push(s);
    else groups['เก่ากว่านั้น'].push(s);
  }

  return Object.entries(groups).filter(([, items]) => items.length > 0);
}

export default function ChatHistorySidebar({ open, onClose }: ChatHistorySidebarProps) {
  const params = useParams();
  const locale = (params?.locale as string) || 'en';
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState('');

  const fetchSessions = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/chat-sessions?userId=demo-user');
      if (res.ok) setSessions(await res.json());
    } catch { /* offline */ } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (open) fetchSessions();
  }, [open, fetchSessions]);

  const filtered = search.trim()
    ? sessions.filter(s => s.title.toLowerCase().includes(search.toLowerCase()))
    : sessions;

  const grouped = groupByDate(filtered);

  return (
    <>
      {/* Backdrop (mobile) */}
      {open && (
        <div
          className="fixed inset-0 z-30 bg-black/20 md:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`fixed top-14 right-0 bottom-0 z-40 w-72 flex flex-col bg-card border-l border-border shadow-2xl transition-transform duration-200 ease-in-out ${
          open ? 'translate-x-0' : 'translate-x-full'
        }`}
      >
        {/* Header */}
        <div className="shrink-0 flex items-center justify-between px-4 py-3 border-b border-border bg-muted/10">
          <div className="flex items-center gap-2">
            <MessageSquare size={15} className="text-primary" />
            <span className="text-sm font-semibold">Chat History</span>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg hover:bg-muted text-muted-foreground hover:text-foreground transition-colors"
          >
            <X size={14} />
          </button>
        </div>

        {/* New Chat button */}
        <div className="shrink-0 px-3 pt-3 pb-2">
          <Link
            href={`/${locale}/workchat`}
            onClick={onClose}
            className="flex items-center justify-center gap-2 w-full px-3 py-2 rounded-xl bg-primary text-primary-foreground text-xs font-semibold hover:bg-primary/90 transition-colors"
          >
            <Plus size={14} />
            New Chat
          </Link>
        </div>

        {/* Search */}
        <div className="shrink-0 px-3 pb-2">
          <div className="relative">
            <Search size={11} className="absolute left-2.5 top-1/2 -translate-y-1/2 text-muted-foreground" />
            <input
              type="text"
              value={search}
              onChange={e => setSearch(e.target.value)}
              placeholder="ค้นหาแชท..."
              className="w-full pl-7 pr-3 py-1.5 rounded-lg bg-muted/50 text-xs outline-none focus:bg-muted placeholder:text-muted-foreground transition-colors"
            />
          </div>
        </div>

        {/* Session list */}
        <div className="flex-1 overflow-y-auto px-2 pb-4">
          {loading ? (
            <div className="flex items-center justify-center py-12 gap-2 text-muted-foreground">
              <Loader2 size={14} className="animate-spin" />
              <span className="text-xs">กำลังโหลด...</span>
            </div>
          ) : sessions.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-16 gap-3 text-center text-muted-foreground">
              <div className="w-12 h-12 rounded-full bg-muted/40 flex items-center justify-center">
                <Bot size={20} className="opacity-30" />
              </div>
              <p className="text-xs">ยังไม่มีประวัติแชท</p>
              <p className="text-[10px] opacity-60">เริ่ม New Chat เพื่อพูดคุยกับ UET Agent</p>
            </div>
          ) : grouped.length === 0 ? (
            <p className="text-xs text-center text-muted-foreground py-8">ไม่พบแชทที่ตรงกัน</p>
          ) : (
            grouped.map(([label, items]) => (
              <div key={label} className="mt-3">
                <p className="text-[9px] font-semibold uppercase tracking-wider text-muted-foreground px-2 mb-1">{label}</p>
                <div className="space-y-0.5">
                  {items.map(s => {
                    const badge = MODEL_BADGE[s.model] ?? { label: s.model, color: 'bg-muted text-muted-foreground' };
                    return (
                      <Link
                        key={s.id}
                        href={`/${locale}/workchat?session=${s.id}`}
                        onClick={onClose}
                        className="group flex items-start gap-2.5 px-2 py-2 rounded-xl hover:bg-muted/50 transition-colors"
                      >
                        <div className="shrink-0 w-7 h-7 rounded-full bg-primary/10 flex items-center justify-center mt-0.5">
                          <Sparkles size={12} className="text-primary" />
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="text-xs font-medium truncate leading-tight">{s.title}</p>
                          <div className="flex items-center gap-1.5 mt-0.5">
                            <span className={`text-[9px] px-1.5 py-0.5 rounded-full font-medium ${badge.color}`}>
                              {badge.label}
                            </span>
                            {s.messageCount > 0 && (
                              <span className="text-[9px] text-muted-foreground">{s.messageCount} msgs</span>
                            )}
                          </div>
                        </div>
                        <ChevronRight size={11} className="shrink-0 text-muted-foreground/40 group-hover:text-muted-foreground mt-1 transition-colors" />
                      </Link>
                    );
                  })}
                </div>
              </div>
            ))
          )}
        </div>

        {/* Footer */}
        <div className="shrink-0 px-4 py-2.5 border-t border-border bg-muted/5">
          <div className="flex items-center gap-1.5 text-[10px] text-muted-foreground">
            <Clock size={10} />
            <span>บันทึกทุก session อัตโนมัติ</span>
          </div>
        </div>
      </aside>
    </>
  );
}
