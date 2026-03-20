'use client';

import { useState, useRef, useCallback, ReactNode } from 'react';
import { ChevronLeft, ChevronRight, GripVertical } from 'lucide-react';

interface PanelContainerProps {
  children: ReactNode;
  side: 'left' | 'right' | 'center';
  defaultWidth?: number;
  minWidth?: number;
  maxWidth?: number;
  collapsible?: boolean;
  defaultCollapsed?: boolean;
  collapsedWidth?: number;
  className?: string;
  title?: string;
  icon?: ReactNode;
}

export default function PanelContainer({
  children,
  side,
  defaultWidth = 300,
  minWidth = 200,
  maxWidth = 500,
  collapsible = true,
  defaultCollapsed = false,
  collapsedWidth = 48,
  className = '',
  title,
  icon,
}: PanelContainerProps) {
  const [collapsed, setCollapsed] = useState(defaultCollapsed);
  const [width, setWidth] = useState(defaultWidth);
  const [isResizing, setIsResizing] = useState(false);
  const panelRef = useRef<HTMLDivElement>(null);

  const handleMouseDown = useCallback((e: React.MouseEvent) => {
    e.preventDefault();
    setIsResizing(true);
    const startX = e.clientX;
    const startWidth = width;

    const handleMouseMove = (e: MouseEvent) => {
      const delta = side === 'left' ? e.clientX - startX : startX - e.clientX;
      const newWidth = Math.max(minWidth, Math.min(maxWidth, startWidth + delta));
      setWidth(newWidth);
    };

    const handleMouseUp = () => {
      setIsResizing(false);
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
      document.body.style.cursor = '';
      document.body.style.userSelect = '';
    };

    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);
    document.body.style.cursor = 'col-resize';
    document.body.style.userSelect = 'none';
  }, [width, side, minWidth, maxWidth]);

  if (side === 'center') {
    return (
      <div className={`flex-1 min-w-0 overflow-hidden ${className}`}>
        {children}
      </div>
    );
  }

  const currentWidth = collapsed ? collapsedWidth : width;

  return (
    <div
      ref={panelRef}
      className={`relative shrink-0 flex transition-[width] duration-200 ${isResizing ? '!transition-none' : ''} ${className}`}
      style={{ width: currentWidth }}
    >
      {/* Panel content */}
      <div className={`flex-1 overflow-hidden ${collapsed ? 'opacity-0 pointer-events-none' : ''}`}>
        {children}
      </div>

      {/* Collapsed state — icon strip */}
      {collapsed && collapsible && (
        <div className="absolute inset-0 flex flex-col items-center pt-3 gap-2">
          {icon && <div className="text-muted-foreground">{icon}</div>}
          <button
            onClick={() => setCollapsed(false)}
            className="p-1.5 rounded-lg hover:bg-muted text-muted-foreground hover:text-foreground transition-colors"
            title={`Expand ${title || 'panel'}`}
          >
            {side === 'left' ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
          </button>
        </div>
      )}

      {/* Collapse button (when expanded) */}
      {!collapsed && collapsible && (
        <button
          onClick={() => setCollapsed(true)}
          className={`absolute top-3 ${side === 'left' ? '-right-3' : '-left-3'} z-10 w-6 h-6 rounded-full bg-card border border-border shadow-sm flex items-center justify-center text-muted-foreground hover:text-foreground hover:bg-muted transition-colors`}
          title={`Collapse ${title || 'panel'}`}
        >
          {side === 'left' ? <ChevronLeft size={12} /> : <ChevronRight size={12} />}
        </button>
      )}

      {/* Resize handle */}
      {!collapsed && (
        <div
          onMouseDown={handleMouseDown}
          className={`absolute top-0 bottom-0 w-1 cursor-col-resize group hover:bg-primary/30 transition-colors z-10 ${
            side === 'left' ? 'right-0' : 'left-0'
          }`}
        >
          <div className="absolute top-1/2 -translate-y-1/2 left-1/2 -translate-x-1/2 opacity-0 group-hover:opacity-100 transition-opacity">
            <GripVertical size={12} className="text-muted-foreground" />
          </div>
        </div>
      )}
    </div>
  );
}
