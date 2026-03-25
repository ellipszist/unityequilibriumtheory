'use client';

import React, { useState } from 'react';
import { Cpu, Zap, Activity, Coins, CheckCircle2, Settings2, Wrench, ChevronDown, ChevronUp, ToggleLeft, ToggleRight, Bot, Sparkles } from 'lucide-react';

interface OutputPanelProps {
  isComputing: boolean;
  miningStatus: any;
}

const MODELS = [
  { id: 'glm-4.7-flash', label: 'GLM 4.7 Flash', badge: 'Fast', color: 'text-emerald-500' },
  { id: 'qwen-2.5-7b', label: 'Qwen 2.5 7B', badge: 'Balanced', color: 'text-blue-500' },
  { id: 'uet-local', label: 'UET Local', badge: 'Research', color: 'text-purple-500' },
];

const TOOLS = [
  { id: 'rag', label: 'RAG Search', desc: 'ค้นหาจาก Sources ที่เพิ่มไว้', defaultOn: true },
  { id: 'pouw', label: 'PoUW Mining', desc: 'คำนวณสมการ UET ขณะตอบ', defaultOn: true },
  { id: 'web', label: 'Web Search', desc: 'ค้นหาข้อมูลเพิ่มเติมจากอินเทอร์เน็ต', defaultOn: false },
  { id: 'code', label: 'Code Executor', desc: 'รันโค้ด Python แบบ Sandbox', defaultOn: false },
];

