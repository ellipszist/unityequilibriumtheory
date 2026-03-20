'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { Hash, FileText, LayoutGrid, Users, Settings, ArrowLeft, Plus, Phone, Globe, Lock } from 'lucide-react';
import { LocaleSwitcher } from '@/components/locale-switcher';
import { ThemeToggle } from '@/components/theme-toggle';
import EmbeddedChat from '@/components/chat/EmbeddedChat';
import VideoCall from '@/components/video/VideoCall';

type Tab = 'channels' | 'documents' | 'tasks' | 'members' | 'settings';

interface WorkspaceDetail {
  id: string;
  name: string;
  description: string | null;
  avatarUrl: string | null;
  isPublic: boolean;
  owner: { id: string; email: string; displayName?: string; avatarUrl?: string };
  members: {
    id: string;
    role: string;
    user: { id: string; email: string; displayName?: string; avatarUrl?: string };
  }[];
  documents: {
    id: string;
    title: string;
    yjsDocId: string;
    updatedAt: string;
    createdBy: { id: string; displayName?: string };
  }[];
  projects: {
    id: string;
    name: string;
    status: string;
    tasks: { id: string; title: string; status: string; bountyAmount: number }[];
    _count: { tasks: number };
  }[];
  _count: { members: number; documents: number; projects: number };
}

const WORKSPACE_CHANNELS = [
  { name: 'general', icon: Hash },
  { name: 'research', icon: Hash },
  { name: 'announcements', icon: Hash },
];

