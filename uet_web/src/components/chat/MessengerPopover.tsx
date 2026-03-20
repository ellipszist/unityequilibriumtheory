'use client';

import { useState, useRef, useEffect } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { MessageCircle, Search, Edit, X, Minimize2 } from 'lucide-react';

interface ChatContact {
  id: string;
  name: string;
  avatar?: string;
  lastMessage?: string;
  time?: string;
  unread?: boolean;
  online?: boolean;
}

const MOCK_CONTACTS: ChatContact[] = [
  { id: '1', name: 'Research Team', lastMessage: 'ส่งผลวิเคราะห์มาแล้ว', time: '4 ชม.', unread: true, online: true },
  { id: '2', name: 'Dr. Smith', lastMessage: 'The quantum results look promising', time: '23 ชม.', online: true },
  { id: '3', name: 'Physics Lab Group', lastMessage: 'Meeting at 2pm tomorrow', time: '2 วัน', online: false },
  { id: '4', name: 'UET Community', lastMessage: 'New paper published!', time: '1 สัปดาห์', online: false },
];

interface MessengerPopoverProps {
  onOpenChat?: (contact: ChatContact) => void;
}

export default function MessengerPopover({ onOpenChat }: MessengerPopoverProps) {
  const params = useParams();
  const locale = (params?.locale as string) || 'en';
  const [open, setOpen] = useState(false);
  const [search, setSearch] = useState('');
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false);
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const filtered = MOCK_CONTACTS.filter(c =>
    c.name.toLowerCase().includes(search.toLowerCase())
  );

  const unreadCount = MOCK_CONTACTS.filter(c => c.unread).length;

  return (
    <div ref={ref} className="relative">
      <button
        onClick={() => setOpen(!open)}
        className="w-9 h-9 rounded-full bg-black/5 dark:bg-white/10 hover:bg-black/10 dark:hover:bg-white/20 flex items-center justify-center transition-colors relative"
        title="แชท"
      >
        <MessageCircle size={17} className="text-black/70 dark:text-white/70" />
        {unreadCount > 0 && (
          <span className="absolute -top-0.5 -right-0.5 w-4 h-4 rounded-full bg-red-500 text-white text-[9px] font-bold flex items-center justify-center">
            {unreadCount}
          </span>
        )}
      </button>

      {open && (
        <div className="absolute right-0 top-full mt-2 w-80 rounded-2xl border border-border bg-card shadow-2xl z-50 overflow-hidden">
          {/* Header */}
          <div className="flex items-center justify-between px-4 py-3">
            <h3 className="text-lg font-bold">แชท</h3>
            <div className="flex items-center gap-1">
              <button className="p-1.5 rounded-full hover:bg-muted transition-colors text-muted-foreground">
                <Edit size={16} />
              </button>
            </div>
          </div>

          {/* Search */}
          <div className="px-3 pb-2">
            <div className="relative">
              <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
              <input
                type="text"
                value={search}
                onChange={e => setSearch(e.target.value)}
                placeholder="ค้นหา Messenger"
                className="w-full pl-9 pr-3 py-2 rounded-full bg-muted/50 border-0 text-xs outline-none focus:bg-muted placeholder:text-muted-foreground"
              />
            </div>
          </div>

          {/* Tabs */}
          <div className="flex gap-1 px-3 pb-2">
            <button className="px-3 py-1 rounded-full bg-primary/10 text-primary text-xs font-medium">ทั้งหมด</button>
            <button className="px-3 py-1 rounded-full text-muted-foreground text-xs font-medium hover:bg-muted">ยังไม่ได้อ่าน</button>
            <button className="px-3 py-1 rounded-full text-muted-foreground text-xs font-medium hover:bg-muted">กลุ่ม</button>
          </div>

          {/* Contact list */}
          <div className="max-h-80 overflow-y-auto">
            {filtered.map(contact => (
              <button
                key={contact.id}
                onClick={() => {
                  onOpenChat?.(contact);
                  setOpen(false);
                }}
                className="w-full flex items-center gap-3 px-4 py-2.5 hover:bg-muted/50 transition-colors"
              >
                <div className="relative shrink-0">
                  {contact.avatar ? (
                    <img src={contact.avatar} className="w-10 h-10 rounded-full object-cover" />
                  ) : (
                    <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center text-primary font-bold text-sm">
                      {contact.name[0]}
                    </div>
                  )}
                  {contact.online && (
                    <span className="absolute bottom-0 right-0 w-3 h-3 rounded-full bg-green-500 border-2 border-card" />
                  )}
                </div>
                <div className="flex-1 min-w-0 text-left">
                  <p className={`text-sm truncate ${contact.unread ? 'font-bold' : 'font-medium'}`}>
                    {contact.name}
                  </p>
                  <p className={`text-xs truncate ${contact.unread ? 'text-foreground font-medium' : 'text-muted-foreground'}`}>
                    {contact.lastMessage} · {contact.time}
                  </p>
                </div>
                {contact.unread && (
                  <span className="w-2.5 h-2.5 rounded-full bg-primary shrink-0" />
                )}
              </button>
            ))}
          </div>

          {/* Footer */}
          <div className="border-t border-border px-4 py-2.5">
            <Link
              href={`/${locale}/messages`}
              onClick={() => setOpen(false)}
              className="text-xs text-primary font-semibold hover:underline"
            >
              ดูทั้งหมดใน Messenger
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}
