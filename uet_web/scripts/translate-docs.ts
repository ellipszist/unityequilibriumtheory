import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';
import { OpenAI } from 'openai';
import pLimit from 'p-limit';
import dotenv from 'dotenv';

// Load environment variables from uet_web/.env.local or .env
dotenv.config({ path: path.join(__dirname, '../.env.local') });
dotenv.config({ path: path.join(__dirname, '../.env') });

const apiKey = process.env.OPENAI_API_KEY;
if (!apiKey) {
  console.error('❌ Error: OPENAI_API_KEY is not set in your .env or .env.local file.');
  console.error('Please add it and try again.');
  process.exit(1);
}

const openai = new OpenAI({ apiKey });

// Target docs directory
const DOCS_DIR = path.join(__dirname, '../../docs/Docs');

// Target locales to translate to
const TARGET_LOCALES = ['th', 'zh'];

// Map locale codes to prompt instructions
const LOCALE_PROMPTS: Record<string, string> = {
  th: 'Translate the following Markdown documentation into Thai. Preserve all Markdown formatting, code blocks, frontmatter structure, and technical terms where appropriate.',
  zh: 'Translate the following Markdown documentation into Simplified Chinese. Preserve all Markdown formatting, code blocks, frontmatter structure, and technical terms where appropriate.'
};

async function translateText(text: string, targetLocale: string): Promise<string> {
  const systemPrompt = LOCALE_PROMPTS[targetLocale];
  
  try {
    const response = await openai.chat.completions.create({
      model: 'gpt-4o-mini', // or 'gpt-4o' for better quality but higher cost
      messages: [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: text }
      ],
      temperature: 0.3,
    });

    return response.choices[0].message.content || text;
  } catch (error) {
    console.error(`❌ Translation to ${targetLocale} failed:`, error);
    throw error;
  }
}

async function translateFile(sourcePath: string, fileName: string, categoryPath: string) {
  console.log(`\n📄 Processing: ${path.join(path.basename(categoryPath), fileName)}`);
  
  const fileContents = fs.readFileSync(sourcePath, 'utf8');
  const parsed = matter(fileContents);
  const baseSlug = fileName.replace(/\.en\.md$/, '').replace(/\.md$/, '');

  for (const locale of TARGET_LOCALES) {
    const targetFileName = `${baseSlug}.${locale}.md`;
    const targetPath = path.join(categoryPath, targetFileName);

    // Skip if translation already exists to save API costs
    // If you want to force re-translate, you can comment this out or pass a --force flag
    if (fs.existsSync(targetPath)) {
      console.log(`   ⏭️  Skipping ${locale} (already exists)`);
      continue;
    }

    console.log(`   🔄 Translating to ${locale}...`);
    
    try {
      // We translate the title and description in frontmatter separately from the content
      const newFrontmatter = { ...parsed.data };
      
      if (newFrontmatter.title) {
        newFrontmatter.title = await translateText(newFrontmatter.title, locale);
      }
      if (newFrontmatter.description) {
        newFrontmatter.description = await translateText(newFrontmatter.description, locale);
      }

      const translatedContent = await translateText(parsed.content, locale);
      
      // Reassemble with gray-matter
      const translatedFileContents = matter.stringify(translatedContent, newFrontmatter);
      
      fs.writeFileSync(targetPath, translatedFileContents, 'utf8');
      console.log(`   ✅ Saved ${targetFileName}`);
    } catch (error) {
      console.error(`   ❌ Failed to process ${locale} for ${baseSlug}`);
    }
  }
}

async function main() {
  console.log('🚀 Starting UET Docs Auto-Translator...');
  
  if (!fs.existsSync(DOCS_DIR)) {
    console.error(`❌ Docs directory not found at ${DOCS_DIR}`);
    process.exit(1);
  }

  const categories = fs.readdirSync(DOCS_DIR).filter((file) => {
    return fs.statSync(path.join(DOCS_DIR, file)).isDirectory();
  });

  const limit = pLimit(3); // Process up to 3 files concurrently
  const tasks: Promise<void>[] = [];

  for (const category of categories) {
    const categoryPath = path.join(DOCS_DIR, category);
    const files = fs.readdirSync(categoryPath);

    for (const file of files) {
      // Only process base .md or .en.md files (ignore .th.md, .zh.md)
      if (file.endsWith('.md') && !file.endsWith('.th.md') && !file.endsWith('.zh.md')) {
        const sourcePath = path.join(categoryPath, file);
        tasks.push(limit(() => translateFile(sourcePath, file, categoryPath)));
      }
    }
  }

  await Promise.all(tasks);
  console.log('\n🎉 All translations completed!');
}

main().catch(console.error);
