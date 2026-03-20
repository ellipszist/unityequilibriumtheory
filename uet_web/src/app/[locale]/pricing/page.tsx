"use client";

import { useState } from "react";
import Link from "next/link";
import { Check, X, CreditCard } from "lucide-react";
import { LocaleSwitcher } from "@/components/locale-switcher";
import { ThemeToggle } from "@/components/theme-toggle";

const PRICING_TIERS = [
  {
    name: "Free",
    description: "For individuals exploring the UET platform.",
    price: "$0",
    interval: "forever",
    features: [
      "100 Requests / month",
      "Standard models (BGE-M3)",
      "Basic MCP integration",
      "Community support",
    ],
    missingFeatures: [
      "Priority API processing",
      "Custom vector embeddings",
      "Advanced integrations",
    ],
    buttonText: "Current Plan",
    buttonVariant: "outline",
  },
  {
    name: "Pro",
    description: "For researchers and developers needing more power.",
    price: "$20",
    interval: "/ month",
    features: [
      "10,000 Requests / month",
      "Standard models (BGE-M3)",
      "Full MCP integration",
      "Priority API processing",
      "Email support",
    ],
    missingFeatures: [
      "Custom vector embeddings",
    ],
    buttonText: "Upgrade to Pro",
    buttonVariant: "primary",
    highlight: true,
  },
  {
    name: "Enterprise",
    description: "Custom limits and dedicated infrastructure.",
    price: "Custom",
    interval: "",
    features: [
      "Unlimited Requests",
      "All models + Custom models",
      "Custom vector embeddings",
      "Dedicated infrastructure",
      "24/7 Priority support",
      "SLA guarantee",
    ],
    missingFeatures: [],
    buttonText: "Contact Us",
    buttonVariant: "outline",
  }
];

