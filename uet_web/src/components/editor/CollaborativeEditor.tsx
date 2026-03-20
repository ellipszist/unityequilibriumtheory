'use client';

import { useEditor, EditorContent } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';
import Collaboration from '@tiptap/extension-collaboration';
import Placeholder from '@tiptap/extension-placeholder';
import { HocuspocusProvider } from '@hocuspocus/provider';
import * as Y from 'yjs';
import { useEffect, useMemo, useState } from 'react';
import { Bold, Italic, Strikethrough, Heading1, Heading2, List, ListOrdered, Quote, Users } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface CollaborativeEditorProps {
  documentId: string;
  token?: string;
  serverUrl?: string;
  onSave?: (content: string) => void;
}

export function CollaborativeEditor({
  documentId,
  token,
  serverUrl = 'ws://localhost:1234',
  onSave,
}: CollaborativeEditorProps) {
  const [connected, setConnected] = useState(false);
  const [synced, setSynced] = useState(false);
  const [peerCount, setPeerCount] = useState(0);

  const ydoc = useMemo(() => new Y.Doc(), []);

  const provider = useMemo(() => {
    const p = new HocuspocusProvider({
      url: serverUrl,
      name: documentId,
      document: ydoc,
      token: token || 'anonymous',
      onConnect: () => setConnected(true),
      onDisconnect: () => setConnected(false),
      onSynced: () => setSynced(true),
      onAwarenessUpdate: ({ states }: any) => {
        setPeerCount(states.length);
      },
    });
    return p;
  }, [documentId, serverUrl, token, ydoc]);

  useEffect(() => {
    return () => {
      provider.destroy();
      ydoc.destroy();
    };
  }, [provider, ydoc]);

  const editor = useEditor({
    extensions: [
      StarterKit,
      Collaboration.configure({
        document: ydoc,
      }),
      Placeholder.configure({
        placeholder: 'Start writing collaboratively...',
      }),
    ],
    editorProps: {
      attributes: {
        class: 'prose dark:prose-invert max-w-none min-h-[400px] p-6 focus:outline-none',
      },
    },
  });

  if (!editor) return null;

  const toggleBold = () => editor.chain().focus().toggleBold().run();
  const toggleItalic = () => editor.chain().focus().toggleItalic().run();
  const toggleStrike = () => editor.chain().focus().toggleStrike().run();
  const toggleH1 = () => editor.chain().focus().toggleHeading({ level: 1 }).run();
  const toggleH2 = () => editor.chain().focus().toggleHeading({ level: 2 }).run();
  const toggleBulletList = () => editor.chain().focus().toggleBulletList().run();
  const toggleOrderedList = () => editor.chain().focus().toggleOrderedList().run();
  const toggleBlockquote = () => editor.chain().focus().toggleBlockquote().run();

  return (
    <div className="border border-border rounded-xl overflow-hidden bg-card">
      {/* Toolbar */}
      <div className="flex items-center justify-between border-b border-border p-2 bg-muted/30">
        <div className="flex flex-wrap items-center gap-1">
          <Button variant="ghost" size="sm" onClick={toggleBold}
            className={`h-8 w-8 p-0 ${editor.isActive('bold') ? 'bg-primary/10 text-primary' : ''}`}>
            <Bold size={15} />
          </Button>
          <Button variant="ghost" size="sm" onClick={toggleItalic}
            className={`h-8 w-8 p-0 ${editor.isActive('italic') ? 'bg-primary/10 text-primary' : ''}`}>
            <Italic size={15} />
          </Button>
          <Button variant="ghost" size="sm" onClick={toggleStrike}
            className={`h-8 w-8 p-0 ${editor.isActive('strike') ? 'bg-primary/10 text-primary' : ''}`}>
            <Strikethrough size={15} />
          </Button>
          <div className="w-px h-5 bg-border mx-1" />
          <Button variant="ghost" size="sm" onClick={toggleH1}
            className={`h-8 w-8 p-0 ${editor.isActive('heading', { level: 1 }) ? 'bg-primary/10 text-primary' : ''}`}>
            <Heading1 size={15} />
          </Button>
          <Button variant="ghost" size="sm" onClick={toggleH2}
            className={`h-8 w-8 p-0 ${editor.isActive('heading', { level: 2 }) ? 'bg-primary/10 text-primary' : ''}`}>
            <Heading2 size={15} />
          </Button>
          <div className="w-px h-5 bg-border mx-1" />
          <Button variant="ghost" size="sm" onClick={toggleBulletList}
            className={`h-8 w-8 p-0 ${editor.isActive('bulletList') ? 'bg-primary/10 text-primary' : ''}`}>
            <List size={15} />
          </Button>
          <Button variant="ghost" size="sm" onClick={toggleOrderedList}
            className={`h-8 w-8 p-0 ${editor.isActive('orderedList') ? 'bg-primary/10 text-primary' : ''}`}>
            <ListOrdered size={15} />
          </Button>
          <Button variant="ghost" size="sm" onClick={toggleBlockquote}
            className={`h-8 w-8 p-0 ${editor.isActive('blockquote') ? 'bg-primary/10 text-primary' : ''}`}>
            <Quote size={15} />
          </Button>
        </div>

        {/* Status indicators */}
        <div className="flex items-center gap-3 text-xs">
          <div className={`flex items-center gap-1.5 ${connected ? 'text-green-500' : 'text-muted-foreground'}`}>
            <div className={`w-1.5 h-1.5 rounded-full ${connected ? 'bg-green-500' : 'bg-muted-foreground'}`} />
            {connected ? (synced ? 'Synced' : 'Syncing...') : 'Offline'}
          </div>
          {peerCount > 1 && (
            <div className="flex items-center gap-1 text-primary">
              <Users size={12} />
              <span>{peerCount}</span>
            </div>
          )}
        </div>
      </div>

      {/* Editor */}
      <div className="max-h-[70vh] overflow-y-auto">
        <EditorContent editor={editor} />
      </div>
    </div>
  );
}
