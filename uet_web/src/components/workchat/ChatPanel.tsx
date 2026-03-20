'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Sparkles, Activity } from 'lucide-react';

interface Message {
  id: string;
  role: 'user' | 'agent' | 'system';
  content: string;
  timestamp: string;
}

const AGENT_URL = process.env.NEXT_PUBLIC_AGENT_URL || 'http://localhost:8001';

interface ChatPanelProps {
  activeSources: any[];
  setIsComputing: (state: boolean) => void;
  setMiningStatus: (status: any) => void;
}

interface ChatResponse {
  response: string;
  equilibrium_data: Record<string, unknown>;
  work_computed: number;
  task_type?: string;
  session_id?: string;
}

interface DebugSessionResponse {
  session_id: string;
  working_memory: Record<string, unknown>;
  recent_episodes: Array<Record<string, unknown>>;
  semantic_bundle: Record<string, unknown>;
}

export default function ChatPanel({ activeSources, setIsComputing, setMiningStatus }: ChatPanelProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'init',
      role: 'agent',
      content: 'สวัสดีครับ ผมคือ UET Agent พร้อมช่วยคุณวิเคราะห์ข้อมูลและคำนวณสมการฟิสิกส์ โปรดเพิ่มแหล่งข้อมูลที่แถบด้านซ้ายก่อนเริ่มใช้งานครับ',
      timestamp: new Date().toISOString()
    }
  ]);
  const [input, setInput] = useState('');
  const [sessionId, setSessionId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const projectScope = 'workchat-local';
  const sourceTags = Array.from(new Set(activeSources.map(source => source.type || 'text')));

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleTrain = async () => {
    if (activeSources.length === 0) {
      setMessages(prev => [...prev, {
        id: Date.now().toString(),
        role: 'system',
        content: 'กรุณาเพิ่มแหล่งข้อมูล (Source) ด้านซ้ายมืออย่างน้อย 1 รายการก่อนทำการเทรนโมเดล',
        timestamp: new Date().toISOString()
      }]);
      return;
    }

    setIsComputing(true);
    setMiningStatus({ status: 'Ingesting knowledge into UET Graph...', progress: 20 });

    try {
      const context = activeSources.map(s => s.content).join('\n\n');
      
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${AGENT_URL}/ingest`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { 'Authorization': `Bearer ${token}` } : {})
        },
        body: JSON.stringify({
          doc_id: `Session_${Date.now()}`,
          text: context,
          source_type: activeSources[0]?.type || 'text',
          project_scope: projectScope,
          doc_version: 'v1',
          tags: sourceTags,
          ingest_mode: 'manual'
        })
      });

      if (!response.ok) throw new Error('Training failed');

      setMiningStatus({ status: 'Knowledge graph stabilized', progress: 100 });
      
      setMessages(prev => [...prev, {
        id: Date.now().toString(),
        role: 'agent',
        content: 'เรียนรู้ข้อมูลสำเร็จแล้ว! ตอนนี้ระบบมีฐานความรู้ใหม่เพิ่มเข้ามาในสมการ UET เรียบร้อย คุณสามารถลองตั้งคำถามหรือให้วิเคราะห์ได้เลยครับ',
        timestamp: new Date().toISOString()
      }]);

    } catch (error) {
      console.error(error);
      setMessages(prev => [...prev, {
        id: Date.now().toString(),
        role: 'system',
        content: 'เกิดข้อผิดพลาดในการเทรนโมเดล กรุณาลองใหม่',
        timestamp: new Date().toISOString()
      }]);
    } finally {
      setIsComputing(false);
      setTimeout(() => setMiningStatus(null), 3000);
    }
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input.trim(),
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsComputing(true);
    setMiningStatus({ status: 'Generating PoUW Task...', progress: 10 });

    try {
      // Create combined context from all active sources
      const context = activeSources.map(s => s.content).join('\n\n');
      
      // Simulate mining progression
      setTimeout(() => setMiningStatus({ status: 'Calculating Equilibrium Path...', progress: 40 }), 500);
      setTimeout(() => setMiningStatus({ status: 'Verifying Matrix...', progress: 80 }), 1500);

      // Call Python Semantic Engine directly (bypassing Rust for local dev)
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${AGENT_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { 'Authorization': `Bearer ${token}` } : {})
        },
        body: JSON.stringify({
          prompt: userMessage.content,
          doc_context: context,
          session_id: sessionId,
          project_scope: projectScope,
          source_tags: sourceTags
        })
      });

      if (!response.ok) {
        throw new Error('Failed to compute');
      }

      const data: ChatResponse = await response.json();

      if (data.session_id) {
        setSessionId(data.session_id);
      }

      let debugSession: DebugSessionResponse | null = null;
      if (data.session_id) {
        const debugResponse = await fetch(`${AGENT_URL}/debug/session/${data.session_id}`);
        if (debugResponse.ok) {
          debugSession = await debugResponse.json();
        }
      }

      setMiningStatus({
        status: 'Mining Complete',
        progress: 100,
        reward: data.work_computed,
        taskType: data.task_type,
        sessionId: data.session_id,
        pathStrategy: data.equilibrium_data?.path_strategy,
        debug: debugSession
      });

      setMessages(prev => [...prev, {
        id: (Date.now() + 1).toString(),
        role: 'agent',
        content: data.response,
        timestamp: new Date().toISOString()
      }]);

    } catch (error) {
      console.error(error);
      setMessages(prev => [...prev, {
        id: (Date.now() + 1).toString(),
        role: 'system',
        content: 'เกิดข้อผิดพลาดในการเชื่อมต่อกับ UET Core กรุณาลองใหม่อีกครั้ง',
        timestamp: new Date().toISOString()
      }]);
      setMiningStatus(null);
    } finally {
      setIsComputing(false);
      setTimeout(() => setMiningStatus(null), 3000); // Clear status after 3s
    }
  };

  return (
    <div className="flex flex-col h-full bg-background relative">
      {/* Header */}
      <div className="p-4 border-b border-border bg-card flex items-center justify-between">
        <h1 className="text-lg font-bold flex items-center gap-2">
          <Sparkles className="w-5 h-5 text-purple-500" />
          Studio Workchat
        </h1>
        <div className="flex items-center gap-2 text-xs text-muted-foreground bg-muted px-3 py-1.5 rounded-full">
          <Activity className="w-3 h-3 text-green-500" />
          <span>UET Engine Online</span>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {messages.map(msg => (
          <div key={msg.id} className={`flex gap-3 max-w-[85%] ${msg.role === 'user' ? 'ml-auto flex-row-reverse' : ''}`}>
            {/* Avatar */}
            <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${
              msg.role === 'agent' ? 'bg-purple-100 text-purple-600' :
              msg.role === 'user' ? 'bg-blue-100 text-blue-600' :
              'bg-red-100 text-red-600'
            }`}>
              {msg.role === 'agent' ? <Bot className="w-4 h-4" /> : 
               msg.role === 'user' ? <User className="w-4 h-4" /> : 
               <span className="text-xs font-bold">!</span>}
            </div>
            
            {/* Bubble */}
            <div className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
              <div className={`p-3 rounded-2xl text-sm whitespace-pre-wrap ${
                msg.role === 'agent' ? 'bg-muted text-foreground rounded-tl-sm' :
                msg.role === 'user' ? 'bg-primary text-primary-foreground rounded-tr-sm' :
                'bg-red-50 text-red-600 border border-red-200'
              }`}>
                {msg.content}
              </div>
              <span className="text-[10px] text-muted-foreground mt-1 px-1">
                {new Date(msg.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
              </span>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-4 bg-card border-t border-border">
        <div className="relative">
          <textarea
            className="w-full bg-background border border-border rounded-xl pl-4 pr-12 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50 resize-none h-14"
            placeholder="ถามคำถาม, ให้วิเคราะห์ข้อมูล, หรือสั่งคำนวณสมการ..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
          />
          <button 
            onClick={handleTrain}
            disabled={!activeSources.length}
            className="absolute right-12 top-2 bottom-2 aspect-square flex items-center justify-center bg-green-500/20 text-green-500 rounded-lg hover:bg-green-500/30 disabled:opacity-50 transition-colors"
            title="เทรน AI ด้วย UET Equation"
          >
            <Bot className="w-4 h-4" />
          </button>
          <button 
            onClick={handleSend}
            disabled={!input.trim()}
            className="absolute right-2 top-2 bottom-2 aspect-square flex items-center justify-center bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 disabled:opacity-50 transition-colors"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
        <div className="text-center mt-2 text-[10px] text-muted-foreground flex items-center justify-center gap-2">
          <span>กด 🤖 เพื่อนำแหล่งข้อมูลไป <b>เทรน Custom AI (UET Equations)</b></span>
          <span className="text-border">|</span>
          <span>กด 📤 เพื่อส่งคำถามปกติ</span>
        </div>
      </div>
    </div>
  );
}
