"use client";

import { useState } from "react";
import Link from "next/link";

export default function ResetRequestPage() {
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:3001"}/api/auth/request-reset`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });

      const data = await res.json();

      // Always show success to prevent email enumeration
      setSuccess(true);
    } catch (err) {
      setError("Network error. Please try again.");
      setLoading(false);
    }
  }

  if (success) {
    return (
      <div className="min-h-screen bg-[#0a0a0f] flex items-center justify-center px-4">
        <div className="w-full max-w-md text-center">
          <div className="text-5xl mb-4">✉️</div>
          <h1 className="text-2xl font-bold text-white mb-2">Check your email</h1>
          <p className="text-white/60 mb-6">
            If an account exists with <strong className="text-white">{email}</strong>, you'll receive a reset link.
          </p>
          <Link
            href="/auth/login"
            className="text-indigo-400 hover:text-indigo-300 text-sm"
          >
            Back to Sign In
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0a0a0f] flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <Link href="/" className="text-3xl font-bold">
            <span className="bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
              ⚛ UET
            </span>
          </Link>
          <p className="text-white/50 text-sm mt-2">Reset your password</p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="rounded-xl border border-white/10 bg-white/5 p-6 space-y-4">
            {error && (
              <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-3 text-red-400 text-sm">
                {error}
              </div>
            )}

            <p className="text-white/60 text-sm">
              Enter your email address and we'll send you a link to reset your password.
            </p>

            <div>
              <label className="block text-xs font-medium text-white/70 mb-1.5">
                Email
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="w-full px-3 py-2 rounded-lg bg-black/40 border border-white/10 text-white text-sm focus:outline-none focus:border-indigo-500"
                placeholder="you@example.com"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-2.5 rounded-lg bg-gradient-to-r from-indigo-500 to-purple-500 text-white font-semibold text-sm hover:opacity-90 disabled:opacity-50"
            >
              {loading ? "Sending..." : "Send Reset Link"}
            </button>
          </div>
        </form>

        {/* Links */}
        <div className="mt-6 text-center text-sm">
          <Link href="/auth/login" className="text-indigo-400 hover:text-indigo-300">
            Back to Sign In
          </Link>
        </div>
      </div>
    </div>
  );
}
