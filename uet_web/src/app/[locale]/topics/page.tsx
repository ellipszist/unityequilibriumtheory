"use client";

import { useState } from "react";
import Link from "next/link";
import { ThemeToggle } from "@/components/theme-toggle";
import { LocaleSwitcher } from "@/components/locale-switcher";
import { useTranslations } from "next-intl";

export default function TopicsPage() {
  const tNav = useTranslations('Navigation');
  const [openCategory, setOpenCategory] = useState<string | null>("Quantum Mechanics");

  const toggleCategory = (cat: string) => {
    setOpenCategory(openCategory === cat ? null : cat);
  };

  const categories = [
    {
      name: "Quantum Mechanics",
      icon: "⚛️",
      count: 42,
      topics: [
        { id: "T-QM-01", name: "Wave Function Collapse", status: "PASS", stability: "99.8%", desc: "Simulates the collapse of the wave function using UET information density metrics." },
        { id: "T-QM-02", name: "Entanglement Information", status: "PASS", stability: "99.5%", desc: "Demonstrates information transfer between entangled particles without violating causality." },
        { id: "T-QM-03", name: "Quantum Gravity Limit", status: "WARN", stability: "85.2%", desc: "Tests behavior at the Planck scale. High instability observed near singularity limits." },
      ]
    },
    {
      name: "Astrophysics",
      icon: "🌌",
      count: 38,
      topics: [
        { id: "T-AS-01", name: "Dark Energy Expansion", status: "PASS", stability: "98.1%", desc: "Explains cosmic expansion as a side-effect of vacuum information processing." },
        { id: "T-AS-02", name: "Black Hole Thermodynamics", status: "PASS", stability: "96.4%", desc: "Aligns Hawking radiation with UET energy-information equivalency." },
      ]
    },
    {
      name: "Economics",
      icon: "📈",
      count: 15,
      topics: [
        { id: "T-EC-01", name: "Hashrate to Value Mapping", status: "PASS", stability: "94.5%", desc: "Proves the mathematical link between cryptographic energy expenditure and market value." },
      ]
    },
  ];

  return (
    <div className="flex flex-col min-h-screen bg-white dark:bg-[#0a0a0f] text-black dark:text-white font-sans selection:bg-[#0d7a5f]/30">
      {/* Background gradients */}
      <div 
        className="fixed inset-0 pointer-events-none dark:opacity-100 opacity-0 transition-opacity"
        style={{
          background: "radial-gradient(circle at 0% 0%, rgba(13, 122, 95, 0.15) 0%, transparent 50%), radial-gradient(circle at 100% 100%, rgba(56, 189, 248, 0.15) 0%, transparent 50%)",
          zIndex: -1
        }}
      />

      {/* Header Nav */}
      <nav className="fixed top-0 w-full z-50 bg-white/80 dark:bg-[#0a0a0f]/80 backdrop-blur-md border-b border-black/5 dark:border-white/10 transition-colors">
        <div className="max-w-7xl mx-auto px-6 h-14 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2 font-bold text-lg text-black dark:text-white">
            <img src="/logo.png" alt="UET Logo" className="w-8 h-8 object-contain" />
            UET
          </Link>
          <div className="flex items-center gap-4 text-sm font-medium text-black/60 dark:text-white/60">
            <Link href="/docs" className="hover:text-black dark:hover:text-white transition-colors">{tNav('docs')}</Link>
            <Link href="/topics" className="text-[#0d7a5f] font-semibold">{tNav('topics') || "Topics"}</Link>
            <Link href="/account" className="px-3 py-1.5 rounded-md bg-black/5 dark:bg-white/10 hover:bg-black/10 dark:hover:bg-white/20 text-black dark:text-white transition-colors text-sm">
              {tNav('dashboard')}
            </Link>
            <div className="flex items-center gap-2">
              <LocaleSwitcher />
              <ThemeToggle />
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 pt-32 pb-24 w-full relative z-10 flex-1">
        <header className="text-center mb-20">
          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-6 bg-gradient-to-r from-[#0d7a5f] to-emerald-400 dark:from-[#2dd4bf] dark:to-emerald-300 text-transparent bg-clip-text drop-shadow-[0_0_30px_rgba(13,122,95,0.3)]">
            UET TOPICS
          </h1>
          <p className="text-xl text-black/60 dark:text-gray-400 font-light">Unified Exhibition Hub &bull; Professional Simulation Gallery</p>
        </header>

        {/* Stats Bar */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-20 bg-black/5 dark:bg-white/5 p-8 rounded-3xl border border-black/10 dark:border-white/10 backdrop-blur-md">
          <div className="text-center">
            <span className="block text-4xl font-bold text-[#0d7a5f] dark:text-[#2dd4bf] mb-2">95</span>
            <span className="text-xs uppercase tracking-widest text-black/50 dark:text-gray-400">Total Topics</span>
          </div>
          <div className="text-center">
            <span className="block text-4xl font-bold text-[#0d7a5f] dark:text-[#2dd4bf] mb-2">91</span>
            <span className="text-xs uppercase tracking-widest text-black/50 dark:text-gray-400">Verified (PASS)</span>
          </div>
          <div className="text-center">
            <span className="block text-4xl font-bold text-[#0d7a5f] dark:text-[#2dd4bf] mb-2">98.3%</span>
            <span className="text-xs uppercase tracking-widest text-black/50 dark:text-gray-400">Model Stability</span>
          </div>
          <div className="text-center">
            <span className="block text-4xl font-bold text-[#0d7a5f] dark:text-[#2dd4bf] mb-2">3</span>
            <span className="text-xs uppercase tracking-widest text-black/50 dark:text-gray-400">Core Domains</span>
          </div>
        </div>

        {/* Theory Section (Inspired by bridge-eq) */}
        <section className="mb-24 pt-10 border-t border-black/10 dark:border-white/10">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-[#0d7a5f] to-emerald-400 dark:from-[#2dd4bf] dark:to-emerald-300 text-transparent bg-clip-text mb-4">
              Theoretical Framework
            </h2>
            <p className="text-black/60 dark:text-gray-400 text-lg font-light">Bridging Material & Information Worlds through Equilibrium Dynamics</p>
          </div>

          <div className="bg-[#0d7a5f]/10 dark:bg-[#0d7a5f]/20 border border-[#0d7a5f]/30 p-12 rounded-3xl text-center backdrop-blur-md relative overflow-hidden group">
            <div className="absolute -inset-[50%] bg-[radial-gradient(circle,rgba(13,122,95,0.1)_0%,transparent_70%)] group-hover:animate-[spin_10s_linear_infinite]" />
            <div className="relative z-10 text-4xl md:text-5xl font-extrabold text-black dark:text-white tracking-widest mb-6">
              V = E &times; I &times; &gamma;
            </div>
            <div className="relative z-10 text-[#0d7a5f] dark:text-[#2dd4bf] text-sm font-semibold uppercase tracking-[0.2em]">
              UET Master Equation
            </div>
          </div>
        </section>

        {/* Categories / Grid */}
        <div className="space-y-6">
          <div className="flex items-center gap-4 mb-10">
            <h2 className="text-3xl font-bold text-black dark:text-white">Simulation Results</h2>
            <div className="flex-1 h-px bg-gradient-to-r from-black/20 dark:from-white/20 to-transparent" />
          </div>

          {categories.map((cat) => (
            <div key={cat.name} className="bg-black/5 dark:bg-gray-900/70 border border-black/10 dark:border-white/10 rounded-2xl overflow-hidden transition-colors hover:border-[#0d7a5f]/50 dark:hover:border-[#2dd4bf]/50">
              <button 
                onClick={() => toggleCategory(cat.name)}
                className="w-full px-8 py-5 flex items-center text-left hover:bg-black/5 dark:hover:bg-white/5 transition-colors"
              >
                <span className="text-xl mr-4">{cat.icon}</span>
                <span className="text-lg font-semibold text-black/80 dark:text-gray-300 group-hover:text-black dark:group-hover:text-white flex-1">{cat.name}</span>
                <span className="text-sm text-black/50 dark:text-gray-500 mr-4">{cat.count} models</span>
                <span className={`transform transition-transform ${openCategory === cat.name ? 'rotate-90' : ''} text-black/40 dark:text-gray-500`}>
                  ▶
                </span>
              </button>
              
              {openCategory === cat.name && (
                <div className="p-8 border-t border-black/5 dark:border-white/10 bg-black/5 dark:bg-black/20">
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {cat.topics.map((topic) => (
                      <div key={topic.id} className="group relative bg-white dark:bg-gray-900/80 border border-black/10 dark:border-white/10 rounded-xl overflow-hidden hover:border-[#0d7a5f] dark:hover:border-[#2dd4bf] hover:-translate-y-1 transition-all duration-300 flex flex-col h-full min-h-[250px] shadow-sm hover:shadow-md">
                        <div className="absolute inset-0 bg-gradient-to-br from-[#0d7a5f]/5 dark:from-white/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none" />
                        
                        <div className="p-6 flex-1 flex flex-col relative z-10">
                          <div className="flex justify-between items-start mb-6">
                            <span className="font-mono text-xs text-black/40 dark:text-gray-500 tracking-wider">{topic.id}</span>
                            <span className={`text-[10px] font-bold px-3 py-1 rounded-full tracking-wider border ${
                              topic.status === 'PASS' ? 'bg-emerald-100 dark:bg-emerald-500/15 text-emerald-700 dark:text-emerald-400 border-emerald-200 dark:border-emerald-500/30' :
                              topic.status === 'WARN' ? 'bg-amber-100 dark:bg-amber-500/15 text-amber-700 dark:text-amber-400 border-amber-200 dark:border-amber-500/30' :
                              'bg-red-100 dark:bg-red-500/15 text-red-700 dark:text-red-400 border-red-200 dark:border-red-500/30'
                            }`}>
                              {topic.status}
                            </span>
                          </div>
                          
                          <h3 className="text-xl font-bold text-black dark:text-white mb-3 group-hover:text-[#0d7a5f] dark:group-hover:text-[#2dd4bf] transition-colors">
                            {topic.name}
                          </h3>
                          
                          <p className="text-sm text-black/60 dark:text-gray-400 leading-relaxed mb-6 flex-1">
                            {topic.desc}
                          </p>

                          <div className="pt-4 border-t border-black/10 dark:border-white/10 flex justify-between items-center text-sm mt-auto">
                            <span className="text-black/50 dark:text-gray-500">Stability Index</span>
                            <span className="font-mono font-medium text-[#0d7a5f] dark:text-[#2dd4bf]">{topic.stability}</span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}
