'use client';

import AppShell from '@/components/layout/AppShell';
import BentoGridLayout, { BentoCard } from '@/components/layout/BentoGridLayout';
import { Newspaper, TrendingUp, Sparkles, ArrowUpRight, FolderGit2, Users } from 'lucide-react';
import Link from 'next/link';
import { useParams } from 'next/navigation';

const FEATURED_PROJECTS = [
  { id: 'proj-1', name: 'UET Core Research', desc: 'Unified thermodynamic framework for ethical AI governance. Latest: v0.9 equation set verified.', members: 12, topics: 8 },
  { id: 'proj-2', name: 'AI Alignment Study', desc: 'Multi-model alignment benchmarks using UET Equilibrium scoring. New dataset published.', members: 6, topics: 4 },
  { id: 'proj-3', name: 'Quantum Entropy Model', desc: 'V = E × I × γ simulation — 99.8% stability index across 200 test domains.', members: 9, topics: 6 },
];

const TRENDING_POSTS = [
  { id: '1', author: 'Dr. Beta', title: 'Quantum entropy model hits 99.8% stability', time: '2h ago' },
  { id: '2', author: 'Researcher Alpha', title: 'AI alignment paper: ethics as thermodynamics', time: '5h ago' },
  { id: '3', author: 'Sarah Chen', title: 'Call for collaborators: thermodynamic economics', time: '1d ago' },
  { id: '4', author: 'Prof. Kumar', title: 'New PoUW node rewards structure proposal', time: '2d ago' },
];

export default function NewsPage() {
  const params = useParams();
  const locale = (params?.locale as string) || 'en';

  return (
    <AppShell>
      <BentoGridLayout columns={3}>

        {/* Header row */}
        <div className="col-span-1 sm:col-span-2 lg:col-span-3 rounded-xl border border-border bg-card px-5 py-4 flex items-center gap-3">
          <Newspaper size={18} className="text-primary shrink-0" />
          <div>
            <h1 className="font-bold text-sm">News & Discovery</h1>
            <p className="text-[11px] text-muted-foreground">Platform updates, project profiles, and research publications</p>
          </div>
        </div>

        {/* Featured Project — 2 cols, tall */}
        <BentoCard span={2} className="flex flex-col">
          <div className="flex items-center gap-2 mb-4">
            <Sparkles size={14} className="text-primary" />
            <span className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider">Featured Project</span>
          </div>
          <div className="flex-1 space-y-3">
            {FEATURED_PROJECTS.slice(0, 2).map(p => (
              <Link key={p.id} href={`/${locale}/project`} className="block p-4 rounded-xl border border-border hover:border-primary/40 bg-muted/30 transition-colors">
                <div className="flex items-start justify-between gap-2 mb-1.5">
                  <div className="flex items-center gap-2">
                    <FolderGit2 size={14} className="text-primary shrink-0 mt-0.5" />
                    <span className="text-sm font-semibold">{p.name}</span>
                  </div>
                  <ArrowUpRight size={13} className="text-muted-foreground shrink-0 mt-0.5" />
                </div>
                <p className="text-xs text-muted-foreground ml-5 mb-2">{p.desc}</p>
                <div className="flex items-center gap-3 ml-5 text-[10px] text-muted-foreground">
                  <span className="flex items-center gap-1"><Users size={10} /> {p.members} members</span>
                  <span>{p.topics} topics</span>
                </div>
              </Link>
            ))}
          </div>
        </BentoCard>

        {/* Trending Posts — 1 col */}
        <BentoCard className="flex flex-col">
          <div className="flex items-center gap-2 mb-4">
            <TrendingUp size={14} className="text-primary" />
            <span className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider">Trending</span>
          </div>
          <div className="flex-1 space-y-3">
            {TRENDING_POSTS.map((post, i) => (
              <Link key={post.id} href={`/${locale}/community`} className="flex items-start gap-2 hover:bg-muted/40 rounded-lg p-2 -mx-2 transition-colors">
                <span className="text-[10px] font-bold text-muted-foreground/50 w-4 shrink-0 mt-0.5">{i + 1}</span>
                <div>
                  <div className="text-xs font-medium leading-snug">{post.title}</div>
                  <div className="text-[10px] text-muted-foreground mt-0.5">{post.author} · {post.time}</div>
                </div>
              </Link>
            ))}
          </div>
        </BentoCard>

        {/* Third project card */}
        <BentoCard className="flex flex-col">
          <div className="flex items-center gap-2 mb-3">
            <FolderGit2 size={14} className="text-primary" />
            <span className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider">New Project</span>
          </div>
          <Link href={`/${locale}/project`} className="flex-1 flex flex-col justify-between hover:opacity-80 transition-opacity">
            <div>
              <h2 className="font-bold mb-1">{FEATURED_PROJECTS[2].name}</h2>
              <p className="text-xs text-muted-foreground">{FEATURED_PROJECTS[2].desc}</p>
            </div>
            <div className="flex items-center gap-2 mt-3 text-[10px] text-muted-foreground">
              <Users size={10} /> {FEATURED_PROJECTS[2].members} members · {FEATURED_PROJECTS[2].topics} topics
            </div>
          </Link>
        </BentoCard>

        {/* Platform update — spans 2 cols */}
        <BentoCard span={2} className="bg-gradient-to-br from-primary/5 to-emerald-500/5">
          <div className="flex items-center gap-2 mb-3">
            <Sparkles size={14} className="text-primary" />
            <span className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider">Platform Update</span>
            <span className="ml-auto text-[10px] bg-primary/10 text-primary px-2 py-0.5 rounded-full font-medium">v5.0</span>
          </div>
          <h2 className="font-bold mb-2">5 Heavy Pages Architecture</h2>
          <p className="text-xs text-muted-foreground">Full platform restructure: News, WorkChat (NotebookLM-style), Community (Facebook + Telegram), Project (Discord + Obsidian), and Economy (KPI Dashboard). All pages now use shared AppShell with locale routing.</p>
        </BentoCard>

      </BentoGridLayout>
    </AppShell>
  );
}
