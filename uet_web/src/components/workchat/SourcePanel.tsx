'use client';

import React, { useState, useRef, useCallback } from 'react';
import { FileText, Plus, Database, AlignLeft, Upload, Link, FileUp, Trash2 } from 'lucide-react';

interface SourcePanelProps {
  sources: any[];
  onSourceAdd: (source: any) => void;
}

type AddMode = 'file' | 'text' | 'url';

const SOURCE_ICON: Record<string, React.ReactNode> = {
  pdf:  <FileText className="w-3.5 h-3.5 text-red-400" />,
  txt:  <FileText className="w-3.5 h-3.5 text-blue-400" />,
  md:   <FileText className="w-3.5 h-3.5 text-purple-400" />,
  text: <AlignLeft className="w-3.5 h-3.5 text-emerald-400" />,
  url:  <Link className="w-3.5 h-3.5 text-amber-400" />,
};

const AGENT_URL = typeof window !== 'undefined'
  ? (process.env.NEXT_PUBLIC_AGENT_URL || 'http://localhost:8001')
  : 'http://localhost:8001';

async function ingestToAgent(source: any) {
  try {
    await fetch(`${AGENT_URL}/ingest`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        doc_id: source.id,
        text: source.content,
        source_type: source.type,
        project_scope: 'workchat-local',
        doc_version: 'v1',
        tags: [source.type],
        ingest_mode: 'manual',
      }),
    });
  } catch {
    /* Agent offline — source still added to local state */
  }
}

