import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';

// Point to the new Docs folder outside the web project
const docsDirectory = path.join(process.cwd(), '../docs/Docs');

export type DocMetadata = {
  title: string;
  description?: string;
  category: string;
  categoryName: string;
  slug: string;
};

export type DocData = DocMetadata & {
  content: string;
};

// Helper to format "01_Introduction" to "Introduction"
export function formatCategoryName(dirName: string) {
  return dirName.replace(/^\d+_/, '').replace(/_/g, ' ');
}

export function getCategories(): string[] {
  if (!fs.existsSync(docsDirectory)) return [];
  return fs.readdirSync(docsDirectory).filter((file) => {
    return fs.statSync(path.join(docsDirectory, file)).isDirectory();
  }).sort(); // Keeps 01_, 02_ in order
}

export function getDocsInCategory(category: string, locale: string = 'en'): DocMetadata[] {
  const categoryPath = path.join(docsDirectory, category);
  if (!fs.existsSync(categoryPath)) return [];

  const fileNames = fs.readdirSync(categoryPath);
  
  // Map to store best file match for each base slug
  const slugMap = new Map<string, string>();
  
  fileNames.forEach((fileName) => {
    if (!fileName.endsWith('.md')) return;

    let baseSlug = fileName;
    let fileLocale = 'en';

    const localeMatch = fileName.match(/\.([a-z]{2})\.md$/);
    if (localeMatch) {
      baseSlug = fileName.replace(/\.[a-z]{2}\.md$/, '');
      fileLocale = localeMatch[1];
    } else {
      baseSlug = fileName.replace(/\.md$/, '');
    }

    if (!slugMap.has(baseSlug)) {
      slugMap.set(baseSlug, fileName);
    } else {
      const currentBest = slugMap.get(baseSlug)!;
      const currentBestLocaleMatch = currentBest.match(/\.([a-z]{2})\.md$/);
      const currentBestLocale = currentBestLocaleMatch ? currentBestLocaleMatch[1] : 'en';

      if (fileLocale === locale) {
        // Exact match takes highest priority
        slugMap.set(baseSlug, fileName);
      } else if (fileLocale === 'en' && currentBestLocale !== locale) {
        // English fallback takes priority over other non-matching locales
        slugMap.set(baseSlug, fileName);
      }
    }
  });

  const docs = Array.from(slugMap.entries()).map(([slug, fileName]) => {
    const fullPath = path.join(categoryPath, fileName);
    const fileContents = fs.readFileSync(fullPath, 'utf8');
    const { data } = matter(fileContents);

    return {
      slug,
      category,
      categoryName: formatCategoryName(category),
      title: data.title || slug,
      description: data.description || '',
    };
  });

  return docs;
}

export function getDocBySlug(category: string, slug: string, locale: string = 'en'): DocData | null {
  const basePath = path.join(docsDirectory, category, slug);
  
  let fullPath = `${basePath}.${locale}.md`;
  if (!fs.existsSync(fullPath)) fullPath = `${basePath}.en.md`;
  if (!fs.existsSync(fullPath)) fullPath = `${basePath}.md`;
  
  if (!fs.existsSync(fullPath)) return null;

  const fileContents = fs.readFileSync(fullPath, 'utf8');
  const { data, content } = matter(fileContents);

  return {
    slug,
    category,
    categoryName: formatCategoryName(category),
    title: data.title || slug,
    description: data.description || '',
    content,
  };
}

export function getAllDocs(locale: string = 'en'): DocMetadata[] {
  const categories = getCategories();
  let allDocs: DocMetadata[] = [];
  for (const cat of categories) {
    allDocs = allDocs.concat(getDocsInCategory(cat, locale));
  }
  return allDocs;
}
