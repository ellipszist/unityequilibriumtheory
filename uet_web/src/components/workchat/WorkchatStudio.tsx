'use client';

import React, { useState, useRef, useEffect, useCallback } from 'react';
import {
  Send, Bot, User, Sparkles, Activity, Settings2, ChevronLeft, ChevronRight,
  FileUp, FileText, Trash2, Plus, Database,
  ToggleLeft, ToggleRight, ChevronDown, ChevronUp,
  Coins, TrendingUp, X, CheckCircle2, Loader2,
} from 'lucide-react';

/* ─── Constants ─── */
const AGENT_URL = process.env.NEXT_PUBLIC_AGENT_URL || 'http://localhost:8001';

const MODELS = [
  { id: 'glm-4.7-flash', label: 'GLM 4.7 Flash', badge: 'Fast', color: 'text-emerald-500' },
  { id: 'qwen-2.5-7b', label: 'Qwen 2.5 7B', badge: 'Balanced', color: 'text-blue-500' },
  { id: 'uet-local', label: 'UET Local', badge: 'Research', color: 'text-purple-500' },
];

const TOOLS = [
  { id: 'rag', label: 'RAG Search', desc: 'ค้นหาจาก Sources ที่เพิ่มไว้', defaultOn: true },
  { id: 'pouw', label: 'PoUW Mining', desc: 'คำนวณสมการ UET ขณะตอบ', defaultOn: true },
  { id: 'web', label: 'Web Search', desc: 'ค้นหาจากอินเทอร์เน็ต', defaultOn: false },
  { id: 'code', label: 'Code Executor', desc: 'รัน Python sandbox', defaultOn: false },
];

/* ─── Types ─── */
interface Source { id: string; type: string; title: string; content: string; size?: number; }
interface Message { id: string; role: 'user' | 'agent' | 'system'; content: string; ts: string; pouw?: number; }
type AddMode = 'file' | 'text' | 'url';

/* ─── Helpers ─── */
async function ingestToAgent(source: Source) {
  try {
    await fetch(`${AGENT_URL}/ingest`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        doc_id: source.id, text: source.content, source_type: source.type,
        project_scope: 'workchat-local', doc_version: 'v1',
        tags: [source.type], ingest_mode: 'manual',
      }),
    });
  } catch { /* agent offline – source still stored locally */ }
}