export default function WorkspaceDetailPage() {
  const params = useParams();
  const locale = (params?.locale as string) || 'en';
  const wsId = params?.id as string;

  const [ws, setWs] = useState<WorkspaceDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<Tab>('channels');
  const [activeChannel, setActiveChannel] = useState<string | null>(null);
  const [activeVoice, setActiveVoice] = useState<string | null>(null);
  const [currentUserName, setCurrentUserName] = useState('User');

  useEffect(() => {
    try {
      const stored = localStorage.getItem('user');
      if (stored) {
        const u = JSON.parse(stored);
        setCurrentUserName(u.display_name || u.email?.split('@')[0] || 'User');
      }
    } catch {}
  }, []);

  useEffect(() => {
    if (!wsId) return;
    fetch(`/api/workspaces/${wsId}`)
      .then(r => r.ok ? r.json() : null)
      .then(data => { if (data) setWs(data); })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [wsId]);

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="animate-spin w-8 h-8 border-2 border-primary border-t-transparent rounded-full" />
      </div>
    );
  }

  if (!ws) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center text-muted-foreground">
        Workspace not found
      </div>
    );
  }

  const tabs: { key: Tab; label: string; icon: typeof Hash; count?: number }[] = [
    { key: 'channels', label: 'Channels', icon: Hash },
    { key: 'documents', label: 'Docs', icon: FileText, count: ws._count.documents },
    { key: 'tasks', label: 'Tasks', icon: LayoutGrid, count: ws.projects.reduce((s, p) => s + p._count.tasks, 0) },
    { key: 'members', label: 'Members', icon: Users, count: ws._count.members },
    { key: 'settings', label: 'Settings', icon: Settings },
  ];

  const taskColumns = ['TODO', 'IN_PROGRESS', 'IN_REVIEW', 'DONE'];

  return (
    <div className="flex flex-col h-screen bg-background text-foreground text-sm">
      {/* Header */}
      <header className="shrink-0 flex items-center justify-between h-14 px-6 border-b border-border bg-background/80 backdrop-blur-md">
        <div className="flex items-center gap-4">
          <Link href={`/${locale}/workspaces`} className="p-1.5 rounded-lg hover:bg-muted transition-colors">
            <ArrowLeft size={18} />
          </Link>
          <div className="flex items-center gap-2.5">
            {ws.avatarUrl ? (
              <img src={ws.avatarUrl} alt={ws.name} className="w-7 h-7 rounded-lg object-cover" />
            ) : (
              <div className="w-7 h-7 rounded-lg bg-primary/10 flex items-center justify-center text-primary font-bold text-xs">
                {ws.name[0]?.toUpperCase()}
              </div>
            )}
            <h1 className="font-semibold">{ws.name}</h1>
            {ws.isPublic ? <Globe size={12} className="text-muted-foreground" /> : <Lock size={12} className="text-muted-foreground" />}
          </div>
        </div>
        <div className="flex items-center gap-3">
          <LocaleSwitcher />
          <ThemeToggle />
        </div>
      </header>

      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar */}
        <aside className="w-56 shrink-0 border-r border-border bg-muted/20 flex flex-col">
          {/* Tabs */}
          <div className="p-3 space-y-0.5">
            {tabs.map(tab => (
              <button
                key={tab.key}
                onClick={() => { setActiveTab(tab.key); setActiveChannel(null); }}
                className={`w-full flex items-center justify-between px-3 py-2 rounded-lg text-sm transition-colors ${
                  activeTab === tab.key
                    ? 'bg-primary/10 text-primary font-medium'
                    : 'text-muted-foreground hover:text-foreground hover:bg-muted'
                }`}
              >
                <span className="flex items-center gap-2"><tab.icon size={14} />{tab.label}</span>
                {tab.count !== undefined && (
                  <span className="text-[10px] bg-muted px-1.5 py-0.5 rounded-full">{tab.count}</span>
                )}
              </button>
            ))}
          </div>

          {/* Channel list (when channels tab active) */}
          {activeTab === 'channels' && (
            <div className="px-3 mt-2 border-t border-border pt-3">
              <p className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground mb-2 px-3">Text Channels</p>
              {WORKSPACE_CHANNELS.map(ch => (
                <button
                  key={ch.name}
                  onClick={() => setActiveChannel(ch.name)}
                  className={`w-full flex items-center gap-2 px-3 py-1.5 rounded-md text-xs transition-colors ${
                    activeChannel === ch.name ? 'bg-primary/10 text-primary' : 'text-muted-foreground hover:text-foreground hover:bg-muted'
                  }`}
                >
                  <ch.icon size={13} /> {ch.name}
                </button>
              ))}
              <p className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground mt-4 mb-2 px-3">Voice Channels</p>
              <button
                onClick={() => { setActiveVoice(activeVoice === 'general' ? null : 'general'); setActiveChannel(null); }}
                className={`w-full flex items-center gap-2 px-3 py-1.5 rounded-md text-xs transition-colors ${
                  activeVoice === 'general' ? 'bg-green-500/10 text-green-600' : 'text-muted-foreground hover:text-foreground hover:bg-muted'
                }`}
              >
                <Phone size={13} /> General Voice
                {activeVoice === 'general' && <span className="ml-auto w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />}
              </button>
            </div>
          )}
        </aside>

        {/* Main content */}
        <main className="flex-1 flex flex-col overflow-hidden">
          {/* Channels tab */}
          {activeTab === 'channels' && (
            activeVoice ? (
              <VideoCall
                roomName={`ws-${wsId}-voice-${activeVoice}`}
                participantName={currentUserName}
                className="flex-1"
              />
            ) : activeChannel ? (
              <EmbeddedChat channel={`ws-${wsId}-${activeChannel}`} className="flex-1 rounded-none border-0" />
            ) : (
              <div className="flex-1 flex items-center justify-center text-muted-foreground">
                <div className="text-center">
                  <Hash size={40} className="mx-auto mb-3 opacity-30" />
                  <p className="font-medium">Select a channel</p>
                  <p className="text-xs mt-1">Choose a text or voice channel from the sidebar</p>
                </div>
              </div>
            )
          )}

          {/* Documents tab */}
          {activeTab === 'documents' && (
            <div className="flex-1 overflow-auto p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-lg font-semibold">Documents</h2>
                <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-primary text-primary-foreground text-xs font-medium hover:bg-primary/90">
                  <Plus size={13} /> New Document
                </button>
              </div>
              {ws.documents.length === 0 ? (
                <p className="text-center text-muted-foreground py-12">No documents yet. Create one to start collaborating!</p>
              ) : (
                <div className="space-y-2">
                  {ws.documents.map(doc => (
                    <Link
                      key={doc.id}
                      href={`/${locale}/workspaces/${wsId}/docs/${doc.id}`}
                      className="flex items-center gap-3 p-4 rounded-xl border border-border hover:border-primary/30 transition-colors"
                    >
                      <FileText size={18} className="text-primary shrink-0" />
                      <div className="flex-1 min-w-0">
                        <h3 className="font-medium truncate">{doc.title}</h3>
                        <p className="text-xs text-muted-foreground">
                          Updated {new Date(doc.updatedAt).toLocaleDateString()} · by {doc.createdBy.displayName || 'Unknown'}
                        </p>
                      </div>
                    </Link>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Tasks tab (Kanban) */}
          {activeTab === 'tasks' && (
            <div className="flex-1 overflow-auto p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-lg font-semibold">Task Board</h2>
                <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-primary text-primary-foreground text-xs font-medium hover:bg-primary/90">
                  <Plus size={13} /> New Task
                </button>
              </div>
              <div className="grid grid-cols-4 gap-4 min-w-[800px]">
                {taskColumns.map(col => {
                  const tasks = ws.projects.flatMap(p => p.tasks).filter(t => t.status === col);
                  return (
                    <div key={col} className="bg-muted/30 rounded-xl p-3">
                      <div className="flex items-center justify-between mb-3 px-1">
                        <h3 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                          {col.replace('_', ' ')}
                        </h3>
                        <span className="text-[10px] bg-muted px-1.5 py-0.5 rounded-full">{tasks.length}</span>
                      </div>
                      <div className="space-y-2">
                        {tasks.map(task => (
                          <div key={task.id} className="p-3 rounded-lg bg-card border border-border hover:border-primary/30 transition-colors">
                            <p className="text-sm font-medium mb-1">{task.title}</p>
                            {task.bountyAmount > 0 && (
                              <span className="text-[10px] text-primary font-medium">{task.bountyAmount} UET</span>
                            )}
                          </div>
                        ))}
                        {tasks.length === 0 && (
                          <p className="text-center text-xs text-muted-foreground py-4 opacity-50">No tasks</p>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* Members tab */}
          {activeTab === 'members' && (
            <div className="flex-1 overflow-auto p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-lg font-semibold">Members ({ws._count.members})</h2>
                <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-border text-xs font-medium hover:bg-muted">
                  <Plus size={13} /> Invite
                </button>
              </div>
              <div className="space-y-2">
                {ws.members.map(m => {
                  const name = m.user.displayName || m.user.email.split('@')[0];
                  return (
                    <div key={m.id} className="flex items-center gap-3 p-3 rounded-xl border border-border">
                      {m.user.avatarUrl ? (
                        <img src={m.user.avatarUrl} className="w-9 h-9 rounded-full object-cover" />
                      ) : (
                        <div className="w-9 h-9 rounded-full bg-primary/10 flex items-center justify-center text-primary text-sm font-bold">
                          {name[0]?.toUpperCase()}
                        </div>
                      )}
                      <div className="flex-1">
                        <p className="font-medium text-sm">{name}</p>
                        <p className="text-xs text-muted-foreground">{m.user.email}</p>
                      </div>
                      <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${
                        m.role === 'OWNER' ? 'bg-primary/10 text-primary' :
                        m.role === 'ADMIN' ? 'bg-amber-500/10 text-amber-600' :
                        'bg-muted text-muted-foreground'
                      }`}>
                        {m.role}
                      </span>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* Settings tab */}
          {activeTab === 'settings' && (
            <div className="flex-1 overflow-auto p-6">
              <h2 className="text-lg font-semibold mb-6">Workspace Settings</h2>
              <div className="max-w-lg space-y-6">
                <div className="p-5 rounded-xl border border-border">
                  <h3 className="font-medium mb-3">General</h3>
                  <div className="space-y-3">
                    <div>
                      <label className="block text-xs text-muted-foreground mb-1">Name</label>
                      <input defaultValue={ws.name} className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm" />
                    </div>
                    <div>
                      <label className="block text-xs text-muted-foreground mb-1">Description</label>
                      <textarea defaultValue={ws.description || ''} rows={3} className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm resize-none" />
                    </div>
                  </div>
                </div>
                <div className="p-5 rounded-xl border border-destructive/30 bg-destructive/5">
                  <h3 className="font-medium text-destructive mb-2">Danger Zone</h3>
                  <p className="text-xs text-muted-foreground mb-3">Permanently delete this workspace and all its data.</p>
                  <button className="px-4 py-1.5 rounded-lg border border-destructive text-destructive text-xs font-medium hover:bg-destructive hover:text-destructive-foreground transition-colors">
                    Delete Workspace
                  </button>
                </div>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
