'use client';

import React from 'react';
import { Cpu, Zap, Activity, Coins, CheckCircle2 } from 'lucide-react';

interface OutputPanelProps {
  isComputing: boolean;
  miningStatus: any;
}

export default function OutputPanel({ isComputing, miningStatus }: OutputPanelProps) {
  return (
    <div className="flex flex-col h-full bg-background">
      <div className="p-4 border-b border-border">
        <h2 className="text-sm font-semibold flex items-center gap-2">
          <Activity className="w-4 h-4 text-primary" />
          สถานะระบบ (Dashboard)
        </h2>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        
        {/* Computing Status Widget */}
        <div className="bg-card border border-border rounded-xl overflow-hidden">
          <div className="bg-muted/50 p-3 border-b border-border flex items-center justify-between">
            <span className="text-xs font-semibold">PoUW Mining Node</span>
            <div className="flex items-center gap-1.5">
              <span className="relative flex h-2 w-2">
                {isComputing && <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>}
                <span className={`relative inline-flex rounded-full h-2 w-2 ${isComputing ? 'bg-green-500' : 'bg-gray-400'}`}></span>
              </span>
              <span className="text-[10px] text-muted-foreground uppercase">{isComputing ? 'PROCESSING' : 'IDLE'}</span>
            </div>
          </div>
          
          <div className="p-4 flex flex-col items-center justify-center min-h-[120px]">
            {isComputing ? (
              <div className="w-full space-y-4">
                <div className="flex justify-center">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
                </div>
                {miningStatus && (
                  <div className="space-y-2 w-full">
                    <div className="flex justify-between text-xs text-muted-foreground">
                      <span>{miningStatus.status}</span>
                      <span>{miningStatus.progress}%</span>
                    </div>
                    <div className="h-1.5 w-full bg-muted rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-primary transition-all duration-300 ease-out"
                        style={{ width: `${miningStatus.progress}%` }}
                      />
                    </div>
                  </div>
                )}
              </div>
            ) : miningStatus?.reward ? (
              <div className="text-center space-y-2">
                <CheckCircle2 className="w-8 h-8 text-green-500 mx-auto" />
                <div className="text-sm font-medium">สมการสมดุลสำเร็จ</div>
                <div className="text-xs text-muted-foreground flex items-center justify-center gap-1">
                  <Zap className="w-3 h-3 text-yellow-500" />
                  Work Generated: {miningStatus.reward.toFixed(4)} Ω
                </div>
              </div>
            ) : (
              <div className="text-center text-muted-foreground">
                <Cpu className="w-8 h-8 mx-auto mb-2 opacity-20" />
                <span className="text-sm">รอคำสั่งการคำนวณ</span>
              </div>
            )}
          </div>
        </div>

        {/* Token Balance Widget */}
        <div className="bg-card border border-border rounded-xl p-4">
          <h3 className="text-xs font-semibold text-muted-foreground mb-3 uppercase tracking-wider">Your Balance</h3>
          <div className="flex items-end gap-2">
            <span className="text-3xl font-bold tracking-tight">1,450</span>
            <span className="text-sm text-primary font-medium mb-1 flex items-center gap-1">
              <Coins className="w-4 h-4" />
              UET
            </span>
          </div>
          <div className="mt-4 flex gap-2">
            <button className="flex-1 bg-secondary text-secondary-foreground hover:bg-secondary/80 text-xs py-2 rounded-md font-medium transition-colors">
              Stake Power
            </button>
            <button className="flex-1 bg-secondary text-secondary-foreground hover:bg-secondary/80 text-xs py-2 rounded-md font-medium transition-colors">
              History
            </button>
          </div>
        </div>

        {miningStatus?.sessionId && (
          <div className="bg-card border border-border rounded-xl p-4 space-y-3">
            <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Developer Debug</h3>
            <div className="space-y-2 text-xs">
              <div className="flex justify-between gap-2">
                <span className="text-muted-foreground">Session</span>
                <span className="text-right break-all">{miningStatus.sessionId}</span>
              </div>
              <div className="flex justify-between gap-2">
                <span className="text-muted-foreground">Task Type</span>
                <span>{miningStatus.taskType || '-'}</span>
              </div>
              <div className="flex justify-between gap-2">
                <span className="text-muted-foreground">Path Strategy</span>
                <span>{miningStatus.pathStrategy || '-'}</span>
              </div>
              <div className="flex justify-between gap-2">
                <span className="text-muted-foreground">Active Sources</span>
                <span>{String(miningStatus.debug?.working_memory?.active_source_count ?? '-')}</span>
              </div>
              <div className="flex justify-between gap-2">
                <span className="text-muted-foreground">Evidence Chunks</span>
                <span>{String(miningStatus.debug?.semantic_bundle?.total_chunk_count ?? '-')}</span>
              </div>
              <div className="flex justify-between gap-2">
                <span className="text-muted-foreground">Persistent Chunks</span>
                <span>{String(miningStatus.debug?.semantic_bundle?.persistent_chunk_count ?? '-')}</span>
              </div>
              <div className="flex justify-between gap-2">
                <span className="text-muted-foreground">Temporary Chunks</span>
                <span>{String(miningStatus.debug?.semantic_bundle?.temporary_chunk_count ?? '-')}</span>
              </div>
            </div>
          </div>
        )}

      </div>
    </div>
  );
}
