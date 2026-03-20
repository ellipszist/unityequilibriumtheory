'use client';

import { ReactNode, useState } from 'react';
import { PanelLeftClose, PanelLeftOpen } from 'lucide-react';

interface SidebarLayoutProps {
  sidebar: ReactNode;
  children: ReactNode;
  sidebarWidth?: number;
  collapsedWidth?: number;
  defaultCollapsed?: boolean;
  className?: string;
}

export default function SidebarLayout({
  sidebar,
  children,
  sidebarWidth = 240,
  collapsedWidth = 48,
  defaultCollapsed = false,
  className = '',
}: SidebarLayoutProps) {
  const [collapsed, setCollapsed] = useState(defaultCollapsed);
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <div className={`flex h-[calc(100vh-56px)] overflow-hidden ${className}`}>
      {/* Desktop sidebar */}
      <aside
        className={`hidden md:flex flex-col shrink-0 border-r border-border bg-muted/20 transition-[width] duration-200 overflow-hidden`}
        style={{ width: collapsed ? collapsedWidth : sidebarWidth }}
      >
        {/* Toggle */}
        <div className={`flex items-center ${collapsed ? 'justify-center' : 'justify-end'} p-2`}>
          <button
            onClick={() => setCollapsed(!collapsed)}
            className="p-1.5 rounded-lg hover:bg-muted text-muted-foreground hover:text-foreground transition-colors"
          >
            {collapsed ? <PanelLeftOpen size={16} /> : <PanelLeftClose size={16} />}
          </button>
        </div>

        {/* Sidebar content */}
        <div className={`flex-1 overflow-y-auto ${collapsed ? 'opacity-0 pointer-events-none' : ''}`}>
          {sidebar}
        </div>
      </aside>

      {/* Mobile sidebar overlay */}
      {mobileOpen && (
        <div className="md:hidden fixed inset-0 z-40">
          <div className="absolute inset-0 bg-black/50" onClick={() => setMobileOpen(false)} />
          <aside className="absolute left-0 top-0 bottom-0 w-72 bg-card border-r border-border overflow-y-auto z-50 animate-in slide-in-from-left">
            {sidebar}
          </aside>
        </div>
      )}

      {/* Mobile toggle */}
      <button
        onClick={() => setMobileOpen(true)}
        className="md:hidden fixed bottom-4 left-4 z-30 w-10 h-10 rounded-full bg-primary text-primary-foreground shadow-lg flex items-center justify-center"
      >
        <PanelLeftOpen size={18} />
      </button>

      {/* Main content */}
      <main className="flex-1 overflow-y-auto">
        {children}
      </main>
    </div>
  );
}
