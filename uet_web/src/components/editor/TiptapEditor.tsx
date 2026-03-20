"use client";

import { useEditor, EditorContent } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';
import Placeholder from '@tiptap/extension-placeholder';
import { Bold, Italic, Strikethrough, Heading1, Heading2, List, ListOrdered, Quote } from 'lucide-react';
import { Button } from '@/components/ui/button';

export function TiptapEditor({ 
  content, 
  onChange 
}: { 
  content?: string; 
  onChange?: (html: string) => void;
}) {
  const editor = useEditor({
    extensions: [
      StarterKit,
      Placeholder.configure({
        placeholder: 'Write something amazing...',
      }),
    ],
    content: content || '',
    onUpdate: ({ editor }) => {
      onChange?.(editor.getHTML());
    },
    editorProps: {
      attributes: {
        class: 'prose dark:prose-invert max-w-none min-h-[150px] p-4 focus:outline-none',
      },
    },
  });

  if (!editor) {
    return null;
  }

  const toggleBold = () => editor.chain().focus().toggleBold().run();
  const toggleItalic = () => editor.chain().focus().toggleItalic().run();
  const toggleStrike = () => editor.chain().focus().toggleStrike().run();
  const toggleH1 = () => editor.chain().focus().toggleHeading({ level: 1 }).run();
  const toggleH2 = () => editor.chain().focus().toggleHeading({ level: 2 }).run();
  const toggleBulletList = () => editor.chain().focus().toggleBulletList().run();
  const toggleOrderedList = () => editor.chain().focus().toggleOrderedList().run();
  const toggleBlockquote = () => editor.chain().focus().toggleBlockquote().run();

  return (
    <div className="border border-black/10 dark:border-white/10 rounded-xl overflow-hidden bg-white dark:bg-[#111] focus-within:ring-2 focus-within:ring-[#0d7a5f] transition-all">
      <div className="flex flex-wrap items-center gap-1 border-b border-black/10 dark:border-white/10 p-2 bg-black/5 dark:bg-white/5">
        <Button 
          variant="ghost" 
          size="sm" 
          onClick={toggleBold} 
          className={`h-8 w-8 p-0 ${editor.isActive('bold') ? 'bg-black/10 dark:bg-white/10' : ''}`}
        >
          <Bold size={16} />
        </Button>
        <Button 
          variant="ghost" 
          size="sm" 
          onClick={toggleItalic} 
          className={`h-8 w-8 p-0 ${editor.isActive('italic') ? 'bg-black/10 dark:bg-white/10' : ''}`}
        >
          <Italic size={16} />
        </Button>
        <Button 
          variant="ghost" 
          size="sm" 
          onClick={toggleStrike} 
          className={`h-8 w-8 p-0 ${editor.isActive('strike') ? 'bg-black/10 dark:bg-white/10' : ''}`}
        >
          <Strikethrough size={16} />
        </Button>
        
        <div className="w-px h-6 bg-black/10 dark:bg-white/10 mx-1" />

        <Button 
          variant="ghost" 
          size="sm" 
          onClick={toggleH1} 
          className={`h-8 w-8 p-0 ${editor.isActive('heading', { level: 1 }) ? 'bg-black/10 dark:bg-white/10' : ''}`}
        >
          <Heading1 size={16} />
        </Button>
        <Button 
          variant="ghost" 
          size="sm" 
          onClick={toggleH2} 
          className={`h-8 w-8 p-0 ${editor.isActive('heading', { level: 2 }) ? 'bg-black/10 dark:bg-white/10' : ''}`}
        >
          <Heading2 size={16} />
        </Button>

        <div className="w-px h-6 bg-black/10 dark:bg-white/10 mx-1" />

        <Button 
          variant="ghost" 
          size="sm" 
          onClick={toggleBulletList} 
          className={`h-8 w-8 p-0 ${editor.isActive('bulletList') ? 'bg-black/10 dark:bg-white/10' : ''}`}
        >
          <List size={16} />
        </Button>
        <Button 
          variant="ghost" 
          size="sm" 
          onClick={toggleOrderedList} 
          className={`h-8 w-8 p-0 ${editor.isActive('orderedList') ? 'bg-black/10 dark:bg-white/10' : ''}`}
        >
          <ListOrdered size={16} />
        </Button>
        <Button 
          variant="ghost" 
          size="sm" 
          onClick={toggleBlockquote} 
          className={`h-8 w-8 p-0 ${editor.isActive('blockquote') ? 'bg-black/10 dark:bg-white/10' : ''}`}
        >
          <Quote size={16} />
        </Button>
      </div>

      <div className="max-h-[400px] overflow-y-auto">
        <EditorContent editor={editor} />
      </div>
    </div>
  );
}
