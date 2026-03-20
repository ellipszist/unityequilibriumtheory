"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Copy, Check, Trash2, Plus, LogOut, Wallet, ArrowUpRight, ArrowDownLeft, Pickaxe, Send, RefreshCw } from "lucide-react";
import { SortableList, SortableItemType } from "@/components/dnd/SortableList";
import { ThemeToggle } from "@/components/theme-toggle";
import { LocaleSwitcher } from "@/components/locale-switcher";

interface User {
  id: string;
  email: string;
  display_name: string | null;
  avatar_url: string | null;
  is_verified: boolean;
  created_at: string;
}

interface Quota {
  tokens_used: number;
  tokens_limit: number;
  requests_used: number;
  requests_limit: number;
  period_start: string;
  plan_name: string;
}

interface ApiKey {
  id: string;
  name: string | null;
  prefix: string;
  created_at: string;
  last_used_at: string | null;
}

interface WalletData {
  id: string;
  address: string;
  balance: number;
  transactions: WalletTx[];
}

interface WalletTx {
  id: string;
  txHash: string | null;
  amount: number;
  type: string;
  status: string;
  createdAt: string;
  fromWalletId: string | null;
  toWalletId: string | null;
}

interface MiningStats {
  totalReward: number;
  totalTasksSolved: number;
  maxDifficulty: number;
}

interface ComputeLog {
  id: string;
  rustTaskId: string;
  difficulty: number;
  rewardEarned: number;
  createdAt: string;
}

const INTEGRATIONS = ["Windsurf", "Claude Code", "Cursor", "VS Code", "OpenCode", "More"];

type DashboardTab = "overview" | "wallet" | "mining";

