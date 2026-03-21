'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';

export default function RegisterPage() {
  const params = useParams();
  const locale = (params?.locale as string) || 'en';
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  async function handleRegister(e: React.FormEvent) {
    e.preventDefault();
    alert('Registration submitted. Check your email to verify.');
    window.location.href = '/' + locale + '/auth/login';
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-background">
      <div className="w-full max-w-sm p-8 rounded-2xl border border-border bg-card shadow-lg">
        <h1 className="text-2xl font-bold text-center mb-6">Create Account</h1>
        <form onSubmit={handleRegister} className="space-y-4">
          <input type="text" placeholder="Display Name" value={name} onChange={e => setName(e.target.value)} className="w-full px-3 py-2 rounded-xl border border-border bg-background text-sm outline-none focus:border-primary/60" required />
          <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} className="w-full px-3 py-2 rounded-xl border border-border bg-background text-sm outline-none focus:border-primary/60" required />
          <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} className="w-full px-3 py-2 rounded-xl border border-border bg-background text-sm outline-none focus:border-primary/60" required />
          <button type="submit" className="w-full py-2 rounded-xl bg-primary text-primary-foreground text-sm font-semibold hover:bg-primary/90 transition-colors">Register</button>
        </form>
        <p className="mt-4 text-center text-xs text-muted-foreground">Already have an account? <Link href={'/' + locale + '/auth/login'} className="text-primary hover:underline">Sign in</Link></p>
      </div>
    </div>
  );
}
