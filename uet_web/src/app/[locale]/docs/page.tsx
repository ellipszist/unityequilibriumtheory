import { redirect } from "@/i18n/routing";
import { getCategories, getDocsInCategory } from "@/lib/docs";

export default async function DocsIndexPage(props: { params: Promise<{ locale: string }> }) {
  const params = await props.params;
  const categories = getCategories();
  
  if (categories.length > 0) {
    const firstCategory = categories[0];
    const docs = getDocsInCategory(firstCategory, params.locale);
    
    if (docs.length > 0) {
      redirect({
        href: `/docs/${firstCategory}/${docs[0].slug}`,
        locale: params.locale
      });
    }
  }

  return (
    <div className="flex items-center justify-center h-full pt-20">
      <p className="text-black/50 dark:text-white/50">No documentation found.</p>
    </div>
  );
}
