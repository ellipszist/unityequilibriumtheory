'use client';

import { useState, useRef, useCallback } from 'react';
import {
  ExternalLink, Loader2, Bot, Database, FileUp, FileText,
  CheckSquare, Square, Trash2, Sparkles, ChevronLeft, ChevronRight,
} from 'lucide-react';

const LOBECHAT_URL = process.env.NEXT_PUBLIC_LOBECHAT_URL || 'http://localhost:3100';
const AGENT_URL = process.env.NEXT_PUBLIC_AGENT_URL || 'http://localhost:8001';

interface RagFile {
  id: string;
  name: string;
  type: string;
  size?: number;
  content: string;
  checked: boolean;
  ingested: boolean;
}

export default function EmbeddedLobeChat({ projectScope = 'workchat' }: { projectScope?: string }) {
  const [isLoaded, setIsLoaded] = useState(false);
  const [ragFiles, setRagFiles] = useState<RagFile[]>([]);
  const [ragDragging, setRagDragging] = useState(false);
  const [ingesting, setIngesting] = useState(false);
  const [ragCollapsed, setRagCollapsed] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);

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
      const newFile: RagFile = {
        id: `${Date.now()}-${Math.random()}`,
        name: file.name,
        type: file.name.split('.').pop()?.toLowerCase() || 'file',
        size: file.size,
        content,
        checked: true,
        ingested: false,
      };
      setRagFiles(prev => [...prev, newFile]);
      /* Auto-ingest immediately */
      try {
        const res = await fetch(`${AGENT_URL}/ingest`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            doc_id: newFile.id, text: content, source_type: newFile.type,
            project_scope: projectScope, doc_version: 'v1',
            tags: [newFile.type], ingest_mode: 'manual',
          }),
        });
        if (res.ok) {
          setRagFiles(prev => prev.map(f => f.id === newFile.id ? { ...f, ingested: true } : f));
        }
      } catch { /* agent offline */ }
    }
  }, [projectScope]);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault(); setRagDragging(false);
    addFiles(e.dataTransfer.files);
  }, [addFiles]);

  const toggleCheck = async (id: string) => {
    const file = ragFiles.find(f => f.id === id);
    if (!file) return;
    const nowChecked = !file.checked;
    setRagFiles(prev => prev.map(f => f.id === id ? { ...f, checked: nowChecked } : f));
    if (nowChecked && !file.ingested) {
      try {
        await fetch(`${AGENT_URL}/ingest`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            doc_id: id, text: file.content, source_type: file.type,
            project_scope: projectScope, doc_version: 'v1',
            tags: [file.type], ingest_mode: 'manual',
          }),
        });
        setRagFiles(prev => prev.map(f => f.id === id ? { ...f, ingested: true } : f));
      } catch { /* offline */ }
    }
  };

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
            project_scope: projectScope, doc_version: 'v1',
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
    <div className="flex h-full w-full overflow-hidden bg-background">

      {/* ── LEFT: RAG Sources panel (NotebookLM style) ── */}
      <div className={`shrink-0 border-r border-border flex flex-col bg-muted/5 transition-[width] duration-200 overflow-hidden ${ragCollapsed ? 'w-0 border-0' : 'w-[260px]'}`}>
        {!ragCollapsed && (
          <>
            {/* Header */}
            <div className="px-3 pt-3 pb-2 border-b border-border shrink-0">
              <div className="flex items-center gap-2 mb-0.5">
                <Database size={13} className="text-primary" />
                <span className="text-xs font-semibold">Knowledge Sources</span>
                {checkedCount > 0 && (
                  <span className="ml-auto text-[9px] bg-primary/10 text-primary px-1.5 rounded-full font-bold">{checkedCount} active</span>
                )}
              </div>
              <p className="text-[10px] text-muted-foreground">ยัดไฟล์ให้ UET Agent อ่าน (NotebookLM style)</p>
            </div>

            {/* Drop zone */}
            <div className="px-2 pt-2 pb-1 shrink-0">
              <div
                onDragOver={e => { e.preventDefault(); setRagDragging(true); }}
                onDragLeave={() => setRagDragging(false)}
                onDrop={handleDrop}
                onClick={() => fileRef.current?.click()}
                className={`cursor-pointer rounded-xl border-2 border-dashed flex flex-col items-center justify-center gap-1.5 py-5 transition-all ${
                  ragDragging ? 'border-primary bg-primary/5' : 'border-border hover:border-primary/50 hover:bg-muted/20'
                }`}
              >
                <FileUp size={20} className={ragDragging ? 'text-primary' : 'text-muted-foreground/30'} />
                <p className="text-[10px] font-medium">วางไฟล์หรือคลิกเพื่อเลือก</p>
                <p className="text-[9px] text-muted-foreground">PDF, TXT, MD, CSV</p>
                <input ref={fileRef} type="file" multiple accept=".pdf,.txt,.md,.csv,.json" className="hidden"
                  onChange={e => addFiles(e.target.files)} />
              </div>
            </div>

            {/* File list with checkboxes */}
            <div className="flex-1 overflow-y-auto px-2 py-1 space-y-0.5">
              {ragFiles.length === 0 ? (
                <div className="flex flex-col items-center justify-center h-full py-8 text-center text-muted-foreground/40 gap-2">
                  <Bot size={24} className="opacity-15" />
                  <p className="text-[10px]">เพิ่มไฟล์เพื่อให้ AI อ่านประกอบการตอบ</p>
                </div>
              ) : ragFiles.map(f => (
                <div key={f.id} className="group flex items-center gap-1.5 px-1.5 py-1.5 rounded-lg hover:bg-muted/40 transition-colors">
                  <button onClick={() => toggleCheck(f.id)} className="shrink-0">
                    {f.checked
                      ? <CheckSquare size={13} className="text-primary" />
                      : <Square size={13} className="text-muted-foreground/40" />}
                  </button>
                  <div className="flex-1 min-w-0">
                    <p className={`text-[10px] truncate font-medium ${f.checked ? 'text-foreground' : 'text-muted-foreground'}`}>{f.name}</p>
                    <p className="text-[8px] text-muted-foreground">
                      {f.type.toUpperCase()}
                      {f.size ? ` · ${Math.round(f.size / 1024)}KB` : ''}
                      {f.ingested && <span className="text-green-500 ml-1">✓ ingested</span>}
                    </p>
                  </div>
                  <button onClick={() => setRagFiles(prev => prev.filter(rf => rf.id !== f.id))}
                    className="opacity-0 group-hover:opacity-100 transition-opacity shrink-0">
                    <Trash2 size={9} className="text-muted-foreground hover:text-red-500" />
                  </button>
                </div>
              ))}
            </div>

            {/* Batch ingest button */}
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

            {/* External link */}
            <div className="px-3 pb-3 pt-1 border-t border-border shrink-0">
              <a href={LOBECHAT_URL} target="_blank" rel="noopener noreferrer"
                className="flex items-center gap-1.5 text-[10px] text-muted-foreground hover:text-foreground transition-colors"
              >
                <ExternalLink size={10} /> เปิด LobeChat แบบ fullscreen
              </a>
            </div>
          </>
        )}
      </div>

      {/* Collapse toggle strip */}
      <button
        onClick={() => setRagCollapsed(v => !v)}
        className="shrink-0 w-4 flex items-center justify-center bg-muted/20 hover:bg-muted/60 border-r border-border transition-colors z-10"
        title={ragCollapsed ? 'Show RAG Sources' : 'Hide RAG Sources'}
      >
        {ragCollapsed
          ? <ChevronRight size={12} className="text-muted-foreground" />
          : <ChevronLeft size={12} className="text-muted-foreground" />}
      </button>

      {/* ── RIGHT: LobeChat iframe ── */}
      <div className="flex-1 min-w-0 relative">
        {!isLoaded && (
          <div className="absolute inset-0 flex flex-col items-center justify-center bg-background z-10 gap-3">
            <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center">
              <Bot className="w-5 h-5 text-primary" />
            </div>
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>กำลังเชื่อมต่อ LobeChat...</span>
            </div>
            <p className="text-[10px] text-muted-foreground/60">
              ต้องรัน <code className="bg-muted px-1 rounded">docker compose up lobe_chat</code> ก่อน
            </p>
          </div>
        )}
        <iframe
          src={LOBECHAT_URL}
          className="w-full h-full border-0"
          onLoad={() => setIsLoaded(true)}
          allow="camera; microphone; fullscreen; clipboard-read; clipboard-write"
          title="LobeChat — UET Agent Studio"
        />
      </div>
    </div>
  );
}
