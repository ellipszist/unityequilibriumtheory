import AppShell from '@/components/layout/AppShell';

export default function ManualPage() {
  return (
    <AppShell>
      <div className="flex-1 flex overflow-hidden">
        <aside className="w-56 border-r border-border bg-muted/30 overflow-y-auto hidden md:flex flex-col p-4">
          <h2 className="font-bold text-sm mb-4">Manual</h2>
          <nav className="space-y-1 text-xs">
            <a href="#" className="block px-2 py-1.5 rounded-md bg-primary/10 text-primary">Getting Started</a>
            <a href="#" className="block px-2 py-1.5 rounded-md hover:bg-muted text-muted-foreground">Platform Overview</a>
            <a href="#" className="block px-2 py-1.5 rounded-md hover:bg-muted text-muted-foreground">WorkChat Guide</a>
            <a href="#" className="block px-2 py-1.5 rounded-md hover:bg-muted text-muted-foreground">Community Guide</a>
            <a href="#" className="block px-2 py-1.5 rounded-md hover:bg-muted text-muted-foreground">Project Guide</a>
            <a href="#" className="block px-2 py-1.5 rounded-md hover:bg-muted text-muted-foreground">Economy & Credits</a>
          </nav>
        </aside>
        <main className="flex-1 p-8 overflow-y-auto">
          <h1 className="text-2xl font-bold mb-4">Getting Started</h1>
          <p className="text-sm text-muted-foreground">Welcome to the UET Platform documentation. This manual covers all platform features.</p>
        </main>
      </div>
    </AppShell>
  );
}
