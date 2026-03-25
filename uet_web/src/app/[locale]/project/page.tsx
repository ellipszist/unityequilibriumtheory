'use client';

import { useState, useRef, useCallback } from 'react';
import AppShell from '@/components/layout/AppShell';
import EmbeddedChat from '@/components/chat/EmbeddedChat';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import {
  FolderGit2, Hash, Phone, Video, FileText, Plus, Wallet, Users, Bot,
  ChevronDown, ChevronRight, Folder, FolderOpen, FileUp, Trash2,
  Database, CheckSquare, Square, Loader2, Sparkles,
} from 'lucide-react';

/* ─── Mock Data ─── */
const MOCK_PROJECTS = [
  {
    id: 'proj-1', name: 'UET Core Research',
    topics: ['general', 'equations', 'proofs'],
    wallet: 1200,
    files: [
      { id: 'f1', name: 'README.md', type: 'md' },
      { id: 'f2', name: 'master_equation.md', type: 'md' },
      { id: 'f3', name: 'results_q1.md', type: 'md' },
    ],
  },
  {
    id: 'proj-2', name: 'AI Alignment Study',
    topics: ['general', 'papers', 'discussion'],
    wallet: 450,
    files: [
      { id: 'f4', name: 'README.md', type: 'md' },
      { id: 'f5', name: 'alignment_notes.md', type: 'md' },
    ],
  },
];

const AGENT_URL = process.env.NEXT_PUBLIC_AGENT_URL || 'http://localhost:8001';

/* ─── Types ─── */
interface RagFile {
  id: string;
  name: string;
  type: string;
  size?: number;
  content: string;
  checked: boolean;   /* NotebookLM: tick = AI reads this file */
  ingested: boolean;
}

