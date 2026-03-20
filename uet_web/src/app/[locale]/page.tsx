"use client";

import { useState } from 'react';
import { useTranslations } from 'next-intl';
import { getTranslations } from 'next-intl/server';
import Link from 'next/link';
import { Sparkles, Github, BookOpen, MessageSquare, ArrowRight, Zap, Network, Scale, Copy, Check, Globe, Terminal, Cpu, Database, Shield, LayoutGrid, Bell, MessageCircle } from 'lucide-react';
import { ThemeToggle } from '@/components/theme-toggle';
import { LocaleSwitcher } from "@/components/locale-switcher";
import { useRouter } from 'next/navigation';
import { useParams } from 'next/navigation';
import MessengerPopover from '@/components/chat/MessengerPopover';
import NotificationBell from '@/components/layout/NotificationBell';
import { useChatContext } from '@/components/chat/ChatProvider';

const INSTALL_COMMANDS: Record<string, string> = {
  "Python Library": "pip install git+https://github.com/unityequilibrium/UnityEquilibriumTheory.git",
  "Topic Verification": "git clone ... && cd UnityEquilibriumTheory && pip install -e .",
  "Developer Setup": "pip install -e '.[dev]'",
};

const FEATURES = [
  { icon: Cpu, title: "Runs on Your Machine", desc: "macOS, Windows, or Linux. Private by default — your data stays yours." },
  { icon: Globe, title: "Any Framework", desc: "Connect to Next.js, React, Rust, Python. Works with any language or stack." },
  { icon: Database, title: "Persistent Knowledge", desc: "Remembers equations, proofs, and concepts uniquely tuned to UET." },
  { icon: Terminal, title: "Full API Access", desc: "Query the UET knowledge base via REST or MCP JSON-RPC endpoints." },
  { icon: Shield, title: "Quantum-Resistant", desc: "Built with Dilithium PQ signatures and SHA3/BLAKE3 hashing from day one." },
  { icon: Zap, title: "Proof-of-Useful-Work", desc: "Mining = solving real UET equations. Earn Uet-Cash for valid proofs." },
];

