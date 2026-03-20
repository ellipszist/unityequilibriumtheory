'use client';

import { useState, useRef, useEffect } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import {
  Settings, HelpCircle, Moon, MessageSquareWarning, LogOut,
  ArrowLeft, Globe, Shield, Lock, Activity, Palette, Keyboard,
  Accessibility, ChevronRight, User, CreditCard
} from 'lucide-react';

type SubMenu = null | 'settings' | 'help' | 'display';

export default function ProfilePopover() {
  const params = useParams();
  const locale = (params?.locale as string) || 'en';
  const [open, setOpen] = useState(false);
  const [subMenu, setSubMenu] = useState<SubMenu>(null);
  const [darkMode, setDarkMode] = useState<'off' | 'on' | 'auto'>('auto');
  const ref = useRef<HTMLDivElement>(null);

  const [userName, setUserName] = useState('User');
  const [userEmail, setUserEmail] = useState('');
  const [userInitials, setUserInitials] = useState('U');

  useEffect(() => {
    try {
      const stored = localStorage.getItem('user');
      if (stored) {
        const u = JSON.parse(stored);
        setUserName(u.display_name || u.name || u.email?.split('@')[0] || 'User');
        setUserEmail(u.email || '');
        setUserInitials((u.display_name || u.name || u.email)?.[0]?.toUpperCase() || 'U');
      }
    } catch {}
  }, []);

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setOpen(false);
        setSubMenu(null);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  function handleToggle() {
    setOpen(!open);
    setSubMenu(null);
  }

  function handleLogout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    window.location.href = '/';
  }

  function handleDarkMode(mode: 'off' | 'on' | 'auto') {
    setDarkMode(mode);
    if (mode === 'on') document.documentElement.classList.add('dark');
    else if (mode === 'off') document.documentElement.classList.remove('dark');
    else {
      if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
    }
  }

  const menuItemClass = "w-full flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-muted/60 transition-colors text-left";
  const iconBoxClass = "w-9 h-9 rounded-full bg-muted flex items-center justify-center shrink-0";

  return (
    <div ref={ref} className="relative">
      <button
        onClick={handleToggle}
        className="w-9 h-9 rounded-full bg-gradient-to-br from-[#0d7a5f] to-emerald-600 flex items-center justify-center text-white text-xs font-bold hover:opacity-90 transition-opacity ring-2 ring-transparent hover:ring-primary/30"
        title="Profile"
      >
        {userInitials}
      </button>

      {open && (
        <div className="absolute right-0 top-full mt-2 w-80 rounded-2xl border border-border bg-card shadow-2xl z-50 overflow-hidden">

          {/* ===== Main Menu ===== */}
          {subMenu === null && (
            <div className="p-2">
              {/* User profile card */}
              <div className="p-3 rounded-xl hover:bg-muted/40 transition-colors mb-1">
                <Link href={`/${locale}/account`} onClick={() => setOpen(false)} className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-gradient-to-br from-[#0d7a5f] to-emerald-600 flex items-center justify-center text-white font-bold text-sm shrink-0">
                    {userInitials}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="font-semibold text-sm truncate">{userName}</p>
                    {userEmail && <p className="text-xs text-muted-foreground truncate">{userEmail}</p>}
                  </div>
                </Link>
              </div>

              {/* View all profiles */}
              <Link
                href={`/${locale}/account`}
                onClick={() => setOpen(false)}
                className="flex items-center justify-center gap-2 w-full py-2 mb-2 rounded-lg bg-muted/40 hover:bg-muted/60 text-sm font-medium transition-colors"
              >
                <User size={15} />
                View Profile
              </Link>

              <div className="border-t border-border my-1" />

              {/* Menu items */}
              <button onClick={() => setSubMenu('settings')} className={menuItemClass}>
                <div className={iconBoxClass}><Settings size={18} /></div>
                <span className="flex-1 text-sm font-medium">Settings & Privacy</span>
                <ChevronRight size={16} className="text-muted-foreground" />
              </button>

              <button onClick={() => setSubMenu('help')} className={menuItemClass}>
                <div className={iconBoxClass}><HelpCircle size={18} /></div>
                <span className="flex-1 text-sm font-medium">Help & Support</span>
                <ChevronRight size={16} className="text-muted-foreground" />
              </button>

              <button onClick={() => setSubMenu('display')} className={menuItemClass}>
                <div className={iconBoxClass}><Moon size={18} /></div>
                <span className="flex-1 text-sm font-medium">Display & Accessibility</span>
                <ChevronRight size={16} className="text-muted-foreground" />
              </button>

              <button className={menuItemClass}>
                <div className={iconBoxClass}><MessageSquareWarning size={18} /></div>
                <span className="flex-1 text-sm font-medium">Give Feedback</span>
              </button>

              <Link href={`/${locale}/account/billing`} onClick={() => setOpen(false)} className={menuItemClass}>
                <div className={iconBoxClass}><CreditCard size={18} /></div>
                <span className="flex-1 text-sm font-medium">Credits & Billing</span>
              </Link>

              <div className="border-t border-border my-1" />

              <button onClick={handleLogout} className={menuItemClass}>
                <div className={iconBoxClass}><LogOut size={18} /></div>
                <span className="flex-1 text-sm font-medium">Log Out</span>
              </button>

              <p className="text-[10px] text-muted-foreground px-3 pt-2 pb-1">
                Privacy · Terms · Cookies · UET Platform © 2026
              </p>
            </div>
          )}

          {/* ===== Settings & Privacy Sub-Menu ===== */}
          {subMenu === 'settings' && (
            <div className="p-2">
              <div className="flex items-center gap-3 px-2 py-2 mb-1">
                <button onClick={() => setSubMenu(null)} className="p-1.5 rounded-full hover:bg-muted transition-colors">
                  <ArrowLeft size={18} />
                </button>
                <h3 className="text-lg font-bold">Settings & Privacy</h3>
              </div>

              <Link href={`/${locale}/account`} onClick={() => setOpen(false)} className={menuItemClass}>
                <div className={iconBoxClass}><Settings size={18} /></div>
                <span className="text-sm font-medium">Settings</span>
              </Link>
              <button className={menuItemClass}>
                <div className={iconBoxClass}><Globe size={18} /></div>
                <span className="flex-1 text-sm font-medium">Language</span>
                <ChevronRight size={16} className="text-muted-foreground" />
              </button>
              <button className={menuItemClass}>
                <div className={iconBoxClass}><Shield size={18} /></div>
                <span className="text-sm font-medium">Privacy Checkup</span>
              </button>
              <button className={menuItemClass}>
                <div className={iconBoxClass}><Lock size={18} /></div>
                <span className="text-sm font-medium">Privacy Center</span>
              </button>
              <button className={menuItemClass}>
                <div className={iconBoxClass}><Activity size={18} /></div>
                <span className="text-sm font-medium">Activity Log</span>
              </button>
            </div>
          )}

          {/* ===== Help & Support Sub-Menu ===== */}
          {subMenu === 'help' && (
            <div className="p-2">
              <div className="flex items-center gap-3 px-2 py-2 mb-1">
                <button onClick={() => setSubMenu(null)} className="p-1.5 rounded-full hover:bg-muted transition-colors">
                  <ArrowLeft size={18} />
                </button>
                <h3 className="text-lg font-bold">Help & Support</h3>
              </div>

              <Link href={`/${locale}/docs`} onClick={() => setOpen(false)} className={menuItemClass}>
                <div className={iconBoxClass}><HelpCircle size={18} /></div>
                <span className="text-sm font-medium">Help Center</span>
              </Link>
              <button className={menuItemClass}>
                <div className={iconBoxClass}><User size={18} /></div>
                <span className="text-sm font-medium">Account Status</span>
              </button>
              <button className={menuItemClass}>
                <div className={iconBoxClass}><MessageSquareWarning size={18} /></div>
                <span className="text-sm font-medium">Support Inbox</span>
              </button>
              <button className={menuItemClass}>
                <div className={iconBoxClass}><Shield size={18} /></div>
                <span className="text-sm font-medium">Report a Problem</span>
              </button>
            </div>
          )}

          {/* ===== Display & Accessibility Sub-Menu ===== */}
          {subMenu === 'display' && (
            <div className="p-2">
              <div className="flex items-center gap-3 px-2 py-2 mb-1">
                <button onClick={() => setSubMenu(null)} className="p-1.5 rounded-full hover:bg-muted transition-colors">
                  <ArrowLeft size={18} />
                </button>
                <h3 className="text-lg font-bold">Display & Accessibility</h3>
              </div>

              {/* Dark Mode */}
              <div className="px-3 py-2">
                <div className="flex items-center gap-3 mb-3">
                  <div className={iconBoxClass}><Moon size={18} /></div>
                  <div>
                    <p className="text-sm font-semibold">Dark Mode</p>
                    <p className="text-xs text-muted-foreground">Adjust the appearance to reduce glare and rest your eyes.</p>
                  </div>
                </div>
                <div className="space-y-1 ml-12">
                  {([
                    { value: 'off' as const, label: 'Off' },
                    { value: 'on' as const, label: 'On' },
                    { value: 'auto' as const, label: 'Automatic' },
                  ]).map(opt => (
                    <button
                      key={opt.value}
                      onClick={() => handleDarkMode(opt.value)}
                      className="w-full flex items-center justify-between px-3 py-2 rounded-lg hover:bg-muted/40 transition-colors"
                    >
                      <span className="text-sm">{opt.label}</span>
                      <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center ${
                        darkMode === opt.value ? 'border-primary bg-primary' : 'border-muted-foreground'
                      }`}>
                        {darkMode === opt.value && <div className="w-2 h-2 rounded-full bg-primary-foreground" />}
                      </div>
                    </button>
                  ))}
                  {darkMode === 'auto' && (
                    <p className="text-[10px] text-muted-foreground px-3 pt-1">
                      We will adjust the display based on your device's system settings automatically.
                    </p>
                  )}
                </div>
              </div>

              <div className="border-t border-border my-2" />

              <button className={menuItemClass}>
                <div className={iconBoxClass}><Keyboard size={18} /></div>
                <span className="flex-1 text-sm font-medium">Keyboard</span>
                <ChevronRight size={16} className="text-muted-foreground" />
              </button>
              <button className={menuItemClass}>
                <div className={iconBoxClass}><Accessibility size={18} /></div>
                <span className="text-sm font-medium">Accessibility Settings</span>
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
