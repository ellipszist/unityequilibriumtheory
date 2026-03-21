"use client";

import { useTranslations } from 'next-intl';
import Link from 'next/link';
import { Sparkles, Github, BookOpen, MessageSquare, ArrowRight, Zap, Network, Scale, Globe, Cpu, Database, Shield } from 'lucide-react';
import { useParams } from 'next/navigation';
import MessengerPopover from '@/components/chat/MessengerPopover';
import MenuPopover from '@/components/layout/MenuPopover';
import NotificationBell from '@/components/layout/NotificationBell';
import ProfilePopover from '@/components/layout/ProfilePopover';
import { useChatContext } from '@/components/chat/ChatProvider';

const FEATURES = [
  { icon: Cpu, title: "Runs on Your Machine", desc: "macOS, Windows, or Linux. Private by default — your data stays yours." },
  { icon: Globe, title: "Any Framework", desc: "Connect to Next.js, React, Rust, Python. Works with any language or stack." },
  { icon: Database, title: "Persistent Knowledge", desc: "Remembers equations, proofs, and concepts uniquely tuned to UET." },
  { icon: Zap, title: "Full API Access", desc: "Query the UET knowledge base via REST or MCP JSON-RPC endpoints." },
  { icon: Shield, title: "Quantum-Resistant", desc: "Built with Dilithium PQ signatures and SHA3/BLAKE3 hashing from day one." },
  { icon: Zap, title: "Proof-of-Useful-Work", desc: "Mining = solving real UET equations. Earn Uet-Cash for valid proofs." },
];

export default function Home() {
  const t = useTranslations('Index');
  const tNav = useTranslations('Navigation');
  const params = useParams();
  const locale = params?.locale as string || 'en';
  const { openChat } = useChatContext();

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
            <Link href={`/${locale}/news`} className="hover:text-black dark:hover:text-white transition-colors">
              News
            </Link>
            <Link href={`/${locale}/workchat`} className="hover:text-black dark:hover:text-white transition-colors flex items-center gap-1">
              <Sparkles className="w-4 h-4 text-purple-500" />
              WorkChat
            </Link>
            <Link href={`/${locale}/community`} className="hover:text-black dark:hover:text-white transition-colors">
              Community
            </Link>
            <Link href={`/${locale}/project`} className="hover:text-black dark:hover:text-white transition-colors">
              Project
            </Link>
            <Link href={`/${locale}/economy`} className="hover:text-black dark:hover:text-white transition-colors">
              Economy
            </Link>
          </div>

          {/* Right nav — Facebook-style icons */}
          <div className="flex items-center gap-1.5">
            <MenuPopover />
            <MessengerPopover onOpenChat={(contact) => openChat(contact)} />
            <NotificationBell />
            <ProfilePopover />
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

          <div className="flex items-center gap-4 mt-8">
            <Link
              href={`/${locale}/community`}
              className="flex items-center gap-2 px-6 py-2.5 rounded-lg bg-[#0d7a5f] hover:bg-[#0b644d] text-white font-semibold text-sm transition-colors"
            >
              Get Started
            </Link>
            <Link
              href={`/${locale}/manual`}
              className="flex items-center gap-2 px-6 py-2.5 rounded-lg border border-black/20 dark:border-white/20 hover:bg-black/10 dark:hover:bg-white/10 text-sm transition-colors"
            >
              <BookOpen size={16} /> {t('readDocs')}
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
          <Link href={`/${locale}/manual`} className="hover:text-black/60 dark:hover:text-white/60 transition-colors">Manual</Link>
          <Link href={`/${locale}/economy/account`} className="hover:text-black/60 dark:hover:text-white/60 transition-colors">Dashboard</Link>
          <Link href="https://github.com/unityequilibrium/UnityEquilibriumTheory" target="_blank" className="hover:text-black/60 dark:hover:text-white/60 transition-colors">GitHub</Link>
        </div>
      </footer>
    </div>
  );
}
