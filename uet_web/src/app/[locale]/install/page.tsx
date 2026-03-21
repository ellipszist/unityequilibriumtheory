import Link from 'next/link';

export default function InstallPage() {
  return (
    <div className="min-h-screen bg-background flex flex-col items-center justify-center p-8">
      <div className="max-w-2xl text-center">
        <h1 className="text-4xl font-bold mb-4">Unity Equilibrium Theory</h1>
        <p className="text-lg text-muted-foreground mb-8">The academic research platform for unified theoretical physics, AI-powered collaboration, and decentralized knowledge sharing.</p>
        <div className="flex gap-4 justify-center">
          <Link href="/en/auth/register" className="px-6 py-3 rounded-xl bg-primary text-primary-foreground font-semibold hover:bg-primary/90 transition-colors">Get Started</Link>
          <Link href="/en/auth/login" className="px-6 py-3 rounded-xl bg-muted text-foreground font-semibold hover:bg-muted/80 transition-colors">Sign In</Link>
        </div>
      </div>
    </div>
  );
}
