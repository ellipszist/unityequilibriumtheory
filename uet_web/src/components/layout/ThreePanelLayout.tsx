'use client';

import { ReactNode, useState } from 'react';
import PanelContainer from './PanelContainer';

interface ThreePanelLayoutProps {
  left: ReactNode;
  center: ReactNode;
  right: ReactNode;
  leftTitle?: string;
  rightTitle?: string;
  leftIcon?: ReactNode;
  rightIcon?: ReactNode;
  leftDefaultWidth?: number;
  rightDefaultWidth?: number;
  leftCollapsed?: boolean;
  rightCollapsed?: boolean;
  className?: string;
}

export default function ThreePanelLayout({
  left,
  center,
  right,
  leftTitle,
  rightTitle,
  leftIcon,
  rightIcon,
  leftDefaultWidth = 280,
  rightDefaultWidth = 300,
  leftCollapsed = false,
  rightCollapsed = false,
  className = '',
}: ThreePanelLayoutProps) {
  const [mobilePanel, setMobilePanel] = useState<'left' | 'center' | 'right'>('center');

  return (
    <>
      {/* Desktop/Tablet: side-by-side panels */}
      <div className={`hidden md:flex h-[calc(100vh-56px)] overflow-hidden ${className}`}>
        <PanelContainer
          side="left"
          defaultWidth={leftDefaultWidth}
          minWidth={200}
          maxWidth={400}
          defaultCollapsed={leftCollapsed}
          title={leftTitle}
          icon={leftIcon}
          className="border-r border-border bg-muted/20"
        >
          <div className="h-full overflow-y-auto">{left}</div>
        </PanelContainer>

        <PanelContainer side="center">
          <div className="h-full overflow-y-auto">{center}</div>
        </PanelContainer>

        <PanelContainer
          side="right"
          defaultWidth={rightDefaultWidth}
          minWidth={200}
          maxWidth={420}
          defaultCollapsed={rightCollapsed}
          title={rightTitle}
          icon={rightIcon}
          className="border-l border-border bg-muted/20"
        >
          <div className="h-full overflow-y-auto">{right}</div>
        </PanelContainer>
      </div>

      {/* Mobile: single panel + bottom tab bar */}
      <div className="md:hidden flex flex-col h-[calc(100vh-56px)]">
        <div className="flex-1 overflow-y-auto">
          {mobilePanel === 'left' && left}
          {mobilePanel === 'center' && center}
          {mobilePanel === 'right' && right}
        </div>

        {/* Bottom tab bar */}
        <div className="shrink-0 flex border-t border-border bg-card">
          {([
            { key: 'left' as const, label: leftTitle || 'Left' },
            { key: 'center' as const, label: 'Main' },
            { key: 'right' as const, label: rightTitle || 'Right' },
          ]).map(tab => (
            <button
              key={tab.key}
              onClick={() => setMobilePanel(tab.key)}
              className={`flex-1 py-3 text-xs font-medium transition-colors ${
                mobilePanel === tab.key
                  ? 'text-primary border-t-2 border-primary bg-primary/5'
                  : 'text-muted-foreground'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>
    </>
  );
}
