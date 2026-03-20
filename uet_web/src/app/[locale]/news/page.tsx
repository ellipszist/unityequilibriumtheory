'use client';

import { useState } from 'react';
import AppShell from '@/components/layout/AppShell';
import { FlaskConical, TrendingUp, CheckCircle2, AlertTriangle, ChevronRight } from 'lucide-react';

const CATEGORIES = [
  {
    name: 'Quantum Mechanics',
    icon: '⚛️',
    count: 42,
    topics: [
      { id: 'T-QM-01', name: 'Wave Function Collapse', status: 'PASS', stability: '99.8%', desc: 'Simulates the collapse of the wave function using UET information density metrics.' },
      { id: 'T-QM-02', name: 'Entanglement Information', status: 'PASS', stability: '99.5%', desc: 'Demonstrates information transfer between entangled particles without violating causality.' },
      { id: 'T-QM-03', name: 'Quantum Gravity Limit', status: 'WARN', stability: '85.2%', desc: 'Tests behavior at the Planck scale. High instability observed near singularity limits.' },
    ],
  },
  {
    name: 'Astrophysics',
    icon: '🌌',
    count: 38,
    topics: [
      { id: 'T-AS-01', name: 'Dark Energy Expansion', status: 'PASS', stability: '98.1%', desc: 'Explains cosmic expansion as a side-effect of vacuum information processing.' },
      { id: 'T-AS-02', name: 'Black Hole Thermodynamics', status: 'PASS', stability: '96.4%', desc: 'Aligns Hawking radiation with UET energy-information equivalency.' },
    ],
  },
  {
    name: 'Economics',
    icon: '📈',
    count: 15,
    topics: [
      { id: 'T-EC-01', name: 'Hashrate to Value Mapping', status: 'PASS', stability: '94.5%', desc: 'Proves the mathematical link between cryptographic energy expenditure and market value.' },
    ],
  },
  {
    name: 'Neuroscience',
    icon: '🧠',
    count: 21,
    topics: [
      { id: 'T-NS-01', name: 'Consciousness Entropy Model', status: 'PASS', stability: '91.2%', desc: 'Maps conscious states to entropy gradients within the UET information field.' },
      { id: 'T-NS-02', name: 'Neural Synchrony Patterns', status: 'WARN', stability: '78.6%', desc: 'Analyzes gamma-band synchronization using UET resonance equations.' },
    ],
  },
  {
    name: 'Thermodynamics',
    icon: '🔥',
    count: 19,
    topics: [
      { id: 'T-TD-01', name: 'Entropy Arrow of Time', status: 'PASS', stability: '97.3%', desc: 'Derives the thermodynamic arrow of time from UET information asymmetry.' },
    ],
  },
];

const STATS = [
  { label: 'Total Topics', value: '95' },
  { label: 'Verified (PASS)', value: '91' },
  { label: 'Model Stability', value: '98.3%' },
  { label: 'Core Domains', value: '31' },
];

export default function NewsPage() {
  const [openCategory, setOpenCategory] = useState<string | null>('Quantum Mechanics');

  return (
    <AppShell>
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-5xl mx-auto px-4 py-8">
          {/* Header */}
          <div className="mb-8">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-9 h-9 rounded-xl bg-primary/10 flex items-center justify-center">
                <FlaskConical size={18} className="text-primary" />
              </div>
              <h1 className="text-2xl font-bold">UET Topics &amp; News</h1>
            </div>
            <p className="text-sm text-muted-foreground">Unified Exhibition Hub · Professional Simulation Gallery</p>
          </div>

          {/* Master equation highlight */}
          <div className="mb-8 rounded-2xl border border-primary/20 bg-primary/5 px-6 py-5 text-center">
            <div className="text-3xl font-extrabold tracking-widest mb-1">V = E × I × γ</div>
            <p className="text-xs text-muted-foreground uppercase tracking-widest font-semibold">UET Master Equation</p>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-8">
            {STATS.map(s => (
              <div key={s.label} className="rounded-xl border border-border bg-card p-4 text-center">
                <div className="text-2xl font-bold text-primary mb-0.5">{s.value}</div>
                <div className="text-xs text-muted-foreground">{s.label}</div>
              </div>
            ))}
          </div>

          {/* Category accordion */}
          <div className="space-y-3">
            <div className="flex items-center gap-3 mb-4">
              <TrendingUp size={16} className="text-primary" />
              <h2 className="font-semibold">Simulation Results</h2>
            </div>

            {CATEGORIES.map(cat => (
              <div key={cat.name} className="rounded-xl border border-border bg-card overflow-hidden">
                <button
                  onClick={() => setOpenCategory(openCategory === cat.name ? null : cat.name)}
                  className="w-full flex items-center gap-3 px-5 py-4 text-left hover:bg-muted/50 transition-colors"
                >
                  <span className="text-xl">{cat.icon}</span>
                  <span className="font-semibold flex-1">{cat.name}</span>
                  <span className="text-xs text-muted-foreground mr-2">{cat.count} models</span>
                  <ChevronRight
                    size={16}
                    className={`text-muted-foreground transition-transform ${openCategory === cat.name ? 'rotate-90' : ''}`}
                  />
                </button>

                {openCategory === cat.name && (
                  <div className="px-5 pb-5 pt-1 border-t border-border grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                    {cat.topics.map(topic => (
                      <div
                        key={topic.id}
                        className="rounded-xl border border-border bg-background p-4 flex flex-col gap-2 hover:border-primary/50 transition-colors"
                      >
                        <div className="flex items-center justify-between">
                          <span className="font-mono text-[10px] text-muted-foreground">{topic.id}</span>
                          <span className={`flex items-center gap-1 text-[10px] font-bold px-2 py-0.5 rounded-full ${
                            topic.status === 'PASS'
                              ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400'
                              : 'bg-amber-500/10 text-amber-600 dark:text-amber-400'
                          }`}>
                            {topic.status === 'PASS'
                              ? <CheckCircle2 size={10} />
                              : <AlertTriangle size={10} />}
                            {topic.status}
                          </span>
                        </div>
                        <h3 className="font-semibold text-sm">{topic.name}</h3>
                        <p className="text-xs text-muted-foreground leading-relaxed flex-1">{topic.desc}</p>
                        <div className="flex items-center justify-between pt-2 border-t border-border text-xs">
                          <span className="text-muted-foreground">Stability</span>
                          <span className="font-mono font-semibold text-primary">{topic.stability}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </AppShell>
  );
}
