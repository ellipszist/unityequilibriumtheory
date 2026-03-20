'use client';

import React, { useState } from 'react';
import { FileText, Plus, Database, AlignLeft } from 'lucide-react';

interface SourcePanelProps {
  sources: any[];
  onSourceAdd: (source: any) => void;
}

export default function SourcePanel({ sources, onSourceAdd }: SourcePanelProps) {
  const [inputText, setInputText] = useState('');

  const handleAddSource = () => {
    if (!inputText.trim()) return;
    onSourceAdd({
      id: Date.now().toString(),
      type: 'text',
      title: `Document ${sources.length + 1}`,
      content: inputText,
      createdAt: new Date().toISOString()
    });
    setInputText('');
  };

  return (
    <div className="flex flex-col h-full bg-muted/10">
      <div className="p-4 border-b border-border flex items-center justify-between">
        <h2 className="text-sm font-semibold flex items-center gap-2">
          <Database className="w-4 h-4 text-primary" />
          แหล่งข้อมูล (Sources)
        </h2>
        <span className="text-xs bg-muted px-2 py-1 rounded-full">{sources.length}</span>
      </div>

      {/* Source List */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {sources.length === 0 ? (
          <div className="text-center text-sm text-muted-foreground mt-10">
            ยังไม่มีข้อมูลนำเข้า<br/>
            เพิ่มข้อมูลเพื่อให้ UET Agent วิเคราะห์
          </div>
        ) : (
          sources.map((source) => (
            <div key={source.id} className="bg-card border border-border rounded-md p-3 hover:border-primary/50 transition-colors cursor-pointer shadow-sm group relative">
              <div className="flex items-center gap-2 mb-1">
                <FileText className="w-4 h-4 text-blue-500" />
                <span className="text-sm font-medium truncate">{source.title}</span>
              </div>
              <p className="text-xs text-muted-foreground line-clamp-2">{source.content}</p>
            </div>
          ))
        )}
      </div>

      {/* Add Source Input */}
      <div className="p-4 border-t border-border bg-card">
        <div className="mb-2 text-xs font-medium flex items-center gap-1 text-muted-foreground">
          <AlignLeft className="w-3 h-3" />
          เพิ่มข้อความดิบ (Raw Text)
        </div>
        <textarea
          className="w-full text-sm bg-background border border-border rounded-md p-2 h-24 resize-none focus:outline-none focus:ring-1 focus:ring-primary mb-2"
          placeholder="วางเนื้อหาทฤษฎี บทความ หรือข้อมูลตัวเลขที่นี่..."
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
        />
        <button 
          onClick={handleAddSource}
          disabled={!inputText.trim()}
          className="w-full bg-primary text-primary-foreground hover:bg-primary/90 disabled:opacity-50 text-sm py-2 rounded-md font-medium transition-colors flex items-center justify-center gap-2"
        >
          <Plus className="w-4 h-4" />
          เพิ่มเข้าสู่ระบบวิเคราะห์
        </button>
      </div>
    </div>
  );
}
