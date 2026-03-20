import { notFound } from "next/navigation";
import { getDocBySlug, getDocsInCategory, getCategories, formatCategoryName } from "@/lib/docs";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import rehypeHighlight from "rehype-highlight";
import Link from "next/link";
import { ChevronRight } from "lucide-react";

import "katex/dist/katex.min.css";
import "highlight.js/styles/github-dark.css";

type Props = {
  params: Promise<{
    locale: string;
    category: string;
    slug: string;
  }>;
};

export default async function DocPage({ params }: Props) {
  const resolvedParams = await params;
  const doc = getDocBySlug(resolvedParams.category, resolvedParams.slug, resolvedParams.locale);

  if (!doc) {
    notFound();
  }

  const categoryDocs = getDocsInCategory(resolvedParams.category, resolvedParams.locale);
  const categories = getCategories();

  return (
    <div className="flex-1 max-w-4xl mx-auto px-6 py-10 w-full">
      {/* Breadcrumbs */}
      <div className="flex items-center gap-2 text-xs text-black/50 dark:text-white/50 mb-8">
        <Link href="/docs" className="hover:text-black dark:hover:text-white transition-colors">Docs</Link>
        <ChevronRight size={12} />
        <span>{doc.categoryName}</span>
        <ChevronRight size={12} />
        <span className="text-black dark:text-white font-medium">{doc.title}</span>
      </div>

      {/* Article Content */}
      <article className="prose prose-sm md:prose-base prose-slate dark:prose-invert max-w-none">
        <ReactMarkdown
          remarkPlugins={[remarkGfm, remarkMath]}
          rehypePlugins={[rehypeKatex, rehypeHighlight]}
        >
          {doc.content}
        </ReactMarkdown>
      </article>

      {/* Footer Navigation */}
      <div className="mt-16 pt-8 border-t border-black/10 dark:border-white/10 flex justify-between">
        {/* We can add previous/next links here later */}
        <div />
        <a 
          href={`https://github.com/unityequilibrium/UnityEquilibriumTheory/tree/main/research_uet/Docs/${doc.category}/${doc.slug}.md`}
          target="_blank"
          rel="noopener noreferrer"
          className="text-xs text-black/50 dark:text-white/50 hover:text-black dark:hover:text-white transition-colors"
        >
          Edit this page on GitHub
        </a>
      </div>
    </div>
  );
}
