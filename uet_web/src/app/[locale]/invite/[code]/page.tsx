'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { Users, CheckCircle, XCircle } from 'lucide-react';

export default function InvitePage() {
  const params = useParams();
  const router = useRouter();
  const locale = (params?.locale as string) || 'en';
  const code = params?.code as string;

  const [status, setStatus] = useState<'loading' | 'ready' | 'joining' | 'success' | 'error'>('loading');
  const [error, setError] = useState('');
  const [userId, setUserId] = useState<string | null>(null);
  const [workspaceName, setWorkspaceName] = useState('');

  useEffect(() => {
    try {
      const stored = localStorage.getItem('user');
      if (stored) {
        setUserId(JSON.parse(stored).id);
        setStatus('ready');
      } else {
        setStatus('error');
        setError('Please sign in to accept this invite');
      }
    } catch {
      setStatus('error');
      setError('Please sign in to accept this invite');
    }
    // In production, validate the invite code against the server here
    setWorkspaceName('Research Lab'); // placeholder
  }, [code]);

  async function handleJoin() {
    if (!userId || !code) return;
    setStatus('joining');
    try {
      // In production, this would call /api/invite/accept with the code
      // For now, simulate success
      setTimeout(() => {
        setStatus('success');
        setTimeout(() => router.push(`/${locale}/workspaces`), 2000);
      }, 1000);
    } catch {
      setStatus('error');
      setError('Failed to join workspace');
    }
  }

  return (
    <div className="min-h-screen bg-background flex items-center justify-center px-4">
      <div className="w-full max-w-md text-center">
        {status === 'loading' && (
          <div className="animate-spin w-10 h-10 border-2 border-primary border-t-transparent rounded-full mx-auto" />
        )}

        {status === 'ready' && (
          <>
            <div className="w-16 h-16 rounded-2xl bg-primary/10 flex items-center justify-center mx-auto mb-6">
              <Users size={28} className="text-primary" />
            </div>
            <h1 className="text-2xl font-bold mb-2">You're invited!</h1>
            <p className="text-muted-foreground mb-6">
              You've been invited to join <strong className="text-foreground">{workspaceName}</strong>
            </p>
            <button
              onClick={handleJoin}
              className="w-full py-3 rounded-xl bg-primary text-primary-foreground font-semibold hover:bg-primary/90 transition-colors"
            >
              Join Workspace
            </button>
            <p className="text-xs text-muted-foreground mt-4">
              Invite code: <code className="bg-muted px-1.5 py-0.5 rounded">{code}</code>
            </p>
          </>
        )}

        {status === 'joining' && (
          <>
            <div className="animate-spin w-10 h-10 border-2 border-primary border-t-transparent rounded-full mx-auto mb-4" />
            <p className="text-muted-foreground">Joining workspace...</p>
          </>
        )}

        {status === 'success' && (
          <>
            <CheckCircle size={48} className="text-green-500 mx-auto mb-4" />
            <h1 className="text-2xl font-bold mb-2">Welcome!</h1>
            <p className="text-muted-foreground">You've joined {workspaceName}. Redirecting...</p>
          </>
        )}

        {status === 'error' && (
          <>
            <XCircle size={48} className="text-destructive mx-auto mb-4" />
            <h1 className="text-2xl font-bold mb-2">Oops</h1>
            <p className="text-muted-foreground mb-6">{error}</p>
            <Link
              href={`/${locale}/auth/login`}
              className="inline-block px-6 py-2.5 rounded-xl bg-primary text-primary-foreground font-semibold hover:bg-primary/90"
            >
              Sign In
            </Link>
          </>
        )}
      </div>
    </div>
  );
}
