'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';

export default function ResetPage() {
  const params = useParams();
  const locale = (params?.locale as string) || 'en';
  const [email, setEmail] = useState('');

  async function handleReset(e: React.FormEvent) {
    e.preventDefault();
    alert('Password reset email sent.');
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-background">
      <div className="w-full max-w-sm p-8 rounded-2xl border border-border bg-card shadow-lg">
        <h1 className="text-2xl font-bold text-center mb-6">Reset Password</h1>
        <form onSubmit={handleReset} className="space-y-4">
          <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} className="w-full px-3 py-2 rounded-xl border border-border bg-background text-sm outline-none focus:border-primary/60" required />
          <button type="submit" className="w-full py-2 rounded-xl bg-primary text-primary-foreground text-sm font-semibold hover:bg-primary/90 transition-colors">Send Reset Link</button>
        </form>
        <p className="mt-4 text-center text-xs text-muted-foreground"><Link href={'/' + locale + '/auth/login'} className="text-primary hover:underline">Back to sign in</Link></p>
      </div>
    </div>
  );
}
