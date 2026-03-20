import { getCategories, formatCategoryName, getDocsInCategory } from "@/lib/docs";
import Link from "next/link";
import { LocaleSwitcher } from "@/components/locale-switcher";
import { ThemeToggle } from "@/components/theme-toggle";
import { DocSearch } from "@/components/docs/search";
import { Menu } from "lucide-react";
import { Sheet, SheetContent, SheetTrigger, SheetTitle, SheetHeader } from "@/components/ui/sheet";

export default async function DocsLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const resolvedParams = await params;
  const categories = getCategories();

  return (
    <div className="flex flex-col min-h-screen bg-white dark:bg-[#0a0a0f] text-black dark:text-white text-sm transition-colors">
      {/* Top bar */}
      <header className="sticky top-0 z-20 flex items-center h-12 px-4 border-b border-black/10 dark:border-white/10 bg-white/90 dark:bg-[#0a0a0f]/90 backdrop-blur-md gap-4">
        {/* Mobile Menu Trigger */}
        <div className="md:hidden flex items-center">
          <Sheet>
            <SheetTrigger className="p-1.5 -ml-1.5 mr-1 text-black/70 hover:text-black dark:text-white/70 dark:hover:text-white rounded-md hover:bg-black/5 dark:hover:bg-white/10 transition-colors">
              <Menu size={18} />
            </SheetTrigger>
            <SheetContent side="left" className="w-72 p-0 bg-white dark:bg-[#0a0a0f] border-r border-black/10 dark:border-white/10">
              <SheetHeader className="p-4 border-b border-black/10 dark:border-white/10 text-left">
                <SheetTitle className="flex items-center gap-2 font-bold text-base">
                  <img src="/logo.png" alt="UET Logo" className="w-6 h-6 object-contain" />
                  UET Docs
                </SheetTitle>
              </SheetHeader>
              <div className="p-4 flex flex-col gap-6 overflow-y-auto h-[calc(100vh-4rem)]">
                {categories.map((category) => {
                  const docs = getDocsInCategory(category, resolvedParams.locale);
                  return (
                    <div key={category}>
                      <p className="text-[11px] font-semibold uppercase tracking-widest text-black/40 dark:text-white/40 mb-2 px-2">
                        {formatCategoryName(category)}
                      </p>
                      <div className="flex flex-col gap-0.5">
                        {docs.map((doc) => (
                          <Link
                            key={doc.slug}
                            href={`/docs/${category}/${doc.slug}`}
                            className="flex items-center px-2 py-2 rounded-md text-[13px] transition-colors text-black/70 hover:text-black hover:bg-black/5 dark:text-white/70 dark:hover:text-white dark:hover:bg-white/5"
                          >
                            {doc.title}
                          </Link>
                        ))}
                      </div>
                    </div>
                  );
                })}
              </div>
            </SheetContent>
          </Sheet>
        </div>

        <Link href="/" className="flex items-center gap-2 font-bold text-base shrink-0">
          <img src="/logo.png" alt="UET Logo" className="w-6 h-6 object-contain" />
          <span className="hidden sm:inline">UET</span>
        </Link>

        {/* Nav tabs */}
        <nav className="hidden md:flex items-center gap-0 ml-2 text-xs overflow-x-auto">
          {categories.map((cat, i) => (
            <Link
              key={cat}
              href={`/docs/${cat}`}
              className={`px-3 py-1.5 rounded-md transition-colors whitespace-nowrap ${
                i === 0 // We can make this dynamic later based on path
                  ? "bg-black/5 dark:bg-white/10 text-black dark:text-white font-medium"
                  : "text-black/50 hover:text-black dark:text-white/50 dark:hover:text-white"
              }`}
            >
              {formatCategoryName(cat)}
            </Link>
          ))}
        </nav>

        <div className="flex-1" />

        {/* Search */}
        <div className="hidden md:flex mx-4">
          <DocSearch />
        </div>

        {/* Mobile Search Icon */}
        <div className="md:hidden">
          <DocSearch />
        </div>

        {/* Right actions */}
        <div className="flex items-center gap-1 sm:gap-2">
          <LocaleSwitcher />
          <ThemeToggle />
        </div>
      </header>

      {/* Main content area with Sidebar */}
      <div className="flex flex-1 overflow-hidden h-[calc(100vh-3rem)]">
        {/* Left Sidebar */}
        <aside className="hidden md:flex flex-col w-64 shrink-0 border-r border-black/10 dark:border-white/10 overflow-y-auto py-6 bg-black/5 dark:bg-[#0a0a0f]">
          {categories.map((category) => {
            const docs = getDocsInCategory(category, resolvedParams.locale);
            return (
              <div key={category} className="mb-6 px-3">
                <p className="text-[11px] font-semibold uppercase tracking-widest text-black/40 dark:text-white/40 mb-2 px-2">
                  {formatCategoryName(category)}
                </p>
                <div className="flex flex-col gap-0.5">
                  {docs.map((doc) => (
                    <Link
                      key={doc.slug}
                      href={`/docs/${category}/${doc.slug}`}
                      className="flex items-center px-2 py-1.5 rounded-md text-[13px] transition-colors text-black/60 hover:text-black hover:bg-black/5 dark:text-white/60 dark:hover:text-white dark:hover:bg-white/5"
                    >
                      {doc.title}
                    </Link>
                  ))}
                </div>
              </div>
            );
          })}
        </aside>

        {/* Main Content */}
        <main className="flex-1 overflow-y-auto bg-white dark:bg-[#0a0a0f]">
          {children}
        </main>
      </div>
    </div>
  );
}