export default function Home() {
  const [activeTab, setActiveTab] = useState("Python Library");
  const [copied, setCopied] = useState(false);
  const t = useTranslations('Index');
  const tNav = useTranslations('Navigation');
  const params = useParams();
  const locale = params?.locale as string || 'en';
  const { openChat } = useChatContext();

  function handleCopy() {
    navigator.clipboard.writeText(INSTALL_COMMANDS[activeTab]);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  return (
    <div className="flex flex-col min-h-screen bg-white dark:bg-[#0a0a0f] text-black dark:text-white">
      {/* Starfield background */}
      <div
        className="fixed inset-0 pointer-events-none dark:opacity-100 opacity-0 transition-opacity"
        style={{
          background:
            "radial-gradient(ellipse at 60% 0%, rgba(13, 122, 95, 0.15) 0%, transparent 60%), radial-gradient(ellipse at 20% 80%, rgba(56, 189, 248, 0.12) 0%, transparent 55%)",
        }}
      />

      {/* Header */}
      <nav className="fixed top-0 w-full z-50 bg-white/80 dark:bg-black/80 backdrop-blur-md border-b border-black/5 dark:border-white/5">
        <div className="max-w-7xl mx-auto px-6 h-14 flex items-center justify-between">
          <div className="flex items-center gap-2 font-bold text-lg text-black dark:text-white">
            <img src="/logo.png" alt="UET Logo" className="w-8 h-8 object-contain" />
            UET
          </div>
          {/* Center nav links */}
          <div className="flex items-center gap-6 text-sm font-medium text-black/60 dark:text-white/60">
            <Link href={`/${locale}/feed`} className="hover:text-black dark:hover:text-white transition-colors">
              Feed
            </Link>
            <Link href={`/${locale}/workspaces`} className="hover:text-black dark:hover:text-white transition-colors">
              Projects
            </Link>
            <Link href={`/${locale}/chat`} className="hover:text-black dark:hover:text-white transition-colors flex items-center gap-1">
              <Sparkles className="w-4 h-4 text-purple-500" />
              Workchat
            </Link>
            <Link href={`/${locale}/docs`} className="hover:text-black dark:hover:text-white transition-colors">
              {t('readDocs')}
            </Link>
            <Link href={`/${locale}/topics`} className="hover:text-black dark:hover:text-white transition-colors">
              Topics
            </Link>
          </div>

          {/* Right nav — Facebook-style icons */}
          <div className="flex items-center gap-1.5">
            <Link href={`/${locale}/search`} className="w-9 h-9 rounded-full bg-black/5 dark:bg-white/10 hover:bg-black/10 dark:hover:bg-white/20 flex items-center justify-center transition-colors" title="Menu">
              <LayoutGrid size={17} className="text-black/70 dark:text-white/70" />
            </Link>
            <MessengerPopover onOpenChat={(contact) => openChat(contact)} />
            <NotificationBell />
            <Link href={`/${locale}/account`} className="w-9 h-9 rounded-full bg-gradient-to-br from-[#0d7a5f] to-emerald-600 flex items-center justify-center text-white text-xs font-bold ml-0.5" title="Profile">
              U
            </Link>
            <div className="flex items-center gap-1 ml-1">
              <LocaleSwitcher />
              <ThemeToggle />
            </div>
          </div>
        </div>
      </nav>

      <main className="relative z-10 flex-1">
        {/* Hero */}
        <section className="flex flex-col items-center text-center px-6 pt-24 pb-16">
          <div className="inline-flex items-center gap-2 px-3 py-1 mb-6 rounded-full border border-black/15 dark:border-white/15 bg-black/5 dark:bg-white/5 text-xs text-black/60 dark:text-white/60">
            <span className="w-1.5 h-1.5 rounded-full bg-green-400 inline-block" />
            v0.9.0 — 200+ Verified Tests
          </div>
          <h1 className="text-5xl sm:text-6xl md:text-7xl font-extrabold tracking-tight leading-tight mb-6">
            Unity Equilibrium<br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#0d7a5f] to-emerald-400 dark:from-[#2dd4bf] dark:to-emerald-300">
              Theory
            </span>
          </h1>
          <p className="max-w-xl text-lg text-black/60 dark:text-white/60 mb-10">
            {t('description')}
          </p>

          {/* Quick-start command block */}
          <div className="w-full max-w-2xl rounded-xl border border-black/10 dark:border-white/10 bg-gray-100 dark:bg-black/50 overflow-hidden shadow-2xl">
            {/* Tabs */}
            <div className="flex items-center gap-1 px-4 py-2 border-b border-black/10 dark:border-white/10 bg-black/5 dark:bg-white/5">
              {Object.keys(INSTALL_COMMANDS).map((tab) => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                    activeTab === tab
                      ? "bg-[#0d7a5f] text-white"
                      : "text-black/50 dark:text-white/50 hover:text-black dark:hover:text-white"
                  }`}
                >
                  {tab}
                </button>
              ))}
            </div>
            {/* Command */}
            <div className="flex items-center justify-between px-5 py-4">
              <code className="text-sm text-green-600 dark:text-green-400 font-mono whitespace-pre-wrap text-left break-all">
                <span className="text-black/40 dark:text-white/40">$ </span>
                {INSTALL_COMMANDS[activeTab]}
              </code>
              <button
                onClick={handleCopy}
                className="ml-4 p-1.5 rounded hover:bg-black/10 dark:hover:bg-white/10 text-black/40 dark:text-white/40 hover:text-black dark:hover:text-white transition-colors flex-shrink-0 self-start"
              >
                {copied ? <Check size={16} className="text-green-600 dark:text-green-400" /> : <Copy size={16} />}
              </button>
            </div>
          </div>
          <p className="mt-3 text-xs text-black/40 dark:text-white/40">
            Choose <strong className="text-black/70 dark:text-white/70">Python Library</strong> for API usage, or <strong className="text-black/70 dark:text-white/70">Topic Verification</strong> to reproduce the 31 domains.
          </p>

          <div className="flex items-center gap-4 mt-8">
            <Link
              href="/docs"
              className="flex items-center gap-2 px-5 py-2.5 rounded-lg bg-[#0d7a5f] hover:bg-[#0b644d] text-white font-semibold text-sm transition-colors"
            >
              <BookOpen size={16} /> {t('readDocs')}
            </Link>
            <Link
              href="https://github.com/unityequilibrium/UnityEquilibriumTheory"
              target="_blank"
              className="flex items-center gap-2 px-5 py-2.5 rounded-lg border border-black/20 dark:border-white/20 hover:bg-black/10 dark:hover:bg-white/10 text-sm transition-colors"
            >
              <Github size={16} /> {t('viewGithub')}
            </Link>
          </div>
        </section>

        {/* What it does */}
        <section id="features" className="px-6 py-16 max-w-5xl mx-auto">
          <h2 className="text-2xl font-bold mb-2">
            <span className="text-[#0d7a5f]">&#x276F;</span> {t('whatItDoes')}
          </h2>
          <p className="text-black/50 dark:text-white/50 mb-10 text-sm">A civilization-level operating system across 31 domains.</p>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {FEATURES.map(({ icon: Icon, title, desc }) => (
              <div
                key={title}
                className="rounded-xl border border-black/10 dark:border-white/10 bg-black/5 dark:bg-white/5 hover:bg-black/10 dark:hover:bg-white/10 p-5 transition-colors"
              >
                <Icon size={22} className="text-[#0d7a5f] dark:text-[#2dd4bf] mb-3" />
                <h3 className="font-semibold text-sm mb-1">{title}</h3>
                <p className="text-xs text-black/50 dark:text-white/50">{desc}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Works with everything */}
        <section className="px-6 py-16 border-t border-black/10 dark:border-white/10">
          <div className="max-w-5xl mx-auto text-center">
            <h2 className="text-2xl font-bold mb-2">
              <span className="text-[#0d7a5f]">&#x276F;</span> {t('worksWith')}
            </h2>
            <p className="text-black/50 dark:text-white/50 text-sm mb-8">Connect UET to any tool, model, or platform.</p>
            <div className="flex flex-wrap justify-center gap-3">
              {["Python", "Rust", "TypeScript", "React", "Next.js", "Docker", "GitHub Actions", "Railway"].map((t) => (
                <span
                  key={t}
                  className="px-4 py-2 rounded-full border border-black/15 dark:border-white/15 bg-black/5 dark:bg-white/5 text-xs text-black/60 dark:text-white/60"
                >
                  {t}
                </span>
              ))}
            </div>
          </div>
        </section>
      </main>

      <footer className="relative z-10 border-t border-black/10 dark:border-white/10 py-6 px-6 flex items-center justify-between text-xs text-black/30 dark:text-white/30">
        <span>© 2026 UET Project · MIT License</span>
        <div className="flex gap-4">
          <Link href="/docs" className="hover:text-black/60 dark:hover:text-white/60 transition-colors">Docs</Link>
          <Link href="/account" className="hover:text-black/60 dark:hover:text-white/60 transition-colors">Dashboard</Link>
          <Link href="https://github.com/unityequilibrium/UnityEquilibriumTheory" target="_blank" className="hover:text-black/60 dark:hover:text-white/60 transition-colors">GitHub</Link>
        </div>
      </footer>
    </div>
  );
}
