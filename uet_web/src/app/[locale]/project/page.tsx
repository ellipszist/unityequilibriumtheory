'use client';

import { useState } from 'react';
import AppShell from '@/components/layout/AppShell';
import SidebarLayout from '@/components/layout/SidebarLayout';
import EmbeddedChat from '@/components/chat/EmbeddedChat';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { FolderGit2, Hash, Phone, Video, FileText, Plus, Wallet, Users, Bot } from 'lucide-react';

const MOCK_PROJECTS = [
  { id: 'proj-1', name: 'UET Core Research', topics: ['general', 'equations', 'proofs'], wallet: 1200 },
  { id: 'proj-2', name: 'AI Alignment Study', topics: ['general', 'papers', 'discussion'], wallet: 450 },
];

export default function ProjectPage() {
  const params = useParams();
  const locale = (params?.locale as string) || 'en';
  const [activeProject, setActiveProject] = useState(MOCK_PROJECTS[0]);
  const [activeTopic, setActiveTopic] = useState('general');

  const sidebar = (
    <div className="flex flex-col h-full">
      {/* Project selector */}
      <div className="p-3 border-b border-border">
        <div className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider mb-2 px-1">Projects</div>
        {MOCK_PROJECTS.map(p => (
          <button
            key={p.id}
            onClick={() => { setActiveProject(p); setActiveTopic('general'); }}
            className={`w-full flex items-center gap-2 px-2 py-1.5 text-xs rounded-md text-left transition-colors mb-0.5 ${activeProject.id === p.id ? 'bg-primary/10 text-primary' : 'hover:bg-accent text-foreground'}`}
          >
            <FolderGit2 size={13} className="shrink-0" />
            <span className="truncate">{p.name}</span>
          </button>
        ))}
        <Link
          href={`/${locale}/project/new`}
          className="w-full flex items-center gap-2 px-2 py-1.5 text-xs rounded-md text-muted-foreground hover:bg-accent hover:text-foreground transition-colors mt-1"
        >
          <Plus size={13} /> New Project
        </Link>
      </div>

      {/* Topics */}
      <div className="p-3 border-b border-border">
        <div className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider mb-2 px-1">Topics</div>
        {activeProject.topics.map(topic => (
          <button
            key={topic}
            onClick={() => setActiveTopic(topic)}
            className={`w-full flex items-center gap-2 px-2 py-1.5 text-xs rounded-md text-left transition-colors mb-0.5 ${activeTopic === topic ? 'bg-accent text-foreground' : 'text-muted-foreground hover:bg-accent hover:text-foreground'}`}
          >
            <Hash size={13} className="shrink-0" /> {topic}
          </button>
        ))}
        <button className="w-full flex items-center gap-2 px-2 py-1.5 text-xs rounded-md text-muted-foreground hover:bg-accent hover:text-foreground transition-colors mt-1">
          <Plus size={13} /> Add Topic
        </button>
      </div>

      {/* Voice & Video */}
      <div className="p-3 border-b border-border">
        <div className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider mb-2 px-1">Voice & Video</div>
        <button className="w-full flex items-center gap-2 px-2 py-1.5 text-xs rounded-md text-muted-foreground hover:bg-accent hover:text-foreground transition-colors mb-0.5">
          <Phone size={13} /> Voice Lounge
        </button>
        <button className="w-full flex items-center gap-2 px-2 py-1.5 text-xs rounded-md text-muted-foreground hover:bg-accent hover:text-foreground transition-colors">
          <Video size={13} /> Meeting Room
        </button>
      </div>

      {/* Files */}
      <div className="p-3 border-b border-border">
        <div className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider mb-2 px-1">Files</div>
        <button className="w-full flex items-center gap-2 px-2 py-1.5 text-xs rounded-md text-muted-foreground hover:bg-accent hover:text-foreground transition-colors mb-0.5">
          <FileText size={13} /> README.md
        </button>
        <button className="w-full flex items-center gap-2 px-2 py-1.5 text-xs rounded-md text-muted-foreground hover:bg-accent hover:text-foreground transition-colors">
          <Plus size={13} /> New File
        </button>
      </div>

      {/* Shared Panels */}
      <div className="p-3 border-b border-border">
        <div className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider mb-2 px-1">Tools</div>
        <button className="w-full flex items-center gap-2 px-2 py-1.5 text-xs rounded-md text-muted-foreground hover:bg-accent hover:text-foreground transition-colors mb-0.5">
          <Bot size={13} /> AI Agent Panel
        </button>
        <button className="w-full flex items-center gap-2 px-2 py-1.5 text-xs rounded-md text-muted-foreground hover:bg-accent hover:text-foreground transition-colors">
          <Users size={13} /> Members
        </button>
      </div>

      {/* Project Wallet */}
      <div className="mt-auto p-3">
        <div className="rounded-lg bg-primary/5 border border-primary/20 p-3">
          <div className="flex items-center gap-2 mb-1">
            <Wallet size={13} className="text-primary" />
            <span className="text-xs font-semibold text-primary">Project Wallet</span>
          </div>
          <div className="text-lg font-bold">{activeProject.wallet.toLocaleString()}</div>
          <div className="text-[10px] text-muted-foreground">credits available</div>
        </div>
      </div>
    </div>
  );

  return (
    <AppShell>
      <SidebarLayout sidebar={sidebar} sidebarWidth={220}>
        <div className="h-full flex flex-col">
          {/* Topic header */}
          <div className="px-6 py-3 border-b border-border flex items-center gap-2">
            <Hash size={16} className="text-muted-foreground" />
            <span className="font-semibold text-sm">{activeTopic}</span>
            <span className="text-xs text-muted-foreground ml-2">— {activeProject.name}</span>
          </div>

          {/* Embedded Rocket.Chat for topic */}
          <div className="flex-1 overflow-hidden p-4">
            <EmbeddedChat channel={`${activeProject.id}-${activeTopic}`} className="h-full" />
          </div>
        </div>
      </SidebarLayout>
    </AppShell>
  );
}