export default function OutputPanel({ isComputing, miningStatus }: OutputPanelProps) {
  const [selectedModel, setSelectedModel] = useState(MODELS[0].id);
  const [systemPrompt, setSystemPrompt] = useState(
    'คุณคือ UET Research Agent ผู้เชี่ยวชาญด้านฟิสิกส์เชิงทฤษฎีและระบบสมดุล ตอบด้วยภาษาไทย และอ้างอิงแหล่งข้อมูลที่ให้มาเสมอ'
  );
  const [tools, setTools] = useState<Record<string, boolean>>(
    Object.fromEntries(TOOLS.map(t => [t.id, t.defaultOn]))
  );
  const [showPromptSection, setShowPromptSection] = useState(true);
  const [showToolsSection, setShowToolsSection] = useState(true);
  const [showStatusSection, setShowStatusSection] = useState(true);

  const toggleTool = (id: string) => setTools(prev => ({ ...prev, [id]: !prev[id] }));

  return (
    <div className="flex flex-col h-full bg-background">
      {/* Header */}
      <div className="px-4 pt-4 pb-3 border-b border-border shrink-0">
        <h2 className="text-sm font-semibold flex items-center gap-2">
          <Settings2 className="w-4 h-4 text-primary" />
          Agent Studio
        </h2>
        <p className="text-[10px] text-muted-foreground mt-0.5">ตั้งค่า Agent ที่จะใช้ในการวิเคราะห์</p>
      </div>

      <div className="flex-1 overflow-y-auto">

        {/* Model Picker */}
        <div className="px-3 py-3 border-b border-border/60">
          <p className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider mb-2">โมเดล AI</p>
          <div className="space-y-1">
            {MODELS.map(m => (
              <button
                key={m.id}
                onClick={() => setSelectedModel(m.id)}
                className={`w-full flex items-center justify-between px-3 py-2 rounded-lg text-xs transition-all ${
                  selectedModel === m.id
                    ? 'bg-primary/10 border border-primary/30 text-foreground'
                    : 'bg-muted/30 border border-transparent hover:border-border text-muted-foreground'
                }`}
              >
                <div className="flex items-center gap-2">
                  <Bot className={`w-3.5 h-3.5 ${selectedModel === m.id ? 'text-primary' : 'text-muted-foreground'}`} />
                  <span className="font-medium">{m.label}</span>
                </div>
                <span className={`text-[9px] px-1.5 py-0.5 rounded-full bg-muted font-medium ${m.color}`}>{m.badge}</span>
              </button>
            ))}
          </div>
        </div>

        {/* System Prompt */}
        <div className="border-b border-border/60">
          <button
            onClick={() => setShowPromptSection(v => !v)}
            className="w-full flex items-center justify-between px-3 py-2.5 text-[10px] font-semibold text-muted-foreground uppercase tracking-wider hover:text-foreground transition-colors"
          >
            <div className="flex items-center gap-1.5">
              <Sparkles className="w-3 h-3" /> System Prompt
            </div>
            {showPromptSection ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
          </button>
          {showPromptSection && (
            <div className="px-3 pb-3">
              <textarea
                value={systemPrompt}
                onChange={e => setSystemPrompt(e.target.value)}
                rows={5}
                className="w-full text-[11px] bg-muted/30 border border-border rounded-lg p-2.5 resize-none focus:outline-none focus:ring-1 focus:ring-primary leading-relaxed"
                placeholder="กำหนดบุคลิก ขอบเขต และพฤติกรรมของ Agent..."
              />
              <p className="text-[9px] text-muted-foreground mt-1">{systemPrompt.length} ตัวอักษร</p>
            </div>
          )}
        </div>

        {/* Tools */}
        <div className="border-b border-border/60">
          <button
            onClick={() => setShowToolsSection(v => !v)}
            className="w-full flex items-center justify-between px-3 py-2.5 text-[10px] font-semibold text-muted-foreground uppercase tracking-wider hover:text-foreground transition-colors"
          >
            <div className="flex items-center gap-1.5">
              <Wrench className="w-3 h-3" /> เครื่องมือ (Tools)
            </div>
            {showToolsSection ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
          </button>
          {showToolsSection && (
            <div className="px-3 pb-3 space-y-2">
              {TOOLS.map(tool => (
                <div key={tool.id} className="flex items-start justify-between gap-2">
                  <div className="flex-1 min-w-0">
                    <p className="text-[11px] font-medium">{tool.label}</p>
                    <p className="text-[10px] text-muted-foreground">{tool.desc}</p>
                  </div>
                  <button
                    onClick={() => toggleTool(tool.id)}
                    className="shrink-0 mt-0.5"
                  >
                    {tools[tool.id]
                      ? <ToggleRight className="w-5 h-5 text-primary" />
                      : <ToggleLeft className="w-5 h-5 text-muted-foreground" />
                    }
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* PoUW Status */}
        <div className="border-b border-border/60">
          <button
            onClick={() => setShowStatusSection(v => !v)}
            className="w-full flex items-center justify-between px-3 py-2.5 text-[10px] font-semibold text-muted-foreground uppercase tracking-wider hover:text-foreground transition-colors"
          >
            <div className="flex items-center gap-1.5">
              <Activity className="w-3 h-3" /> PoUW Status
            </div>
            <div className="flex items-center gap-1.5">
              <span className="relative flex h-1.5 w-1.5">
                {isComputing && <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75" />}
                <span className={`relative inline-flex rounded-full h-1.5 w-1.5 ${isComputing ? 'bg-green-500' : 'bg-muted-foreground/40'}`} />
              </span>
              {showStatusSection ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
            </div>
          </button>
          {showStatusSection && (
            <div className="px-3 pb-3">
              <div className="rounded-xl bg-muted/30 border border-border p-3">
                {isComputing ? (
                  <div className="space-y-3">
                    <div className="flex items-center gap-2">
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary shrink-0" />
                      <span className="text-xs font-medium">{miningStatus?.status || 'Processing…'}</span>
                    </div>
                    <div className="h-1.5 w-full bg-muted rounded-full overflow-hidden">
                      <div
                        className="h-full bg-primary transition-all duration-300 ease-out"
                        style={{ width: `${miningStatus?.progress ?? 0}%` }}
                      />
                    </div>
                    <p className="text-[10px] text-muted-foreground text-right">{miningStatus?.progress ?? 0}%</p>
                  </div>
                ) : miningStatus?.reward ? (
                  <div className="flex items-center gap-3">
                    <CheckCircle2 className="w-6 h-6 text-green-500 shrink-0" />
                    <div>
                      <p className="text-xs font-semibold">สมดุลสำเร็จ</p>
                      <p className="text-[10px] text-muted-foreground flex items-center gap-1">
                        <Zap className="w-3 h-3 text-yellow-500" />
                        {miningStatus.reward.toFixed(4)} Ω generated
                      </p>
                    </div>
                  </div>
                ) : (
                  <div className="flex items-center gap-2 text-muted-foreground/50">
                    <Cpu className="w-4 h-4" />
                    <span className="text-xs">Idle — รอคำสั่ง</span>
                  </div>
                )}
              </div>

              {miningStatus?.sessionId && (
                <div className="mt-2 space-y-1">
                  {[
                    ['Task Type', miningStatus.taskType],
                    ['Path Strategy', miningStatus.pathStrategy],
                    ['Session', miningStatus.sessionId?.slice(0, 12) + '…'],
                    ['Evidence Chunks', miningStatus.debug?.semantic_bundle?.total_chunk_count],
                  ].map(([k, v]) => v ? (
                    <div key={String(k)} className="flex justify-between text-[10px]">
                      <span className="text-muted-foreground">{k}</span>
                      <span className="font-mono">{String(v)}</span>
                    </div>
                  ) : null)}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Balance quick-view */}
        <div className="px-3 py-3">
          <p className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider mb-2">ยอดคงเหลือ</p>
          <div className="rounded-xl bg-gradient-to-br from-primary/10 to-purple-500/5 border border-primary/20 px-4 py-3 flex items-center justify-between">
            <div>
              <p className="text-xl font-bold">1,450</p>
              <p className="text-[10px] text-muted-foreground flex items-center gap-1">
                <Coins className="w-3 h-3 text-primary" /> UET Credits
              </p>
            </div>
            <div className="flex flex-col gap-1">
              <button className="text-[10px] bg-primary/20 text-primary px-2.5 py-1 rounded-lg hover:bg-primary/30 transition-colors font-medium">Stake</button>
              <button className="text-[10px] bg-muted text-muted-foreground px-2.5 py-1 rounded-lg hover:bg-muted/80 transition-colors font-medium">History</button>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
