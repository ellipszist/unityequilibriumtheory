'use client';

import { useParams } from 'next/navigation';
import Link from 'next/link';

export default function VerifyPage() {
  const params = useParams();
  const locale = (params?.locale as string) || 'en';

  return (
    <div className="min-h-screen flex items-center justify-center bg-background">
      <div className="w-full max-w-sm p-8 rounded-2xl border border-border bg-card shadow-lg text-center">
        <h1 className="text-2xl font-bold mb-4">Email Verified</h1>
        <p className="text-sm text-muted-foreground mb-6">Your email has been verified successfully.</p>
        <Link href={'/' + locale + '/auth/login'} className="px-4 py-2 rounded-xl bg-primary text-primary-foreground text-sm font-semibold hover:bg-primary/90 transition-colors">Sign In</Link>
      </div>
    </div>
  );
}
