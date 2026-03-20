import { redirect } from "@/i18n/routing";
import { getDocsInCategory } from "@/lib/docs";

export default async function CategoryIndexPage(props: {
  params: Promise<{ locale: string; category: string }>;
}) {
  const params = await props.params;
  const docs = getDocsInCategory(params.category, params.locale);
  
  if (docs.length > 0) {
    redirect({
      href: `/docs/${params.category}/${docs[0].slug}`,
      locale: params.locale
    });
  }

  return (
    <div className="flex items-center justify-center h-full pt-20">
      <p className="text-black/50 dark:text-white/50">No documentation found in this category.</p>
    </div>
  );
}