/* ══════════════════════════════════════════════════
   LEFT PANEL — Agent Config (LobeChat-style)
══════════════════════════════════════════════════ */
function AgentConfigPanel({
  sources, onSourceAdd, onSourceRemove,
  selectedModel, onModelChange,
  systemPrompt, onPromptChange,
  tools, onToolToggle,
}: {
  sources: Source[];
  onSourceAdd: (s: Source) => void;
  onSourceRemove: (id: string) => void;
  selectedModel: string;
  onModelChange: (id: string) => void;
  systemPrompt: string;
  onPromptChange: (v: string) => void;
  tools: Record<string, boolean>;
  onToolToggle: (id: string) => void;
}) {
  const [addMode, setAddMode] = useState<AddMode>('file');
  const [textInput, setTextInput] = useState('');
  const [urlInput, setUrlInput] = useState('');
  const [isDragging, setIsDragging] = useState(false);
  const [showPrompt, setShowPrompt] = useState(true);
  const [showSources, setShowSources] = useState(true);
  const [showTools, setShowTools] = useState(true);
  const fileRef = useRef<HTMLInputElement>(null);

  const readFile = (f: File): Promise<string> =>
    new Promise((res, rej) => {
      const r = new FileReader();
      r.onload = () => res(r.result as string);
      r.onerror = rej;
      r.readAsText(f);
    });

  const addFile = useCallback(async (file: File) => {
    const ext = file.name.split('.').pop()?.toLowerCase() || 'txt';
    let content = '';
    try { content = await readFile(file); } catch { content = `[Binary: ${file.name}]`; }
    const src: Source = { id: Date.now().toString(), type: ext, title: file.name, content, size: file.size };
    onSourceAdd(src);
    ingestToAgent(src);
  }, [onSourceAdd]);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault(); setIsDragging(false);
    Array.from(e.dataTransfer.files).forEach(addFile);
  }, [addFile]);

  const handleAddText = () => {
    if (!textInput.trim()) return;
    const src: Source = { id: Date.now().toString(), type: 'text', title: `Snippet ${sources.length + 1}`, content: textInput.trim() };
    onSourceAdd(src); ingestToAgent(src); setTextInput('');
  };

  const handleAddUrl = () => {
    if (!urlInput.trim()) return;
    const src: Source = { id: Date.now().toString(), type: 'url', title: urlInput.replace(/^https?:\/\//, '').slice(0, 40), content: `[URL] ${urlInput}`, };
    onSourceAdd(src); ingestToAgent(src); setUrlInput('');
  };

  return (
    <div className="flex flex-col h-full overflow-y-auto bg-muted/5">
      {/* Header */}
      <div className="px-4 pt-4 pb-3 border-b border-border shrink-0">
        <h2 className="text-sm font-semibold flex items-center gap-2">
          <Settings2 className="w-4 h-4 text-primary" /> Agent Studio
        </h2>
        <p className="text-[10px] text-muted-foreground mt-0.5">ตั้งค่า Agent และ Knowledge Sources</p>
      </div>

      {/* ── Model Picker ── */}
      <div className="px-3 py-3 border-b border-border/60">
        <p className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider mb-2">โมเดล AI</p>
        <div className="space-y-1">
          {MODELS.map(m => (
            <button key={m.id} onClick={() => onModelChange(m.id)}
              className={`w-full flex items-center justify-between px-3 py-2 rounded-lg text-xs transition-all ${
                selectedModel === m.id ? 'bg-primary/10 border border-primary/30 text-foreground' : 'hover:bg-muted border border-transparent text-muted-foreground'
              }`}
            >
              <span className="font-medium">{m.label}</span>
              <span className={`text-[9px] font-bold ${m.color}`}>{m.badge}</span>
            </button>
          ))}
        </div>
      </div>

      {/* ── System Prompt ── */}
      <div className="px-3 py-3 border-b border-border/60">
        <button onClick={() => setShowPrompt(v => !v)}
          className="flex items-center justify-between w-full text-[10px] font-semibold text-muted-foreground uppercase tracking-wider mb-2"
        >
          System Prompt {showPrompt ? <ChevronUp size={10} /> : <ChevronDown size={10} />}
        </button>
        {showPrompt && (
          <textarea
            value={systemPrompt}
            onChange={e => onPromptChange(e.target.value)}
            className="w-full text-xs bg-background border border-border rounded-lg p-2.5 h-24 resize-none focus:outline-none focus:ring-1 focus:ring-primary"
            placeholder="คุณคือ..."
          />
        )}
      </div>

      {/* ── Knowledge Sources (RAG) ── */}
      <div className="px-3 py-3 border-b border-border/60">
        <button onClick={() => setShowSources(v => !v)}
          className="flex items-center justify-between w-full text-[10px] font-semibold text-muted-foreground uppercase tracking-wider mb-2"
        >
          <span className="flex items-center gap-1">
            <Database size={10} /> Knowledge Sources
            {sources.length > 0 && (
              <span className="ml-1 bg-primary/10 text-primary px-1.5 rounded-full text-[9px]">{sources.length}</span>
            )}
          </span>
          {showSources ? <ChevronUp size={10} /> : <ChevronDown size={10} />}
        </button>

        {showSources && (
          <>
            {/* Tab switcher */}
            <div className="flex gap-0.5 bg-muted/60 rounded-lg p-0.5 mb-2">
              {([['file','ไฟล์'], ['text','ข้อความ'], ['url','URL']] as [AddMode,string][]).map(([id, label]) => (
                <button key={id} onClick={() => setAddMode(id)}
                  className={`flex-1 text-[10px] py-1 rounded-md font-medium transition-all ${
                    addMode === id ? 'bg-background shadow-sm text-foreground' : 'text-muted-foreground'
                  }`}
                >{label}</button>
              ))}
            </div>

            {/* File drop zone */}
            {addMode === 'file' && (
              <div
                onDragOver={e => { e.preventDefault(); setIsDragging(true); }}
                onDragLeave={() => setIsDragging(false)}
                onDrop={handleDrop}
                onClick={() => fileRef.current?.click()}
                className={`cursor-pointer rounded-xl border-2 border-dashed flex flex-col items-center justify-center gap-1.5 py-5 mb-2 transition-all ${
                  isDragging ? 'border-primary bg-primary/5' : 'border-border hover:border-primary/50 hover:bg-muted/20'
                }`}
              >
                <FileUp size={20} className={isDragging ? 'text-primary' : 'text-muted-foreground/30'} />
                <p className="text-[10px] font-medium">วางไฟล์หรือคลิกเพื่อเลือก</p>
                <p className="text-[9px] text-muted-foreground">PDF, TXT, MD, CSV</p>
                <input ref={fileRef} type="file" multiple accept=".pdf,.txt,.md,.csv,.json" className="hidden"
                  onChange={e => Array.from(e.target.files || []).forEach(addFile)} />
              </div>
            )}

            {/* Text input */}
            {addMode === 'text' && (
              <div className="space-y-1.5 mb-2">
                <textarea className="w-full text-xs bg-background border border-border rounded-lg p-2 h-20 resize-none focus:outline-none focus:ring-1 focus:ring-primary"
                  placeholder="วางบทความ, สมการ, หรือเนื้อหาวิจัย..."
                  value={textInput} onChange={e => setTextInput(e.target.value)} />
                <button onClick={handleAddText} disabled={!textInput.trim()}
                  className="w-full bg-primary text-primary-foreground text-[11px] py-1.5 rounded-lg font-medium disabled:opacity-40 flex items-center justify-center gap-1">
                  <Plus size={11} /> เพิ่ม
                </button>
              </div>
            )}

            {/* URL input */}
            {addMode === 'url' && (
              <div className="space-y-1.5 mb-2">
                <input type="url" className="w-full text-xs bg-background border border-border rounded-lg p-2 focus:outline-none focus:ring-1 focus:ring-primary"
                  placeholder="https://arxiv.org/abs/..."
                  value={urlInput} onChange={e => setUrlInput(e.target.value)}
                  onKeyDown={e => e.key === 'Enter' && handleAddUrl()} />
                <button onClick={handleAddUrl} disabled={!urlInput.trim()}
                  className="w-full bg-primary text-primary-foreground text-[11px] py-1.5 rounded-lg font-medium disabled:opacity-40 flex items-center justify-center gap-1">
                  <Plus size={11} /> เพิ่ม URL
                </button>
              </div>
            )}

            {/* Source list */}
            {sources.length > 0 && (
              <div className="space-y-1">
                {sources.map(s => (
                  <div key={s.id} className="group flex items-center gap-2 px-2 py-1.5 rounded-lg bg-card border border-border hover:border-primary/30">
                    <FileText size={10} className="text-primary shrink-0" />
                    <span className="text-[10px] truncate flex-1">{s.title}</span>
                    <button onClick={() => onSourceRemove(s.id)} className="opacity-0 group-hover:opacity-100 transition-opacity">
                      <Trash2 size={9} className="text-muted-foreground hover:text-red-500" />
                    </button>
                  </div>
                ))}
              </div>
            )}
          </>
        )}
      </div>

      {/* ── Tools ── */}
      <div className="px-3 py-3">
        <button onClick={() => setShowTools(v => !v)}
          className="flex items-center justify-between w-full text-[10px] font-semibold text-muted-foreground uppercase tracking-wider mb-2"
        >
          Tools {showTools ? <ChevronUp size={10} /> : <ChevronDown size={10} />}
        </button>
        {showTools && (
          <div className="space-y-2">
            {TOOLS.map(t => (
              <div key={t.id} className="flex items-center justify-between gap-2">
                <div>
                  <p className="text-xs font-medium">{t.label}</p>
                  <p className="text-[9px] text-muted-foreground">{t.desc}</p>
                </div>
                <button onClick={() => onToolToggle(t.id)} className="shrink-0">
                  {tools[t.id]
                    ? <ToggleRight className="w-5 h-5 text-primary" />
                    : <ToggleLeft className="w-5 h-5 text-muted-foreground/40" />}
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

/* ══════════════════════════════════════════════════
   POUW POPOVER — inline button in chat toolbar
══════════════════════════════════════════════════ */
function PoUWButton({ miningStatus, balance }: { miningStatus: any; balance: number }) {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handler = (e: MouseEvent) => { if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false); };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  const isActive = miningStatus && miningStatus.status !== 'Mining Complete';

  return (
    <div className="relative" ref={ref}>
      <button
        onClick={() => setOpen(v => !v)}
        className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs font-medium border transition-all ${
          isActive
            ? 'bg-amber-500/10 border-amber-500/40 text-amber-600 animate-pulse'
            : 'bg-muted/40 border-border text-muted-foreground hover:border-primary/40 hover:text-foreground'
        }`}
        title="PoUW Status & Wallet"
      >
        <Coins size={13} className={isActive ? 'text-amber-500' : ''} />
        <span>{balance.toLocaleString()}</span>
        {miningStatus?.reward && (
          <span className="text-[9px] text-green-500 font-bold">+{miningStatus.reward.toFixed(2)}</span>
        )}
      </button>

      {open && (
        <>
          {/* Backdrop */}
          <div className="fixed inset-0 z-40" onClick={() => setOpen(false)} />
          <div className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-72 bg-card border border-border rounded-xl shadow-2xl z-50 p-4">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold flex items-center gap-1.5"><TrendingUp size={12} className="text-primary" /> PoUW & Wallet</span>
            <button onClick={() => setOpen(false)}><X size={12} className="text-muted-foreground" /></button>
          </div>

          {/* Balance */}
          <div className="bg-primary/5 border border-primary/20 rounded-lg p-2.5 mb-3">
            <p className="text-[9px] text-muted-foreground uppercase tracking-wider mb-1">Credits Available</p>
            <p className="text-xl font-bold">{balance.toLocaleString()}</p>
          </div>

          {/* Mini bar chart — last 7 sessions */}
          <div className="mb-3">
            <p className="text-[9px] text-muted-foreground uppercase tracking-wider mb-1.5">การใช้งาน 7 ครั้งล่าสุด</p>
            <div className="flex items-end gap-1 h-10">
              {[12, 34, 18, 55, 22, 41, miningStatus?.reward ? Math.round(miningStatus.reward * 10) : 8].map((v, i) => (
                <div key={i} className="flex-1 bg-primary/20 rounded-sm transition-all" style={{ height: `${Math.min(100, (v / 55) * 100)}%` }} />
              ))}
            </div>
            <div className="flex justify-between mt-0.5">
              <span className="text-[8px] text-muted-foreground">-7</span>
              <span className="text-[8px] text-muted-foreground">ตอนนี้</span>
            </div>
          </div>

          {/* Current mining status */}
          {miningStatus && (
            <div className="bg-muted/40 rounded-lg p-2">
              <div className="flex items-center gap-1.5 mb-1.5">
                {isActive ? <Loader2 size={10} className="animate-spin text-amber-500" /> : <CheckCircle2 size={10} className="text-green-500" />}
                <span className="text-[10px] font-medium truncate">{miningStatus.status}</span>
              </div>
              {miningStatus.progress !== undefined && (
                <div className="h-1 bg-muted rounded-full overflow-hidden">
                  <div className="h-full bg-primary rounded-full transition-all" style={{ width: `${miningStatus.progress}%` }} />
                </div>
              )}
              {miningStatus.reward && (
                <p className="text-[9px] text-green-500 font-bold mt-1">+{miningStatus.reward.toFixed(4)} credits earned</p>
              )}
            </div>
          )}
          </div>
        </>
      )}
    </div>
  );
}

/* ══════════════════════════════════════════════════
   RIGHT PANEL — Chat (functional, calls uet_agents)
══════════════════════════════════════════════════ */
function ChatArea({
  sources, selectedModel, systemPrompt, tools,
  isComputing, setIsComputing, miningStatus, setMiningStatus,
  projectScope,
}: {
  sources: Source[];
  selectedModel: string;
  systemPrompt: string;
  tools: Record<string, boolean>;
  isComputing: boolean;
  setIsComputing: (v: boolean) => void;
  miningStatus: any;
  setMiningStatus: (v: any) => void;
  projectScope: string;
}) {
  const [messages, setMessages] = useState<Message[]>([{
    id: 'init', role: 'agent', ts: new Date().toISOString(),
    content: 'สวัสดีครับ ผมคือ UET Agent พร้อมช่วยวิเคราะห์ข้อมูลและคำนวณสมการ UET เพิ่ม Knowledge Sources ทางซ้ายเพื่อให้ผมอ่านก่อนเริ่มได้เลยครับ',
  }]);
  const [input, setInput] = useState('');
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [balance, setBalance] = useState(2500);
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => { endRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [messages]);

  const sourceTags = Array.from(new Set(sources.map(s => s.type)));
  const context = sources.map(s => s.content).join('\n\n');

  const handleTrain = async () => {
    if (!sources.length) {
      setMessages(prev => [...prev, { id: Date.now().toString(), role: 'system', ts: new Date().toISOString(), content: 'เพิ่ม Source ทางซ้ายก่อนนะครับ' }]);
      return;
    }
    setIsComputing(true);
    setMiningStatus({ status: 'Ingesting into UET Graph...', progress: 20 });
    try {
      const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
      const res = await fetch(`${AGENT_URL}/ingest`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...(token ? { Authorization: `Bearer ${token}` } : {}) },
        body: JSON.stringify({ doc_id: `session_${Date.now()}`, text: context, source_type: sources[0]?.type || 'text', project_scope: projectScope, doc_version: 'v1', tags: sourceTags, ingest_mode: 'manual' }),
      });
      if (!res.ok) throw new Error();
      setMiningStatus({ status: 'Knowledge stabilized', progress: 100 });
      setMessages(prev => [...prev, { id: Date.now().toString(), role: 'agent', ts: new Date().toISOString(), content: `เรียนรู้ ${sources.length} source(s) สำเร็จแล้วครับ! ตั้งคำถามได้เลย` }]);
    } catch {
      setMessages(prev => [...prev, { id: Date.now().toString(), role: 'system', ts: new Date().toISOString(), content: 'เชื่อมต่อ Agent ไม่ได้ (กำลัง offline) แต่ Sources บันทึกไว้แล้วในระบบ' }]);
    } finally {
      setIsComputing(false);
      setTimeout(() => setMiningStatus(null), 3000);
    }
  };

  const handleSend = async () => {
    if (!input.trim()) return;
    const userMsg: Message = { id: Date.now().toString(), role: 'user', ts: new Date().toISOString(), content: input.trim() };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsComputing(true);
    setMiningStatus({ status: 'Generating PoUW Task...', progress: 10 });

    try {
      setTimeout(() => setMiningStatus({ status: 'Calculating Equilibrium Path...', progress: 45 }), 500);
      setTimeout(() => setMiningStatus({ status: 'Verifying UET Matrix...', progress: 80 }), 1200);

      const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
      const res = await fetch(`${AGENT_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...(token ? { Authorization: `Bearer ${token}` } : {}) },
        body: JSON.stringify({
          prompt: userMsg.content, doc_context: context, session_id: sessionId,
          project_scope: projectScope, source_tags: sourceTags,
          model: selectedModel, system_prompt: systemPrompt,
          tools_enabled: Object.entries(tools).filter(([, v]) => v).map(([k]) => k),
        }),
      });
      if (!res.ok) throw new Error();
      const data = await res.json();
      if (data.session_id) setSessionId(data.session_id);

      const reward = data.work_computed || 0;
      setBalance(b => b + reward);
      setMiningStatus({ status: 'Mining Complete', progress: 100, reward });
      setMessages(prev => [...prev, { id: (Date.now() + 1).toString(), role: 'agent', ts: new Date().toISOString(), content: data.response, pouw: reward }]);
    } catch {
      setMessages(prev => [...prev, { id: (Date.now() + 1).toString(), role: 'system', ts: new Date().toISOString(), content: 'เกิดข้อผิดพลาด – Agent อาจ offline อยู่ครับ ลองใหม่อีกครั้ง' }]);
      setMiningStatus(null);
    } finally {
      setIsComputing(false);
      setTimeout(() => setMiningStatus(null), 4000);
    }
  };

  return (
    <div className="flex flex-col h-full bg-background">
      {/* ── Header ── */}
      <div className="px-4 py-2.5 border-b border-border bg-card flex items-center justify-between shrink-0">
        <h1 className="text-sm font-bold flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-purple-500" />
          UET WorkChat
        </h1>
        <div className="flex items-center gap-2">
          {/* Source count badge */}
          {sources.length > 0 && (
            <span className="text-[10px] bg-emerald-500/10 text-emerald-600 border border-emerald-500/20 px-2 py-0.5 rounded-full font-medium">
              {sources.length} source{sources.length > 1 ? 's' : ''} active
            </span>
          )}
          {/* Online pill */}
          <div className="flex items-center gap-1 text-[10px] text-muted-foreground bg-muted px-2 py-1 rounded-full">
            <Activity className="w-3 h-3 text-green-500" />
            <span>UET Engine</span>
          </div>
          {/* PoUW button */}
          <PoUWButton miningStatus={miningStatus} balance={balance} />
        </div>
      </div>

      {/* ── Messages ── */}
      <div className="flex-1 overflow-y-auto px-4 py-4 space-y-5">
        {messages.map(msg => (
          <div key={msg.id} className={`flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse ml-auto max-w-[80%]' : 'max-w-[80%]'}`}>
            {msg.role !== 'system' && (
              <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${
                msg.role === 'agent' ? 'bg-purple-100 text-purple-600' : 'bg-blue-100 text-blue-600'
              }`}>
                {msg.role === 'agent' ? <Bot className="w-4 h-4" /> : <User className="w-4 h-4" />}
              </div>
            )}
            <div className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
              <div className={`px-3.5 py-2.5 rounded-2xl text-sm whitespace-pre-wrap leading-relaxed ${
                msg.role === 'agent' ? 'bg-muted text-foreground rounded-tl-sm' :
                msg.role === 'user' ? 'bg-primary text-primary-foreground rounded-tr-sm' :
                'bg-amber-50 text-amber-700 border border-amber-200 rounded-xl text-xs italic'
              }`}>
                {msg.content}
              </div>
              <div className="flex items-center gap-2 mt-0.5 px-1">
                <span className="text-[9px] text-muted-foreground">
                  {new Date(msg.ts).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </span>
                {msg.pouw && msg.pouw > 0 && (
                  <span className="text-[9px] text-green-500 font-bold flex items-center gap-0.5">
                    <Coins size={8} /> +{msg.pouw.toFixed(3)}
                  </span>
                )}
              </div>
            </div>
          </div>
        ))}
        {isComputing && (
          <div className="flex gap-3 max-w-[80%]">
            <div className="w-8 h-8 rounded-full bg-purple-100 flex items-center justify-center shrink-0">
              <Bot className="w-4 h-4 text-purple-600" />
            </div>
            <div className="bg-muted rounded-2xl rounded-tl-sm px-4 py-3 flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-muted-foreground/40 animate-bounce [animation-delay:0ms]" />
              <span className="w-1.5 h-1.5 rounded-full bg-muted-foreground/40 animate-bounce [animation-delay:150ms]" />
              <span className="w-1.5 h-1.5 rounded-full bg-muted-foreground/40 animate-bounce [animation-delay:300ms]" />
            </div>
          </div>
        )}
        <div ref={endRef} />
      </div>

      {/* ── Input ── */}
      <div className="px-4 pb-4 pt-2 bg-card border-t border-border shrink-0">
        <div className="flex items-end gap-2">
          <textarea
            className="flex-1 bg-background border border-border rounded-xl px-3.5 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-primary/40 resize-none"
            style={{ minHeight: 44, maxHeight: 120 }}
            placeholder="ถามคำถาม, วิเคราะห์ข้อมูล, หรือคำนวณสมการ... (Enter ส่ง, Shift+Enter ขึ้นบรรทัด)"
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend(); } }}
            rows={1}
          />
          {/* Train button */}
          <button onClick={handleTrain} disabled={!sources.length || isComputing}
            className="w-10 h-10 flex items-center justify-center rounded-xl bg-emerald-500/10 text-emerald-600 hover:bg-emerald-500/20 disabled:opacity-40 transition-colors border border-emerald-500/20 shrink-0"
            title="เทรน AI ด้วย Sources ที่เพิ่มไว้"
          >
            {isComputing ? <Loader2 className="w-4 h-4 animate-spin" /> : <Bot className="w-4 h-4" />}
          </button>
          {/* Send button */}
          <button onClick={handleSend} disabled={!input.trim() || isComputing}
            className="w-10 h-10 flex items-center justify-center rounded-xl bg-primary text-primary-foreground hover:bg-primary/90 disabled:opacity-40 transition-colors shrink-0"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
        <p className="text-center mt-1.5 text-[9px] text-muted-foreground">
          🤖 = เทรน AI ด้วย Sources &nbsp;|&nbsp; 📤 = ส่งคำถาม &nbsp;|&nbsp; Model: <span className="text-primary font-medium">{MODELS.find(m => m.id === selectedModel)?.label}</span>
        </p>
      </div>
    </div>
  );
}

/* ══════════════════════════════════════════════════
   MAIN: WorkchatStudio — 2-panel layout
══════════════════════════════════════════════════ */
export interface WorkchatStudioProps {
  projectScope?: string;
}

export default function WorkchatStudio({ projectScope = 'workchat-local' }: WorkchatStudioProps) {
  const [sources, setSources] = useState<Source[]>([]);
  const [selectedModel, setSelectedModel] = useState(MODELS[0].id);
  const [systemPrompt, setSystemPrompt] = useState('คุณคือ UET Research Agent ผู้เชี่ยวชาญด้านฟิสิกส์เชิงทฤษฎีและระบบสมดุล ตอบด้วยภาษาไทย และอ้างอิงแหล่งข้อมูลที่ให้มาเสมอ');
  const [tools, setTools] = useState<Record<string, boolean>>(Object.fromEntries(TOOLS.map(t => [t.id, t.defaultOn])));
  const [isComputing, setIsComputing] = useState(false);
  const [miningStatus, setMiningStatus] = useState<any>(null);
  const [configCollapsed, setConfigCollapsed] = useState(false);

  const addSource = (s: Source) => setSources(prev => [...prev, s]);
  const removeSource = (id: string) => setSources(prev => prev.filter(s => s.id !== id));
  const toggleTool = (id: string) => setTools(prev => ({ ...prev, [id]: !prev[id] }));

  return (
    <div className="flex h-full w-full bg-background overflow-hidden">
      {/* ── LEFT: Agent Config panel (collapsible) ── */}
      <div className={`shrink-0 border-r border-border h-full flex flex-col transition-[width] duration-200 overflow-hidden ${configCollapsed ? 'w-0 border-0' : 'w-[300px]'}`}>
        {!configCollapsed && (
          <AgentConfigPanel
            sources={sources} onSourceAdd={addSource} onSourceRemove={removeSource}
            selectedModel={selectedModel} onModelChange={setSelectedModel}
            systemPrompt={systemPrompt} onPromptChange={setSystemPrompt}
            tools={tools} onToolToggle={toggleTool}
          />
        )}
      </div>

      {/* Collapse toggle */}
      <button
        onClick={() => setConfigCollapsed(v => !v)}
        className="shrink-0 w-4 flex items-center justify-center bg-muted/20 hover:bg-muted/60 border-r border-border transition-colors z-10"
        title={configCollapsed ? 'Show Agent Config' : 'Hide Agent Config'}
      >
        {configCollapsed ? <ChevronRight size={12} className="text-muted-foreground" /> : <ChevronLeft size={12} className="text-muted-foreground" />}
      </button>

      {/* ── RIGHT: Chat ── */}
      <div className="flex-1 min-w-0 h-full">
        <ChatArea
          sources={sources}
          selectedModel={selectedModel}
          systemPrompt={systemPrompt}
          tools={tools}
          isComputing={isComputing}
          setIsComputing={setIsComputing}
          miningStatus={miningStatus}
          setMiningStatus={setMiningStatus}
          projectScope={projectScope}
        />
      </div>
    </div>
  );
}
