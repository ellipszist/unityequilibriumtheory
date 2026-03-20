"use client"

import * as React from "react"
import { Search } from "lucide-react"
import { useRouter } from "@/i18n/routing"
import { useLocale } from "next-intl"
import Fuse from "fuse.js"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"

type SearchResult = {
  title: string
  categoryName: string
  slug: string
  category: string
}

export function DocSearch() {
  const [open, setOpen] = React.useState(false)
  const [query, setQuery] = React.useState("")
  const [results, setResults] = React.useState<SearchResult[]>([])
  const [fuse, setFuse] = React.useState<Fuse<any> | null>(null)
  
  const router = useRouter()
  const locale = useLocale()

  React.useEffect(() => {
    // Fetch all docs for searching when component mounts
    fetch(`/api/docs?locale=${locale}`)
      .then(res => res.json())
      .then(data => {
        const fuseInstance = new Fuse(data, {
          keys: ['title', 'description', 'content'],
          threshold: 0.3,
          includeScore: true
        })
        setFuse(fuseInstance)
      })
      .catch(err => console.error("Failed to load search index", err))
  }, [locale])

  React.useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === "/" && (e.metaKey || e.ctrlKey || !e.target || (e.target as HTMLElement).tagName !== 'INPUT')) {
        e.preventDefault()
        setOpen((open) => !open)
      }
    }
    document.addEventListener("keydown", down)
    return () => document.removeEventListener("keydown", down)
  }, [])

  React.useEffect(() => {
    if (fuse && query.trim().length > 1) {
      const searchResults = fuse.search(query).slice(0, 8).map(r => r.item)
      setResults(searchResults)
    } else {
      setResults([])
    }
  }, [query, fuse])

  const handleSelect = (category: string, slug: string) => {
    setOpen(false)
    router.push(`/docs/${category}/${slug}`)
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger>
        <div className="relative group max-w-sm w-full cursor-text">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-black/40 dark:text-white/40" size={14} />
          <div className="flex items-center w-full h-8 pl-9 pr-12 rounded-md bg-black/5 dark:bg-black/30 border border-black/10 dark:border-white/10 text-xs text-black/50 dark:text-white/50 hover:border-black/30 dark:hover:border-white/30 transition-colors">
            Search documentation...
          </div>
          <kbd className="absolute right-2 top-1/2 -translate-y-1/2 px-1.5 py-0.5 rounded bg-black/10 dark:bg-white/10 text-[10px] text-black/50 dark:text-white/50 font-mono">
            /
          </kbd>
        </div>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[500px] p-0 gap-0 overflow-hidden">
        <DialogHeader className="p-4 pb-0">
          <DialogTitle className="sr-only">Search Documentation</DialogTitle>
          <div className="relative flex items-center w-full">
            <Search className="absolute left-3 text-black/40 dark:text-white/40" size={16} />
            <input
              autoFocus
              className="w-full h-10 pl-10 pr-4 text-sm bg-transparent border-b border-black/10 dark:border-white/10 focus:outline-none text-black dark:text-white placeholder:text-black/40 dark:placeholder:text-white/40"
              placeholder="Search..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
          </div>
        </DialogHeader>
        <div className="max-h-[300px] overflow-y-auto p-2">
          {results.length === 0 && query.trim().length > 0 && (
            <p className="p-4 text-sm text-center text-black/50 dark:text-white/50">
              No results found.
            </p>
          )}
          {results.map((result, i) => (
            <button
              key={`${result.category}-${result.slug}-${i}`}
              className="w-full flex flex-col items-start px-4 py-2 text-left hover:bg-black/5 dark:hover:bg-white/10 rounded-md transition-colors"
              onClick={() => handleSelect(result.category, result.slug)}
            >
              <span className="text-sm font-medium text-black dark:text-white">{result.title}</span>
              <span className="text-xs text-black/50 dark:text-white/50">{result.categoryName}</span>
            </button>
          ))}
        </div>
      </DialogContent>
    </Dialog>
  )
}