export default function PricingPage() {
  const [isAnnual, setIsAnnual] = useState(false);

  return (
    <div className="flex flex-col min-h-screen bg-white dark:bg-[#0a0a0f] text-[#111] dark:text-white text-sm">
      {/* Header */}
      <header className="flex items-center h-14 px-6 border-b border-black/10 dark:border-white/10 bg-white/90 dark:bg-[#0a0a0f]/90 backdrop-blur-md">
        <Link href="/" className="flex items-center gap-2 font-bold text-base hover:opacity-80 transition-opacity">
          <img src="/logo.png" alt="UET Logo" className="w-8 h-8 object-contain" />
          <span className="hidden sm:inline">UET Platform</span>
        </Link>
        <nav className="ml-8 flex items-center gap-6 text-xs text-black/50 dark:text-white/50">
          <Link href="/account" className="hover:text-black dark:hover:text-white transition-colors">Overview</Link>
          <Link href="/docs" className="hover:text-black dark:hover:text-white transition-colors">Docs</Link>
          <Link href="/chat" className="hover:text-black dark:hover:text-white transition-colors">Knowledge Search</Link>
          <Link href="/pricing" className="text-[#0d7a5f] font-semibold border-b-2 border-[#0d7a5f] pb-0.5">Pricing</Link>
        </nav>
        <div className="ml-auto flex items-center gap-3">
          <LocaleSwitcher />
          <ThemeToggle />
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 flex flex-col items-center py-16 px-4 md:px-6">
        
        {/* Pricing Header */}
        <div className="text-center max-w-2xl mx-auto mb-12">
          <h1 className="text-3xl md:text-4xl font-bold mb-4 tracking-tight">Simple, transparent pricing</h1>
          <p className="text-base text-black/60 dark:text-white/60 mb-8">
            Start for free, upgrade when you need more power to accelerate your research.
          </p>

          {/* Billing Toggle */}
          <div className="flex items-center justify-center gap-3">
            <span className={`text-sm ${!isAnnual ? 'font-semibold' : 'text-black/50 dark:text-white/50'}`}>Monthly</span>
            <button 
              onClick={() => setIsAnnual(!isAnnual)}
              className="relative w-12 h-6 rounded-full bg-black/10 dark:bg-white/10 p-1 transition-colors"
            >
              <div 
                className={`w-4 h-4 rounded-full bg-white shadow-sm transition-transform ${isAnnual ? 'translate-x-6' : 'translate-x-0'}`}
              />
            </button>
            <span className={`text-sm ${isAnnual ? 'font-semibold' : 'text-black/50 dark:text-white/50'}`}>
              Annually <span className="ml-1 text-[10px] bg-green-100 text-green-700 px-2 py-0.5 rounded-full font-bold uppercase tracking-wide">Save 20%</span>
            </span>
          </div>
        </div>

        {/* Pricing Cards */}
        <div className="grid md:grid-cols-3 gap-6 max-w-5xl w-full">
          {PRICING_TIERS.map((tier) => (
            <div 
              key={tier.name}
              className={`relative flex flex-col p-6 rounded-2xl bg-white dark:bg-[#1a1a24] border ${
                tier.highlight 
                  ? 'border-[#0d7a5f] shadow-lg shadow-[#0d7a5f]/10 dark:shadow-[#0d7a5f]/20 scale-[1.02]' 
                  : 'border-black/10 dark:border-white/10'
              }`}
            >
              {tier.highlight && (
                <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-[#0d7a5f] text-white text-[10px] font-bold uppercase tracking-widest px-3 py-1 rounded-full">
                  Most Popular
                </div>
              )}

              <div className="mb-6">
                <h3 className="text-lg font-bold mb-2">{tier.name}</h3>
                <p className="text-xs text-black/50 dark:text-white/50 min-h-[40px]">{tier.description}</p>
              </div>

              <div className="mb-6 flex items-baseline gap-1">
                <span className="text-4xl font-bold">
                  {tier.price === "Custom" ? tier.price : isAnnual && tier.price !== "$0" ? `$${parseInt(tier.price.replace('$', '')) * 0.8}` : tier.price}
                </span>
                <span className="text-sm text-black/50 dark:text-white/50 font-medium">{tier.interval}</span>
              </div>

              <button 
                className={`w-full py-2.5 rounded-xl font-medium text-sm transition-all flex items-center justify-center gap-2 mb-8 ${
                  tier.buttonVariant === 'primary'
                    ? 'bg-[#0d7a5f] text-white hover:bg-[#0b644d] shadow-sm hover:shadow'
                    : 'bg-black/5 dark:bg-white/5 hover:bg-black/10 dark:hover:bg-white/10 text-black dark:text-white'
                }`}
              >
                {tier.buttonVariant === 'primary' && <CreditCard size={16} />}
                {tier.buttonText}
              </button>

              <div className="flex-1">
                <p className="text-xs font-semibold uppercase tracking-wider text-black/40 dark:text-white/40 mb-4">What's included</p>
                <ul className="space-y-3">
                  {tier.features.map((feat) => (
                    <li key={feat} className="flex items-start gap-3 text-sm">
                      <Check size={16} className="text-[#0d7a5f] shrink-0 mt-0.5" />
                      <span className="text-black/80 dark:text-white/80">{feat}</span>
                    </li>
                  ))}
                  {tier.missingFeatures.map((feat) => (
                    <li key={feat} className="flex items-start gap-3 text-sm opacity-40">
                      <X size={16} className="text-black shrink-0 mt-0.5" />
                      <span className="text-black/80 dark:text-white/80">{feat}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>

        {/* Enterprise/FAQ Section */}
        <div className="mt-24 text-center max-w-2xl mx-auto">
          <h2 className="text-xl font-bold mb-4">Need something else?</h2>
          <p className="text-black/60 dark:text-white/60 mb-6">
            If you represent a university or research lab, we offer special academic pricing. Contact us for details.
          </p>
          <a href="#" className="text-[#0d7a5f] font-semibold hover:underline">Contact Sales &rarr;</a>
        </div>

      </main>
    </div>
  );
}