export default function AccountDashboard() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [quota, setQuota] = useState<Quota | null>(null);
  const [apiKeys, setApiKeys] = useState<ApiKey[]>([]);
  const [loading, setLoading] = useState(true);
  const [copied, setCopied] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<"Remote" | "Local">("Remote");
  const [activeIntegration, setActiveIntegration] = useState("Windsurf");
  const [showCreateKey, setShowCreateKey] = useState(false);
  const [newKeyName, setNewKeyName] = useState("");
  const [newKey, setNewKey] = useState<string | null>(null);

  // Wallet state
  const [dashboardTab, setDashboardTab] = useState<DashboardTab>("overview");
  const [wallet, setWallet] = useState<WalletData | null>(null);
  const [walletLoading, setWalletLoading] = useState(false);
  const [sendTo, setSendTo] = useState("");
  const [sendAmount, setSendAmount] = useState("");
  const [sendStatus, setSendStatus] = useState<string | null>(null);

  // Mining state
  const [miningStats, setMiningStats] = useState<MiningStats | null>(null);
  const [computeLogs, setComputeLogs] = useState<ComputeLog[]>([]);

  const [sortableIntegrations, setSortableIntegrations] = useState<SortableItemType[]>(
    INTEGRATIONS.map((t) => ({ id: t, content: <span className="text-xs font-medium">{t}</span> }))
  );

  const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:3001";
  const DEV_MODE = process.env.NODE_ENV === "development";

  // Dev mock data for previewing UI without backend
  const mockUser: User = {
    id: "admin-001",
    email: "admin@uet-platform.com",
    display_name: "UET Admin",
    avatar_url: null,
    is_verified: true,
    created_at: new Date().toISOString(),
  };
  const mockQuota: Quota = {
    tokens_used: 12480,
    tokens_limit: 100000,
    requests_used: 47,
    requests_limit: 500,
    period_start: new Date().toISOString(),
    plan_name: "Pro",
  };
  const mockApiKeys: ApiKey[] = [
    { id: "k1", name: "Production", prefix: "uet_sk_prod_8x", created_at: "2026-01-15T00:00:00Z", last_used_at: "2026-03-14T12:00:00Z" },
    { id: "k2", name: "Dev Testing", prefix: "uet_sk_dev_3m", created_at: "2026-02-20T00:00:00Z", last_used_at: null },
  ];
  const mockWallet: WalletData = {
    id: "w1",
    address: "uet1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
    balance: 2847.56,
    transactions: [
      { id: "tx1", txHash: "0xabc123def456", amount: 150.0, type: "MINING_REWARD", status: "CONFIRMED", createdAt: "2026-03-14T10:00:00Z", fromWalletId: null, toWalletId: "w1" },
      { id: "tx2", txHash: "0x789fed012abc", amount: -50.0, type: "TRANSFER", status: "CONFIRMED", createdAt: "2026-03-13T15:30:00Z", fromWalletId: "w1", toWalletId: "w2" },
      { id: "tx3", txHash: "0xdef456789abc", amount: 200.0, type: "BOUNTY_PAYOUT", status: "CONFIRMED", createdAt: "2026-03-12T09:00:00Z", fromWalletId: null, toWalletId: "w1" },
      { id: "tx4", txHash: null, amount: -25.0, type: "TRANSFER", status: "PENDING", createdAt: "2026-03-14T14:00:00Z", fromWalletId: "w1", toWalletId: "w3" },
      { id: "tx5", txHash: "0x111222333aaa", amount: 75.0, type: "MINING_REWARD", status: "CONFIRMED", createdAt: "2026-03-11T18:45:00Z", fromWalletId: null, toWalletId: "w1" },
    ],
  };
  const mockMiningStats: MiningStats = { totalReward: 2497.56, totalTasksSolved: 1832, maxDifficulty: 14 };
  const mockComputeLogs: ComputeLog[] = [
    { id: "cl1", rustTaskId: "eq-cert-7f3a9b2c", difficulty: 12, rewardEarned: 3.2, createdAt: "2026-03-14T13:45:00Z" },
    { id: "cl2", rustTaskId: "det-sim-a1b2c3d4", difficulty: 14, rewardEarned: 5.8, createdAt: "2026-03-14T12:30:00Z" },
    { id: "cl3", rustTaskId: "opt-bnd-e5f6a7b8", difficulty: 10, rewardEarned: 2.1, createdAt: "2026-03-14T11:15:00Z" },
    { id: "cl4", rustTaskId: "eq-cert-c9d0e1f2", difficulty: 11, rewardEarned: 2.9, createdAt: "2026-03-14T09:00:00Z" },
    { id: "cl5", rustTaskId: "det-sim-34567890", difficulty: 13, rewardEarned: 4.5, createdAt: "2026-03-13T22:10:00Z" },
  ];

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    // Dev bypass: auto-login with mock data if backend is not available
    if (DEV_MODE && !token) {
      localStorage.setItem("access_token", "dev_mock_token");
      localStorage.setItem("user", JSON.stringify(mockUser));
    }

    fetchData();
  }, [router]);

  useEffect(() => {
    if (user && dashboardTab === "wallet") {
      fetchWallet();
    }
    if (user && dashboardTab === "mining") {
      fetchMining();
    }
  }, [dashboardTab, user]);

  async function fetchData() {
    // In dev mode, try backend but fall back to mock data immediately on any error
    if (DEV_MODE) {
      try {
        const token = localStorage.getItem("access_token");
        const headers = { Authorization: `Bearer ${token}` };
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 2000);

        const userRes = await fetch(`${API_BASE}/api/auth/me`, { headers, signal: controller.signal });
        clearTimeout(timeout);

        if (userRes.ok) {
          const [quotaRes, keysRes] = await Promise.all([
            fetch(`${API_BASE}/api/auth/quota`, { headers }),
            fetch(`${API_BASE}/api/auth/api-keys`, { headers }),
          ]);
          setUser(await userRes.json());
          setQuota(await quotaRes.json());
          setApiKeys(await keysRes.json());
          setLoading(false);
          return;
        }
      } catch {
        // Backend unreachable — use mock data silently
      }
      setUser(mockUser);
      setQuota(mockQuota);
      setApiKeys(mockApiKeys);
      setLoading(false);
      return;
    }

    // Production mode
    try {
      const token = localStorage.getItem("access_token");
      const headers = { Authorization: `Bearer ${token}` };

      const [userRes, quotaRes, keysRes] = await Promise.all([
        fetch(`${API_BASE}/api/auth/me`, { headers }),
        fetch(`${API_BASE}/api/auth/quota`, { headers }),
        fetch(`${API_BASE}/api/auth/api-keys`, { headers }),
      ]);

      if (!userRes.ok) {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        localStorage.removeItem("user");
        router.push("/auth/login");
        return;
      }

      setUser(await userRes.json());
      setQuota(await quotaRes.json());
      setApiKeys(await keysRes.json());
    } catch (err) {
      console.error("Failed to fetch data:", err);
    } finally {
      setLoading(false);
    }
  }

  async function fetchWallet() {
    if (!user) return;
    setWalletLoading(true);
    try {
      const res = await fetch(`/api/wallet?userId=${user.id}`);
      if (res.ok) {
        const data = await res.json();
        setWallet(data);
      } else if (DEV_MODE) {
        setWallet(mockWallet);
      }
    } catch (err) {
      console.error("Failed to fetch wallet:", err);
      if (DEV_MODE) setWallet(mockWallet);
    } finally {
      setWalletLoading(false);
    }
  }

  async function fetchMining() {
    if (!user) return;
    try {
      const res = await fetch(`/api/compute?userId=${user.id}`);
      if (res.ok) {
        const data = await res.json();
        setMiningStats(data.stats);
        setComputeLogs(data.logs);
      } else if (DEV_MODE) {
        setMiningStats(mockMiningStats);
        setComputeLogs(mockComputeLogs);
      }
    } catch (err) {
      console.error("Failed to fetch mining:", err);
      if (DEV_MODE) {
        setMiningStats(mockMiningStats);
        setComputeLogs(mockComputeLogs);
      }
    }
  }

  async function handleSend() {
    if (!sendTo || !sendAmount || !user) return;
    setSendStatus("sending");
    try {
      const res = await fetch("/api/wallet/transfer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          fromUserId: user.id,
          toUserId: sendTo,
          amount: parseFloat(sendAmount),
        }),
      });
      if (res.ok) {
        setSendStatus("success");
        setSendTo("");
        setSendAmount("");
        fetchWallet();
        setTimeout(() => setSendStatus(null), 3000);
      } else {
        const err = await res.json();
        setSendStatus(`error: ${err.error}`);
        setTimeout(() => setSendStatus(null), 4000);
      }
    } catch {
      setSendStatus("error: Network error");
      setTimeout(() => setSendStatus(null), 4000);
    }
  }

  function copy(text: string, key: string) {
    navigator.clipboard.writeText(text);
    setCopied(key);
    setTimeout(() => setCopied(null), 2000);
  }

  async function createApiKey() {
    const token = localStorage.getItem("access_token");
    const res = await fetch(`${API_BASE}/api/auth/api-keys`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ name: newKeyName || null }),
    });

    if (res.ok) {
      const data = await res.json();
      setNewKey(data.key);
      setNewKeyName("");
      setShowCreateKey(false);
      fetchData();
    }
  }

  async function deleteApiKey(id: string) {
    if (!confirm("Delete this API key?")) return;

    const token = localStorage.getItem("access_token");
    const res = await fetch(`${API_BASE}/api/auth/api-keys/${id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });

    if (res.ok) {
      fetchData();
    }
  }

  function logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user");
    router.push("/");
  }

  const mcpUrl = "mcp.uet-platform.com/mcp";
  const apiUrl = "uet-platform.com/api/v1";

  const remoteSnippets: Record<string, string> = {
    "Windsurf":
      `windsurf mcp add --scope user --transport http uet \\\n  https://mcp.uet-platform.com/mcp \\\n  --header "UET_API_KEY: YOUR_API_KEY"`,
    "Claude Code":
      `claude mcp add --scope user --transport http uet \\\n  https://mcp.uet-platform.com/mcp \\\n  --header "UET_API_KEY: YOUR_API_KEY"`,
    "Cursor":
      `# Add to ~/.cursor/mcp.json\n{\n  "uet": {\n    "url": "https://mcp.uet-platform.com/mcp",\n    "headers": { "UET_API_KEY": "YOUR_API_KEY" }\n  }\n}`,
    "VS Code":
      `# Add to .vscode/mcp.json\n{\n  "uet": {\n    "url": "https://mcp.uet-platform.com/mcp",\n    "headers": { "UET_API_KEY": "YOUR_API_KEY" }\n  }\n}`,
    "OpenCode":
      `opencode mcp add uet https://mcp.uet-platform.com/mcp \\\n  --header "UET_API_KEY: YOUR_API_KEY"`,
    "More": `# See docs for all integration guides\ncurl https://uet-platform.com/api/v1/knowledge/search`,
  };

  const snippet = remoteSnippets[activeIntegration];

  if (loading) {
    return (
      <div className="min-h-screen bg-white dark:bg-[#0a0a0f] flex items-center justify-center">
        <div className="animate-spin w-8 h-8 border-2 border-[#0d7a5f] border-t-transparent rounded-full"></div>
      </div>
    );
  }

  const usagePercent = quota ? (quota.requests_used / quota.requests_limit) * 100 : 0;
  const initials = user?.display_name?.[0]?.toUpperCase() || user?.email?.[0]?.toUpperCase() || "U";

  return (
    <div className="min-h-screen bg-white dark:bg-[#0a0a0f] text-black dark:text-white text-sm">
      {/* Header */}
      <header className="flex items-center h-14 px-6 border-b border-black/10 dark:border-white/10 bg-white/90 dark:bg-[#0a0a0f]/90 backdrop-blur-md">
        <Link href="/" className="flex items-center gap-2 font-bold text-base">
          <img src="/logo.png" alt="UET Logo" className="w-8 h-8 object-contain" />
          UET Platform
        </Link>
        <nav className="ml-8 flex items-center gap-1 text-xs">
          {([
            { key: "overview", label: "Overview" },
            { key: "wallet", label: "Wallet" },
            { key: "mining", label: "Mining" },
          ] as const).map((tab) => (
            <button
              key={tab.key}
              onClick={() => setDashboardTab(tab.key)}
              className={`px-3 py-1.5 rounded-md transition-colors ${
                dashboardTab === tab.key
                  ? "text-[#0d7a5f] dark:text-[#2dd4bf] font-semibold bg-[#0d7a5f]/10 dark:bg-[#2dd4bf]/10"
                  : "text-black/50 dark:text-white/50 hover:text-black dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/5"
              }`}
            >
              {tab.label}
            </button>
          ))}
          <span className="mx-2 w-px h-4 bg-black/10 dark:bg-white/10" />
          <Link href="/docs" className="px-3 py-1.5 rounded-md text-black/50 dark:text-white/50 hover:text-black dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/5 transition-colors">Docs</Link>
        </nav>
        <div className="ml-auto flex items-center gap-3">
          <LocaleSwitcher />
          <ThemeToggle />
          <div className="w-7 h-7 rounded-full bg-gradient-to-br from-[#0d7a5f] to-emerald-600 flex items-center justify-center text-white text-xs font-bold ml-2">
            {initials}
          </div>
          <button onClick={logout} className="p-1.5 rounded hover:bg-black/5 dark:hover:bg-white/10 text-black/40 dark:text-white/40 hover:text-red-500 dark:hover:text-red-400">
            <LogOut size={14} />
          </button>
        </div>
      </header>

      <main className="max-w-2xl mx-auto py-10 px-4 space-y-6">

        {/* ==================== OVERVIEW TAB ==================== */}
        {dashboardTab === "overview" && (
          <>
            {/* Stats bar */}
            <div className="rounded-xl border border-black/10 dark:border-white/10 bg-black/5 dark:bg-white/5 p-5">
              <div className="grid grid-cols-4 divide-x divide-black/10">
                {[
                  { label: "REQUESTS", value: quota ? `${quota.requests_used}/${quota.requests_limit}` : "0/100" },
                  { label: "TOKENS", value: quota ? quota.tokens_used.toLocaleString() : "0" },
                  { label: "PLAN", value: quota?.plan_name || "Free" },
                  { label: "EMAIL", value: user?.email?.split("@")[0] || "—" },
                ].map(({ label, value }) => (
                  <div key={label} className="px-5 first:pl-0 last:pr-0">
                    <p className="text-[10px] font-semibold tracking-widest text-black/40 uppercase mb-1">{label}</p>
                    <p className="text-xl font-bold truncate">{value}</p>
                  </div>
                ))}
              </div>
              {/* Request progress bar */}
              <div className="mt-4">
                <div className="w-full h-1 rounded-full bg-black/10 overflow-hidden">
                  <div className="h-1 bg-[#0d7a5f] rounded-full transition-all" style={{ width: `${Math.min(usagePercent, 100)}%` }} />
                </div>
              </div>
            </div>

            {/* API Keys */}
            <div className="rounded-xl border border-black/10 dark:border-white/10 bg-black/5 dark:bg-white/5 p-5">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h2 className="font-semibold text-base">API Keys</h2>
                  <p className="text-xs text-black/40 dark:text-white/40 mt-0.5">Manage your API keys to authenticate MCP queries</p>
                </div>
                <button
                  onClick={() => setShowCreateKey(true)}
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-[#0d7a5f] text-[#0d7a5f] dark:text-[#2dd4bf] dark:border-[#2dd4bf] hover:bg-[#0d7a5f]/5 dark:hover:bg-[#2dd4bf]/10 text-xs font-medium transition-colors"
                >
                  <Plus size={13} /> Create API Key
                </button>
              </div>

              {/* New key display */}
              {newKey && (
                <div className="mb-4 p-3 rounded-lg bg-green-50 dark:bg-green-500/10 border border-green-200 dark:border-green-500/20">
                  <p className="text-xs text-green-700 dark:text-green-400 font-medium mb-1">Your new API key (copy it now!):</p>
                  <div className="flex items-center gap-2">
                    <code className="flex-1 text-xs font-mono bg-white dark:bg-black/50 px-2 py-1 rounded border border-green-200 dark:border-green-500/20 text-green-800 dark:text-green-300">{newKey}</code>
                    <button onClick={() => { copy(newKey, "newkey"); }} className="p-1 hover:bg-green-100 dark:hover:bg-green-500/20 text-green-700 dark:text-green-400 rounded">
                      {copied === "newkey" ? <Check size={14} /> : <Copy size={14} />}
                    </button>
                  </div>
                </div>
              )}

              {/* Create key modal */}
              {showCreateKey && (
                <div className="mb-4 p-4 rounded-lg bg-white dark:bg-[#1a1a24] border border-black/10 dark:border-white/10">
                  <input
                    type="text"
                    value={newKeyName}
                    onChange={(e) => setNewKeyName(e.target.value)}
                    placeholder="Key name (optional)"
                    className="w-full px-3 py-2 rounded-lg border border-black/10 dark:border-white/10 bg-transparent text-sm mb-2 focus:outline-none focus:border-[#0d7a5f] dark:focus:border-[#2dd4bf]"
                  />
                  <div className="flex gap-2">
                    <button onClick={createApiKey} className="px-4 py-1.5 rounded-lg bg-[#0d7a5f] hover:bg-[#0b644d] text-white text-xs font-medium transition-colors">
                      Create
                    </button>
                    <button onClick={() => setShowCreateKey(false)} className="px-4 py-1.5 rounded-lg text-xs text-black/60 dark:text-white/60 hover:bg-black/5 dark:hover:bg-white/5 transition-colors">
                      Cancel
                    </button>
                  </div>
                </div>
              )}

              {/* Table header */}
              <div className="grid grid-cols-[2fr_2fr_2fr_2fr_auto] gap-2 px-2 pb-2 border-b border-black/10 dark:border-white/10 text-[10px] font-semibold tracking-widest text-black/40 dark:text-white/40 uppercase">
                <span>Name</span>
                <span>Key</span>
                <span>Created</span>
                <span>Last Used</span>
                <span />
              </div>

              {apiKeys.length === 0 ? (
                <p className="text-center text-black/40 dark:text-white/40 py-8 text-xs">No API keys yet. Create one to get started.</p>
              ) : (
                apiKeys.map((k) => (
                  <div key={k.id} className="grid grid-cols-[2fr_2fr_2fr_2fr_auto] gap-2 px-2 py-3 border-b border-black/5 dark:border-white/5 last:border-0 items-center">
                    <span className="font-medium text-xs">{k.name || "—"}</span>
                    <span className="font-mono text-xs bg-black/5 dark:bg-white/10 px-2 py-0.5 rounded">{k.prefix}...</span>
                    <span className="text-xs text-black/50 dark:text-white/50">{new Date(k.created_at).toLocaleDateString()}</span>
                    <span className="text-xs text-black/50 dark:text-white/50">{k.last_used_at ? new Date(k.last_used_at).toLocaleDateString() : "Never"}</span>
                    <button
                      onClick={() => deleteApiKey(k.id)}
                      className="p-1 rounded hover:bg-black/5 dark:hover:bg-white/10 text-black/30 dark:text-white/30 hover:text-red-500 dark:hover:text-red-400 transition-colors"
                    >
                      <Trash2 size={13} />
                    </button>
                  </div>
                ))
              )}
            </div>

            {/* Connect & Integrations (Drag and Drop) */}
            <div className="rounded-xl border border-black/10 dark:border-white/10 bg-black/5 dark:bg-white/5 p-5">
              <h2 className="font-semibold text-base mb-0.5">Integrations (Reorderable)</h2>
              <p className="text-xs text-black/40 dark:text-white/40 mb-4">Drag to prioritize your favorite tools</p>
              
              <SortableList 
                items={sortableIntegrations} 
                onReorder={setSortableIntegrations} 
              />

              <div className="mt-6 space-y-2">
                <h2 className="font-semibold text-base mb-0.5">Connection Details</h2>
                <Link href="/docs" className="text-xs text-[#0d7a5f] dark:text-[#2dd4bf] hover:underline">Check the docs</Link>
                <span className="text-xs text-black/40 dark:text-white/40"> for installation</span>

                {/* URL rows */}
                <div className="mt-4 space-y-2">
                  {[
                    { label: "MCP URL", value: mcpUrl },
                    { label: "API URL", value: apiUrl },
                  ].map(({ label, value }) => (
                    <div key={label} className="flex items-center gap-3 rounded-lg bg-white dark:bg-black/50 px-4 py-2.5 border border-black/5 dark:border-white/5">
                      <span className="text-[10px] font-semibold text-black/40 dark:text-white/40 w-16 shrink-0">{label}</span>
                      <span className="text-xs font-mono flex-1 text-black/70 dark:text-white/70">: {value}</span>
                      <button
                        onClick={() => copy(value, label)}
                        className="p-1 rounded hover:bg-black/5 dark:hover:bg-white/10 text-black/30 dark:text-white/30 hover:text-black dark:hover:text-white transition-colors"
                      >
                        {copied === label ? <Check size={13} className="text-green-600 dark:text-green-400" /> : <Copy size={13} />}
                      </button>
                    </div>
                  ))}
                </div>

                {/* Integration tabs */}
                <div className="flex items-center gap-2 mt-4">
                  {(["Remote", "Local"] as const).map((t) => (
                    <button
                      key={t}
                      onClick={() => setActiveTab(t)}
                      className={`px-4 py-1.5 rounded-full text-xs font-semibold transition-colors ${
                        activeTab === t
                          ? "bg-black dark:bg-white text-white dark:text-black shadow-sm"
                          : "bg-white/50 dark:bg-white/5 text-black/60 dark:text-white/60 hover:bg-black/5 hover:text-black dark:hover:bg-white/10 dark:hover:text-white border border-black/5 dark:border-white/5"
                      }`}
                    >
                      {t}
                    </button>
                  ))}
                </div>

                {/* Code snippet */}
                <div className="mt-3 relative rounded-lg bg-[#0a0a0f] border border-black/10 dark:border-white/10 overflow-hidden">
                  <pre className="p-4 text-xs text-[#2dd4bf] font-mono overflow-x-auto whitespace-pre">{snippet}</pre>
                  <button
                    onClick={() => copy(snippet, "snippet")}
                    className="absolute top-2 right-2 p-1.5 rounded hover:bg-white/10 text-white/40 hover:text-white transition-colors"
                  >
                    {copied === "snippet" ? <Check size={14} className="text-[#2dd4bf]" /> : <Copy size={14} />}
                  </button>
                </div>
              </div>
            </div>
          </>
        )}

        {/* ==================== WALLET TAB ==================== */}
        {dashboardTab === "wallet" && (
          <>
            {/* Balance Card */}
            <div className="rounded-xl border border-black/10 dark:border-white/10 bg-gradient-to-br from-[#0d7a5f]/10 to-emerald-500/5 dark:from-[#0d7a5f]/20 dark:to-emerald-500/10 p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-[#0d7a5f] flex items-center justify-center">
                    <Wallet size={18} className="text-white" />
                  </div>
                  <div>
                    <p className="text-[10px] font-semibold tracking-widest text-black/40 dark:text-white/40 uppercase">Uet-Cash Balance</p>
                    <p className="text-3xl font-extrabold text-[#0d7a5f] dark:text-[#2dd4bf]">
                      {walletLoading ? "..." : wallet ? wallet.balance.toLocaleString(undefined, { minimumFractionDigits: 2 }) : "0.00"}
                      <span className="text-sm font-medium ml-1.5 text-black/40 dark:text-white/40">UET</span>
                    </p>
                  </div>
                </div>
                <button onClick={fetchWallet} className="p-2 rounded-lg hover:bg-black/5 dark:hover:bg-white/5 text-black/40 dark:text-white/40 hover:text-black dark:hover:text-white transition-colors">
                  <RefreshCw size={14} className={walletLoading ? "animate-spin" : ""} />
                </button>
              </div>

              {/* Address */}
              {wallet && (
                <div className="flex items-center gap-2 mt-2 p-2.5 rounded-lg bg-white/60 dark:bg-black/30 border border-black/5 dark:border-white/5">
                  <span className="text-[10px] font-semibold text-black/40 dark:text-white/40 w-14 shrink-0">ADDRESS</span>
                  <span className="text-xs font-mono flex-1 text-black/60 dark:text-white/60 truncate">{wallet.address}</span>
                  <button onClick={() => copy(wallet.address, "addr")} className="p-1 rounded hover:bg-black/5 dark:hover:bg-white/10 text-black/30 dark:text-white/30">
                    {copied === "addr" ? <Check size={13} className="text-green-500" /> : <Copy size={13} />}
                  </button>
                </div>
              )}
            </div>

            {/* Send UET */}
            <div className="rounded-xl border border-black/10 dark:border-white/10 bg-black/5 dark:bg-white/5 p-5">
              <h2 className="font-semibold text-base mb-3 flex items-center gap-2">
                <Send size={14} className="text-[#0d7a5f] dark:text-[#2dd4bf]" />
                Send Uet-Cash
              </h2>
              <div className="space-y-3">
                <input
                  type="text"
                  value={sendTo}
                  onChange={(e) => setSendTo(e.target.value)}
                  placeholder="Recipient User ID or Address"
                  className="w-full px-3 py-2.5 rounded-lg border border-black/10 dark:border-white/10 bg-white dark:bg-black/50 text-sm focus:outline-none focus:border-[#0d7a5f] dark:focus:border-[#2dd4bf] placeholder:text-black/30 dark:placeholder:text-white/30"
                />
                <div className="flex gap-2">
                  <input
                    type="number"
                    value={sendAmount}
                    onChange={(e) => setSendAmount(e.target.value)}
                    placeholder="Amount"
                    min="0"
                    step="0.01"
                    className="flex-1 px-3 py-2.5 rounded-lg border border-black/10 dark:border-white/10 bg-white dark:bg-black/50 text-sm focus:outline-none focus:border-[#0d7a5f] dark:focus:border-[#2dd4bf] placeholder:text-black/30 dark:placeholder:text-white/30"
                  />
                  <button
                    onClick={handleSend}
                    disabled={!sendTo || !sendAmount || sendStatus === "sending"}
                    className="px-5 py-2.5 rounded-lg bg-[#0d7a5f] hover:bg-[#0b644d] disabled:opacity-40 disabled:cursor-not-allowed text-white text-xs font-semibold transition-colors flex items-center gap-1.5"
                  >
                    {sendStatus === "sending" ? <RefreshCw size={13} className="animate-spin" /> : <ArrowUpRight size={13} />}
                    Send
                  </button>
                </div>
                {sendStatus === "success" && (
                  <p className="text-xs text-green-600 dark:text-green-400 font-medium">Transfer successful!</p>
                )}
                {sendStatus?.startsWith("error") && (
                  <p className="text-xs text-red-500 font-medium">{sendStatus}</p>
                )}
              </div>
            </div>

            {/* Transaction History */}
            <div className="rounded-xl border border-black/10 dark:border-white/10 bg-black/5 dark:bg-white/5 p-5">
              <h2 className="font-semibold text-base mb-3">Transaction History</h2>

              {!wallet || wallet.transactions.length === 0 ? (
                <p className="text-center text-black/40 dark:text-white/40 py-8 text-xs">No transactions yet</p>
              ) : (
                <div className="space-y-1">
                  {wallet.transactions.map((tx) => {
                    const isIncoming = tx.amount > 0;
                    return (
                      <div key={tx.id} className="flex items-center gap-3 p-3 rounded-lg hover:bg-white/50 dark:hover:bg-white/5 transition-colors">
                        <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                          isIncoming 
                            ? "bg-green-100 dark:bg-green-500/20 text-green-600 dark:text-green-400"
                            : "bg-red-100 dark:bg-red-500/20 text-red-500 dark:text-red-400"
                        }`}>
                          {isIncoming ? <ArrowDownLeft size={14} /> : <ArrowUpRight size={14} />}
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="text-xs font-medium">{tx.type.replace("_", " ")}</p>
                          <p className="text-[10px] text-black/40 dark:text-white/40 truncate">{tx.txHash || tx.id.slice(0, 16)}</p>
                        </div>
                        <div className="text-right">
                          <p className={`text-sm font-bold ${isIncoming ? "text-green-600 dark:text-green-400" : "text-red-500 dark:text-red-400"}`}>
                            {isIncoming ? "+" : ""}{tx.amount.toLocaleString(undefined, { minimumFractionDigits: 2 })}
                          </p>
                          <p className="text-[10px] text-black/40 dark:text-white/40">{new Date(tx.createdAt).toLocaleDateString()}</p>
                        </div>
                        <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${
                          tx.status === "CONFIRMED" 
                            ? "bg-green-100 dark:bg-green-500/20 text-green-700 dark:text-green-400"
                            : tx.status === "FAILED"
                            ? "bg-red-100 dark:bg-red-500/20 text-red-600 dark:text-red-400"
                            : "bg-yellow-100 dark:bg-yellow-500/20 text-yellow-700 dark:text-yellow-400"
                        }`}>
                          {tx.status}
                        </span>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          </>
        )}

        {/* ==================== MINING TAB ==================== */}
        {dashboardTab === "mining" && (
          <>
            {/* Mining Stats */}
            <div className="rounded-xl border border-black/10 dark:border-white/10 bg-gradient-to-br from-amber-500/10 to-orange-500/5 dark:from-amber-500/20 dark:to-orange-500/10 p-6">
              <div className="flex items-center gap-3 mb-5">
                <div className="w-10 h-10 rounded-full bg-amber-500 flex items-center justify-center">
                  <Pickaxe size={18} className="text-white" />
                </div>
                <div>
                  <p className="text-[10px] font-semibold tracking-widest text-black/40 dark:text-white/40 uppercase">Proof-of-Useful-Work</p>
                  <p className="text-base font-semibold">Mining Dashboard</p>
                </div>
              </div>
              <div className="grid grid-cols-3 gap-4">
                {[
                  { label: "TOTAL EARNED", value: `${miningStats?.totalReward?.toLocaleString(undefined, { minimumFractionDigits: 2 }) || "0.00"} UET`, color: "text-amber-600 dark:text-amber-400" },
                  { label: "TASKS SOLVED", value: miningStats?.totalTasksSolved?.toLocaleString() || "0", color: "text-[#0d7a5f] dark:text-[#2dd4bf]" },
                  { label: "MAX DIFFICULTY", value: miningStats?.maxDifficulty?.toString() || "0", color: "text-purple-600 dark:text-purple-400" },
                ].map(({ label, value, color }) => (
                  <div key={label} className="rounded-lg bg-white/60 dark:bg-black/30 border border-black/5 dark:border-white/5 p-4 text-center">
                    <p className="text-[10px] font-semibold tracking-widest text-black/40 dark:text-white/40 uppercase mb-1">{label}</p>
                    <p className={`text-xl font-bold ${color}`}>{value}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Recent Compute Logs */}
            <div className="rounded-xl border border-black/10 dark:border-white/10 bg-black/5 dark:bg-white/5 p-5">
              <h2 className="font-semibold text-base mb-3">Recent Compute Logs</h2>

              {computeLogs.length === 0 ? (
                <p className="text-center text-black/40 dark:text-white/40 py-8 text-xs">No compute logs yet. Start mining to earn Uet-Cash!</p>
              ) : (
                <div className="space-y-1">
                  <div className="grid grid-cols-[2fr_1fr_1fr_1.5fr] gap-2 px-3 pb-2 border-b border-black/10 dark:border-white/10 text-[10px] font-semibold tracking-widest text-black/40 dark:text-white/40 uppercase">
                    <span>Task ID</span>
                    <span>Difficulty</span>
                    <span>Reward</span>
                    <span>Date</span>
                  </div>
                  {computeLogs.slice(0, 20).map((log) => (
                    <div key={log.id} className="grid grid-cols-[2fr_1fr_1fr_1.5fr] gap-2 px-3 py-2.5 rounded-lg hover:bg-white/50 dark:hover:bg-white/5 transition-colors items-center">
                      <span className="text-xs font-mono truncate text-black/70 dark:text-white/70">{log.rustTaskId}</span>
                      <span className="text-xs">
                        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-purple-100 dark:bg-purple-500/20 text-purple-700 dark:text-purple-400 text-[10px] font-semibold">
                          Lv.{log.difficulty}
                        </span>
                      </span>
                      <span className="text-xs font-bold text-amber-600 dark:text-amber-400">+{log.rewardEarned}</span>
                      <span className="text-xs text-black/50 dark:text-white/50">{new Date(log.createdAt).toLocaleString()}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </>
        )}

      </main>
    </div>
  );
}
