'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';

export default function LoginPage() {
  const params = useParams();
  const locale = (params?.locale as string) || 'en';
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    localStorage.setItem('user', JSON.stringify({ id: 'user-1', email, display_name: email.split('@')[0] }));
    window.location.href = '/' + locale + '/community';
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-background">
      <div className="w-full max-w-sm p-8 rounded-2xl border border-border bg-card shadow-lg">
        <h1 className="text-2xl font-bold text-center mb-6">Sign In</h1>
        <form onSubmit={handleLogin} className="space-y-4">
          <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} className="w-full px-3 py-2 rounded-xl border border-border bg-background text-sm outline-none focus:border-primary/60" required />
          <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} className="w-full px-3 py-2 rounded-xl border border-border bg-background text-sm outline-none focus:border-primary/60" required />
          <button type="submit" className="w-full py-2 rounded-xl bg-primary text-primary-foreground text-sm font-semibold hover:bg-primary/90 transition-colors">Sign In</button>
        </form>
        <div className="mt-4 text-center text-xs text-muted-foreground space-y-1">
          <p><Link href={'/' + locale + '/auth/register'} className="text-primary hover:underline">Create account</Link></p>
          <p><Link href={'/' + locale + '/auth/reset'} className="text-primary hover:underline">Forgot password?</Link></p>
        </div>
      </div>
    </div>
  );
}