export default function SourcePanel({ sources, onSourceAdd }: SourcePanelProps) {
  const [mode, setMode] = useState<AddMode>('file');
  const [inputText, setInputText] = useState('');
  const [urlInput, setUrlInput] = useState('');
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const readFile = (file: File): Promise<string> =>
    new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result as string);
      reader.onerror = reject;
      reader.readAsText(file);
    });

  const addFileSource = async (file: File) => {
    const ext = file.name.split('.').pop()?.toLowerCase() || 'txt';
    let content = '';
    try { content = await readFile(file); } catch { content = `[Binary file: ${file.name}]`; }
    const source = {
      id: Date.now().toString(),
      type: ext,
      title: file.name,
      content,
      size: file.size,
      createdAt: new Date().toISOString(),
      ingested: false,
    };
    onSourceAdd(source);
    ingestToAgent(source);
  };

  const handleFiles = useCallback(async (files: FileList | null) => {
    if (!files) return;
    for (const file of Array.from(files)) await addFileSource(file);
  }, [sources.length]);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    handleFiles(e.dataTransfer.files);
  }, [handleFiles]);

  const handleAddText = () => {
    if (!inputText.trim()) return;
    const source = {
      id: Date.now().toString(),
      type: 'text',
      title: `Text snippet ${sources.length + 1}`,
      content: inputText.trim(),
      createdAt: new Date().toISOString(),
    };
    onSourceAdd(source);
    ingestToAgent(source);
    setInputText('');
  };

  const handleAddUrl = () => {
    if (!urlInput.trim()) return;
    const source = {
      id: Date.now().toString(),
      type: 'url',
      title: urlInput.replace(/^https?:\/\//, '').slice(0, 40),
      content: `[URL source] ${urlInput}`,
      url: urlInput,
      createdAt: new Date().toISOString(),
    };
    onSourceAdd(source);
    ingestToAgent(source);
    setUrlInput('');
  };

  const tabs: { id: AddMode; label: string; icon: React.ReactNode }[] = [
    { id: 'file', label: 'ไฟล์', icon: <Upload className="w-3 h-3" /> },
    { id: 'text', label: 'ข้อความ', icon: <AlignLeft className="w-3 h-3" /> },
    { id: 'url', label: 'URL', icon: <Link className="w-3 h-3" /> },
  ];

  return (
    <div className="flex flex-col h-full bg-muted/5">
      {/* Header */}
      <div className="px-4 pt-4 pb-3 border-b border-border shrink-0">
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-sm font-semibold flex items-center gap-2">
            <Database className="w-4 h-4 text-primary" />
            แหล่งข้อมูล
          </h2>
          <span className="text-[10px] bg-primary/10 text-primary px-2 py-0.5 rounded-full font-medium">
            {sources.length} source{sources.length !== 1 ? 's' : ''}
          </span>
        </div>

        {/* Add Mode Tabs */}
        <div className="flex gap-1 bg-muted/60 rounded-lg p-0.5">
          {tabs.map(t => (
            <button
              key={t.id}
              onClick={() => setMode(t.id)}
              className={`flex-1 flex items-center justify-center gap-1 text-[11px] py-1.5 rounded-md font-medium transition-all ${
                mode === t.id
                  ? 'bg-background shadow-sm text-foreground'
                  : 'text-muted-foreground hover:text-foreground'
              }`}
            >
              {t.icon} {t.label}
            </button>
          ))}
        </div>
      </div>

      {/* Add Source Zone */}
      <div className="px-3 pt-3 pb-2 border-b border-border shrink-0">
        {mode === 'file' && (
          <div
            onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
            onDragLeave={() => setIsDragging(false)}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
            className={`cursor-pointer rounded-xl border-2 border-dashed flex flex-col items-center justify-center gap-2 py-6 transition-all ${
              isDragging
                ? 'border-primary bg-primary/5 scale-[1.01]'
                : 'border-border hover:border-primary/50 hover:bg-muted/30'
            }`}
          >
            <FileUp className={`w-8 h-8 ${isDragging ? 'text-primary' : 'text-muted-foreground/40'}`} />
            <div className="text-center">
              <p className="text-xs font-medium">วางไฟล์ที่นี่ หรือคลิกเพื่อเลือก</p>
              <p className="text-[10px] text-muted-foreground mt-0.5">รองรับ PDF, TXT, MD, CSV</p>
            </div>
            <input
              ref={fileInputRef}
              type="file"
              multiple
              accept=".pdf,.txt,.md,.csv,.json"
              className="hidden"
              onChange={(e) => handleFiles(e.target.files)}
            />
          </div>
        )}

        {mode === 'text' && (
          <div className="space-y-2">
            <textarea
              className="w-full text-xs bg-background border border-border rounded-lg p-2.5 h-28 resize-none focus:outline-none focus:ring-1 focus:ring-primary"
              placeholder="วางข้อความ บทความ สมการ หรือเนื้อหาวิจัยที่นี่..."
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
            />
            <button
              onClick={handleAddText}
              disabled={!inputText.trim()}
              className="w-full bg-primary text-primary-foreground hover:bg-primary/90 disabled:opacity-40 text-xs py-2 rounded-lg font-medium transition-colors flex items-center justify-center gap-1.5"
            >
              <Plus className="w-3.5 h-3.5" /> เพิ่มข้อความ
            </button>
          </div>
        )}

        {mode === 'url' && (
          <div className="space-y-2">
            <input
              type="url"
              className="w-full text-xs bg-background border border-border rounded-lg p-2.5 focus:outline-none focus:ring-1 focus:ring-primary"
              placeholder="https://arxiv.org/abs/..."
              value={urlInput}
              onChange={(e) => setUrlInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleAddUrl()}
            />
            <p className="text-[10px] text-muted-foreground">ใส่ลิงก์บทความ, ArXiv, หรือหน้าเว็บที่ต้องการให้ AI อ่าน</p>
            <button
              onClick={handleAddUrl}
              disabled={!urlInput.trim()}
              className="w-full bg-primary text-primary-foreground hover:bg-primary/90 disabled:opacity-40 text-xs py-2 rounded-lg font-medium transition-colors flex items-center justify-center gap-1.5"
            >
              <Plus className="w-3.5 h-3.5" /> เพิ่ม URL
            </button>
          </div>
        )}
      </div>

      {/* Source List */}
      <div className="flex-1 overflow-y-auto px-3 py-2 space-y-2">
        {sources.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center text-muted-foreground/60 gap-2 pb-8">
            <Database className="w-10 h-10 opacity-15" />
            <p className="text-xs">ยังไม่มี Sources<br/>เพิ่มข้อมูลด้านบนเพื่อให้ Agent วิเคราะห์</p>
          </div>
        ) : (
          sources.map((source, i) => (
            <div
              key={source.id}
              className="group bg-card border border-border rounded-lg p-2.5 hover:border-primary/40 transition-colors"
            >
              <div className="flex items-start gap-2">
                <div className="w-6 h-6 rounded-md bg-muted flex items-center justify-center shrink-0 mt-0.5">
                  {SOURCE_ICON[source.type] || <FileText className="w-3.5 h-3.5 text-muted-foreground" />}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-[11px] font-medium truncate">{source.title}</p>
                  <p className="text-[10px] text-muted-foreground line-clamp-1 mt-0.5">
                    {source.type.toUpperCase()}
                    {source.size ? ` · ${Math.round(source.size / 1024)}KB` : ''}
                    {' · Added ' + new Date(source.createdAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </p>
                </div>
                <button
                  className="opacity-0 group-hover:opacity-100 transition-opacity p-1 rounded hover:bg-red-500/10 hover:text-red-500 text-muted-foreground"
                  onClick={() => {/* remove handled by parent if needed */}}
                  title="ลบ source"
                >
                  <Trash2 className="w-3 h-3" />
                </button>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Footer tip */}
      {sources.length > 0 && (
        <div className="px-3 pb-3 shrink-0">
          <div className="rounded-lg bg-primary/5 border border-primary/20 px-3 py-2 text-[10px] text-primary/80">
            💡 กด <span className="font-semibold">🤖 Train</span> ในช่องแชทเพื่อให้ Agent เรียนรู้ sources เหล่านี้
          </div>
        </div>
      )}
    </div>
  );
}
