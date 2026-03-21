'use client';

import AppShell from '@/components/layout/AppShell';
import ProfilePanel from '@/components/feed/ProfilePanel';
import ChatFriendsPanel from '@/components/feed/ChatFriendsPanel';
import { Rss, PenLine } from 'lucide-react';

const MOCK_POSTS = [
  { id: '1', author: 'Researcher Alpha', institution: 'MIT', time: '2 hours ago', content: 'Just published a new paper on AI alignment! Check it out in Project Alpha.', upvotes: 42, comments: 8, isVerified: true },
  { id: '2', author: 'Dr. Beta', institution: 'CERN', time: '5 hours ago', content: 'New simulation results for quantum entropy model V = E × I × γ. The stability index reached 99.8% across all test domains.', upvotes: 128, comments: 23, isVerified: true },
  { id: '3', author: 'Sarah Chen', institution: 'Stanford', time: '1 day ago', content: 'Looking for collaborators on thermodynamic economics modeling. DM me if interested!', upvotes: 15, comments: 4, isVerified: false },
];

export default function CommunityPage() {
  return (
    <AppShell>
      <div className="flex-1 flex overflow-hidden">
        {/* Panel 1: Profile (IG style) */}
        <div className="w-[280px] min-w-[250px] border-r border-border overflow-y-auto hidden md:block">
          <ProfilePanel />
        </div>

        {/* Panel 2: Feed + Reels + Posts */}
        <div className="flex-1 overflow-y-auto">
          <div className="max-w-2xl mx-auto p-4">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <Rss size={18} className="text-primary" />
                <h2 className="font-semibold text-sm">Community Feed</h2>
              </div>
              <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-primary text-primary-foreground text-xs font-medium hover:bg-primary/90 transition-colors">
                <PenLine size={13} /> New Post
              </button>
            </div>

            <div className="space-y-3">
              {MOCK_POSTS.map(post => (
                <div key={post.id} className="p-4 rounded-xl border border-border bg-card hover:border-primary/40 transition-colors">
                  <div className="flex items-center gap-2 mb-2">
                    <div className="w-9 h-9 rounded-full bg-gradient-to-br from-primary/30 to-emerald-500/30 flex items-center justify-center text-xs font-bold">{post.author[0]}</div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-1.5">
                        <span className="text-sm font-semibold truncate">{post.author}</span>
                        {post.isVerified && <span className="text-[9px] bg-primary/10 text-primary px-1.5 py-0.5 rounded-full font-medium">Verified</span>}
                      </div>
                      <div className="text-[10px] text-muted-foreground">{post.institution} · {post.time}</div>
                    </div>
                  </div>
                  <p className="text-sm mb-3">{post.content}</p>
                  <div className="flex items-center gap-4 text-xs text-muted-foreground">
                    <span>▲ {post.upvotes}</span>
                    <span>💬 {post.comments}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Panel 3: Chat Community & Friends */}
        <div className="w-[280px] min-w-[250px] border-l border-border overflow-y-auto hidden lg:block">
          <ChatFriendsPanel />
        </div>
      </div>
    </AppShell>
  );
}
