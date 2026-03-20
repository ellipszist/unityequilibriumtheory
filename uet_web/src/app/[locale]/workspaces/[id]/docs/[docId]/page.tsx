'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, Users, Save } from 'lucide-react';
import { ThemeToggle } from '@/components/theme-toggle';
import { CollaborativeEditor } from '@/components/editor/CollaborativeEditor';

interface DocData {
  id: string;
  title: string;
  yjsDocId: string;
  updatedAt: string;
  createdBy: { id: string; displayName?: string };
}

export default function DocumentEditorPage() {
  const params = useParams();
  const locale = (params?.locale as string) || 'en';
  const wsId = params?.id as string;
  const docId = params?.docId as string;

  const [doc, setDoc] = useState<DocData | null>(null);
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (!wsId || !docId) return;
    fetch(`/api/workspaces/${wsId}/documents`)
      .then(r => r.ok ? r.json() : [])
      .then(docs => {
        const found = docs.find((d: any) => d.id === docId);
        if (found) setDoc(found);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [wsId, docId]);

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="animate-spin w-8 h-8 border-2 border-primary border-t-transparent rounded-full" />
      </div>
    );
  }

  if (!doc) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center text-muted-foreground">
        Document not found
      </div>
    );
  }

  return (
    <div className="flex flex-col h-screen bg-background text-foreground text-sm">
      {/* Header */}
      <header className="shrink-0 flex items-center justify-between h-14 px-6 border-b border-border bg-background/80 backdrop-blur-md">
        <div className="flex items-center gap-4">
          <Link href={`/${locale}/workspaces/${wsId}`} className="p-1.5 rounded-lg hover:bg-muted transition-colors">
            <ArrowLeft size={18} />
          </Link>
          <div>
            <h1 className="font-semibold">{doc.title}</h1>
            <p className="text-[10px] text-muted-foreground">
              Yjs Doc: {doc.yjsDocId.slice(0, 30)}... · Last updated {new Date(doc.updatedAt).toLocaleDateString()}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1 px-2 py-1 rounded-full bg-green-500/10 text-green-600 text-[10px] font-medium">
            <Users size={11} />
            <span>Collaborative</span>
          </div>
          <button
            onClick={() => { setSaving(true); setTimeout(() => setSaving(false), 1000); }}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-primary text-primary-foreground text-xs font-medium hover:bg-primary/90"
          >
            {saving ? <div className="animate-spin w-3.5 h-3.5 border-2 border-current border-t-transparent rounded-full" /> : <Save size={13} />}
            {saving ? 'Saving...' : 'Save'}
          </button>
          <ThemeToggle />
        </div>
      </header>

      {/* Editor area */}
      <div className="flex-1 overflow-auto">
        <div className="max-w-4xl mx-auto py-8 px-6">
          <CollaborativeEditor
            documentId={doc.yjsDocId}
            serverUrl={process.env.NEXT_PUBLIC_HOCUSPOCUS_URL || 'ws://localhost:1234'}
          />
        </div>
      </div>
    </div>
  );
}
