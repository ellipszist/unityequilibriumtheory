'use client';

import { useState } from 'react';
import { useParams } from 'next/navigation';

export default function ResetConfirmPage() {
  const params = useParams();
  const locale = (params?.locale as string) || 'en';
  const [password, setPassword] = useState('');

  async function handleConfirm(e: React.FormEvent) {
    e.preventDefault();
    alert('Password updated.');
    window.location.href = '/' + locale + '/auth/login';
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-background">
      <div className="w-full max-w-sm p-8 rounded-2xl border border-border bg-card shadow-lg">
        <h1 className="text-2xl font-bold text-center mb-6">Set New Password</h1>
        <form onSubmit={handleConfirm} className="space-y-4">
          <input type="password" placeholder="New Password" value={password} onChange={e => setPassword(e.target.value)} className="w-full px-3 py-2 rounded-xl border border-border bg-background text-sm outline-none focus:border-primary/60" required />
          <button type="submit" className="w-full py-2 rounded-xl bg-primary text-primary-foreground text-sm font-semibold hover:bg-primary/90 transition-colors">Update Password</button>
        </form>
      </div>
    </div>
  );
}