export default function ProjectPage() {
  const params = useParams();
  const locale = (params?.locale as string) || 'en';

  /* Project / topic state */
  const [activeProject, setActiveProject] = useState(MOCK_PROJECTS[0]);
  const [activeTopic, setActiveTopic] = useState('general');
  const [activeFile, setActiveFile] = useState<string | null>(null);
  const [filesExpanded, setFilesExpanded] = useState(true);
  const [ragExpanded, setRagExpanded] = useState(true);

  /* RAG files in sidebar */
  const [ragFiles, setRagFiles] = useState<RagFile[]>([]);
  const [ragDragging, setRagDragging] = useState(false);
  const [ingesting, setIngesting] = useState(false);
  const ragFileRef = useRef<HTMLInputElement>(null);

  /* Read file text */
  const readText = (f: File): Promise<string> =>
    new Promise((res, rej) => {
      const r = new FileReader();
      r.onload = () => res(r.result as string);
      r.onerror = rej;
      r.readAsText(f);
    });

  const addFiles = useCallback(async (files: FileList | null) => {
    if (!files) return;
    for (const file of Array.from(files)) {
      let content = '';
      try { content = await readText(file); } catch { content = `[Binary: ${file.name}]`; }
      setRagFiles(prev => [...prev, {
        id: Date.now().toString() + Math.random(),
        name: file.name,
        type: file.name.split('.').pop()?.toLowerCase() || 'file',
        size: file.size,
        content,
        checked: true,   /* auto-checked when added */
        ingested: false,
      }]);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault(); setRagDragging(false);
    addFiles(e.dataTransfer.files);
  }, [addFiles]);

  /* Toggle checkbox — if turning on and not yet ingested, ingest now */
  const toggleCheck = async (id: string) => {
    const file = ragFiles.find(f => f.id === id);
    if (!file) return;
    const nowChecked = !file.checked;
    setRagFiles(prev => prev.map(f => f.id === id ? { ...f, checked: nowChecked } : f));

    if (nowChecked && !file.ingested) {
      /* Auto-ingest to uet_agents */
      try {
        await fetch(`${AGENT_URL}/ingest`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            doc_id: id, text: file.content, source_type: file.type,
            project_scope: activeProject.id, doc_version: 'v1',
            tags: [file.type], ingest_mode: 'manual',
          }),
        });
        setRagFiles(prev => prev.map(f => f.id === id ? { ...f, ingested: true } : f));
      } catch { /* agent offline — still visually checked */ }
    }
  };

  /* Ingest all checked files at once */
  const ingestAll = async () => {
    const targets = ragFiles.filter(f => f.checked && !f.ingested);
    if (!targets.length) return;
    setIngesting(true);
    for (const f of targets) {
      try {
        await fetch(`${AGENT_URL}/ingest`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            doc_id: f.id, text: f.content, source_type: f.type,
            project_scope: activeProject.id, doc_version: 'v1',
            tags: [f.type], ingest_mode: 'manual',
          }),
        });
        setRagFiles(prev => prev.map(rf => rf.id === f.id ? { ...rf, ingested: true } : rf));
      } catch { /* offline */ }
    }
    setIngesting(false);
  };

  const checkedCount = ragFiles.filter(f => f.checked).length;

  return (
    <AppShell>
      <div className="flex h-[calc(100vh-56px)] overflow-hidden">

        {/* ══════════════════════════════════════
            LEFT SIDEBAR — Nav + RAG
        ══════════════════════════════════════ */}
        <aside className="w-[240px] shrink-0 border-r border-border bg-muted/10 flex flex-col overflow-hidden">

          {/* Project selector */}
          <div className="p-3 border-b border-border shrink-0">
            <div className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider mb-2 px-1">Projects</div>
            {MOCK_PROJECTS.map(p => (
              <button
                key={p.id}
                onClick={() => { setActiveProject(p); setActiveTopic('general'); setActiveFile(null); setRagFiles([]); }}
                className={`w-full flex items-center gap-2 px-2 py-1.5 text-xs rounded-md text-left transition-colors mb-0.5 ${
                  activeProject.id === p.id ? 'bg-primary/10 text-primary' : 'hover:bg-accent text-foreground'
                }`}
              >
                <FolderGit2 size={13} className="shrink-0" />
                <span className="truncate">{p.name}</span>
              </button>
            ))}
            <Link href={`/${locale}/project/new`}
              className="w-full flex items-center gap-2 px-2 py-1.5 text-xs rounded-md text-muted-foreground hover:bg-accent hover:text-foreground transition-colors mt-1"
            >
              <Plus size={13} /> New Project
            </Link>
          </div>

          {/* Topics */}
          <div className="p-3 border-b border-border shrink-0">
            <div className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider mb-2 px-1">Topics</div>
            {activeProject.topics.map(topic => (
              <button key={topic} onClick={() => setActiveTopic(topic)}
                className={`w-full flex items-center gap-2 px-2 py-1.5 text-xs rounded-md text-left transition-colors mb-0.5 ${
                  activeTopic === topic ? 'bg-accent font-semibold text-foreground' : 'text-muted-foreground hover:bg-accent hover:text-foreground'
                }`}
              >
                <Hash size={13} className="shrink-0" /> {topic}
              </button>
            ))}
            <button className="w-full flex items-center gap-2 px-2 py-1.5 text-xs rounded-md text-muted-foreground hover:bg-accent hover:text-foreground transition-colors mt-1">
              <Plus size={13} /> Add Topic
            </button>
          </div>

          {/* Voice & Video */}
          <div className="p-3 border-b border-border shrink-0">
            <div className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider mb-2 px-1">Voice & Video</div>
            <button className="w-full flex items-center gap-2 px-2 py-1.5 text-xs rounded-md text-muted-foreground hover:bg-accent hover:text-foreground transition-colors mb-0.5">
              <Phone size={13} /> Voice Lounge
            </button>
            <button className="w-full flex items-center gap-2 px-2 py-1.5 text-xs rounded-md text-muted-foreground hover:bg-accent hover:text-foreground transition-colors">
              <Video size={13} /> Meeting Room
            </button>
          </div>

          {/* Obsidian File Explorer */}
          <div className="p-3 border-b border-border shrink-0">
            <button
              className="flex items-center gap-1 text-[10px] font-semibold text-muted-foreground uppercase tracking-wider mb-2 px-1 w-full hover:text-foreground transition-colors"
              onClick={() => setFilesExpanded(v => !v)}
            >
              {filesExpanded ? <ChevronDown size={10} /> : <ChevronRight size={10} />}
              {filesExpanded ? <FolderOpen size={11} /> : <Folder size={11} />}
              <span className="ml-1">Files</span>
            </button>
            {filesExpanded && (
              <div className="space-y-0.5 ml-1">
                {activeProject.files.map(file => (
                  <button key={file.id} onClick={() => setActiveFile(file.id)}
                    className={`w-full flex items-center gap-2 px-2 py-1.5 text-xs rounded-md text-left transition-colors group ${
                      activeFile === file.id ? 'bg-primary/10 text-primary' : 'text-muted-foreground hover:bg-accent hover:text-foreground'
                    }`}
                  >
                    <FileText size={11} className="shrink-0" />
                    <span className="truncate flex-1">{file.name}</span>
                    <Trash2 size={9} className="opacity-0 group-hover:opacity-50 shrink-0" />
                  </button>
                ))}
                <button className="w-full flex items-center gap-1.5 px-2 py-1.5 text-xs rounded-md text-muted-foreground hover:bg-accent hover:text-foreground transition-colors">
                  <Plus size={11} /> New .md File
                </button>
              </div>
            )}
          </div>

          {/* ══ RAG KNOWLEDGE SOURCES (NotebookLM style) ══ */}
          <div className="flex-1 overflow-y-auto flex flex-col min-h-0">
            {/* RAG section header */}
            <button
              className="flex items-center justify-between px-3 py-2.5 border-b border-border w-full hover:bg-muted/20 transition-colors shrink-0"
              onClick={() => setRagExpanded(v => !v)}
            >
              <span className="flex items-center gap-1.5 text-[10px] font-semibold text-muted-foreground uppercase tracking-wider">
                <Database size={10} className="text-primary" />
                RAG Sources
                {checkedCount > 0 && (
                  <span className="bg-primary/10 text-primary text-[9px] px-1.5 rounded-full font-bold">{checkedCount} active</span>
                )}
              </span>
              {ragExpanded ? <ChevronDown size={10} className="text-muted-foreground" /> : <ChevronRight size={10} className="text-muted-foreground" />}
            </button>

            {ragExpanded && (
              <div className="flex flex-col flex-1 min-h-0">
                {/* Drop zone */}
                <div className="px-2 pt-2 pb-1 shrink-0">
                  <div
                    onDragOver={e => { e.preventDefault(); setRagDragging(true); }}
                    onDragLeave={() => setRagDragging(false)}
                    onDrop={handleDrop}
                    onClick={() => ragFileRef.current?.click()}
                    className={`cursor-pointer rounded-lg border-2 border-dashed flex items-center justify-center gap-2 py-3 transition-all ${
                      ragDragging ? 'border-primary bg-primary/5' : 'border-border hover:border-primary/40 hover:bg-muted/20'
                    }`}
                  >
                    <FileUp size={14} className={ragDragging ? 'text-primary' : 'text-muted-foreground/40'} />
                    <div>
                      <p className="text-[10px] font-medium">วางไฟล์หรือคลิก</p>
                      <p className="text-[9px] text-muted-foreground">PDF, TXT, MD, CSV</p>
                    </div>
                    <input ref={ragFileRef} type="file" multiple accept=".pdf,.txt,.md,.csv,.json" className="hidden"
                      onChange={e => addFiles(e.target.files)} />
                  </div>
                </div>

                {/* File list with checkboxes */}
                <div className="flex-1 overflow-y-auto px-2 py-1 space-y-0.5">
                  {ragFiles.length === 0 ? (
                    <div className="flex flex-col items-center justify-center py-6 text-center text-muted-foreground/40 gap-1.5">
                      <Database size={20} className="opacity-15" />
                      <p className="text-[9px]">เพิ่มไฟล์เพื่อให้<br/>AI อ่านประกอบ</p>
                    </div>
                  ) : ragFiles.map(f => (
                    <div key={f.id} className="group flex items-center gap-1.5 px-1.5 py-1.5 rounded-lg hover:bg-muted/40 transition-colors">
                      {/* Checkbox */}
                      <button onClick={() => toggleCheck(f.id)} className="shrink-0">
                        {f.checked
                          ? <CheckSquare size={13} className="text-primary" />
                          : <Square size={13} className="text-muted-foreground/40" />}
                      </button>
                      {/* File info */}
                      <div className="flex-1 min-w-0">
                        <p className={`text-[10px] truncate font-medium ${f.checked ? 'text-foreground' : 'text-muted-foreground'}`}>{f.name}</p>
                        <p className="text-[8px] text-muted-foreground flex items-center gap-1">
                          {f.type.toUpperCase()}
                          {f.size ? ` · ${Math.round(f.size / 1024)}KB` : ''}
                          {f.ingested && <span className="text-green-500">· ✓ ingested</span>}
                        </p>
                      </div>
                      {/* Delete */}
                      <button
                        onClick={() => setRagFiles(prev => prev.filter(rf => rf.id !== f.id))}
                        className="opacity-0 group-hover:opacity-100 transition-opacity shrink-0"
                      >
                        <Trash2 size={9} className="text-muted-foreground hover:text-red-500" />
                      </button>
                    </div>
                  ))}
                </div>

                {/* Ingest button — only shown when there are checked but not-yet-ingested files */}
                {ragFiles.some(f => f.checked && !f.ingested) && (
                  <div className="px-2 pb-2 pt-1 shrink-0">
                    <button onClick={ingestAll} disabled={ingesting}
                      className="w-full bg-primary text-primary-foreground hover:bg-primary/90 disabled:opacity-60 text-[11px] py-1.5 rounded-lg font-medium transition-colors flex items-center justify-center gap-1.5"
                    >
                      {ingesting
                        ? <><Loader2 size={11} className="animate-spin" /> กำลังอ่าน...</>
                        : <><Sparkles size={11} /> ให้ AI อ่านไฟล์ที่เลือก ({ragFiles.filter(f => f.checked && !f.ingested).length})</>
                      }
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Tools */}
          <div className="p-3 border-t border-border shrink-0">
            <button className="w-full flex items-center gap-2 px-2 py-1.5 text-xs rounded-md text-muted-foreground hover:bg-accent hover:text-foreground transition-colors mb-0.5">
              <Bot size={13} /> AI Agent Panel
            </button>
            <button className="w-full flex items-center gap-2 px-2 py-1.5 text-xs rounded-md text-muted-foreground hover:bg-accent hover:text-foreground transition-colors">
              <Users size={13} /> Members
            </button>
          </div>

          {/* Project Wallet */}
          <div className="p-3 shrink-0 border-t border-border">
            <div className="rounded-lg bg-primary/5 border border-primary/20 p-2.5">
              <div className="flex items-center gap-2 mb-0.5">
                <Wallet size={12} className="text-primary" />
                <span className="text-xs font-semibold text-primary">Project Wallet</span>
              </div>
              <div className="text-base font-bold">{activeProject.wallet.toLocaleString()}</div>
              <div className="text-[10px] text-muted-foreground">credits available</div>
            </div>
          </div>
        </aside>

        {/* ══════════════════════════════════════
            CENTER: EmbeddedChat (Rocket.Chat)
        ══════════════════════════════════════ */}
        <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
          {/* Topic header */}
          <div className="px-4 py-2.5 border-b border-border flex items-center gap-2 shrink-0">
            <Hash size={15} className="text-muted-foreground shrink-0" />
            <span className="font-semibold text-sm">{activeTopic}</span>
            <span className="text-xs text-muted-foreground">— {activeProject.name}</span>
            {checkedCount > 0 && (
              <span className="ml-auto text-[9px] bg-primary/10 text-primary border border-primary/20 px-2 py-0.5 rounded-full font-medium flex items-center gap-1">
                <Database size={9} /> {checkedCount} RAG source{checkedCount > 1 ? 's' : ''} active
              </span>
            )}
          </div>

          {/* Chat area */}
          <div className="flex-1 overflow-hidden p-3">
            <EmbeddedChat channel={`${activeProject.id}-${activeTopic}`} className="h-full" />
          </div>
        </div>

      </div>
    </AppShell>
  );
}
