import { NextRequest, NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'
import matter from 'gray-matter'

const docsDirectory = path.join(process.cwd(), '../research_uet/Docs')
const platformSpecsDirs = [
  path.join(process.cwd(), 'Docs_software_design/platform_specs'),
  path.join(process.cwd(), 'docs/software_design/platform_specs'),
]

interface DocChunk {
  path: string
  title: string
  text: string
  category: string
  score: number
}

// Load all markdown files and split into chunks
function loadAllDocs(): DocChunk[] {
  const chunks: DocChunk[] = []

  // Load research docs
  if (fs.existsSync(docsDirectory)) {
    loadDocsFromDir(docsDirectory, chunks, 'research')
  }

  // Load platform specs
  for (const platformSpecsDir of platformSpecsDirs) {
    if (fs.existsSync(platformSpecsDir)) {
      loadDocsFromDir(platformSpecsDir, chunks, 'platform_specs')
      break
    }
  }

  return chunks
}

function loadDocsFromDir(dir: string, chunks: DocChunk[], category: string) {
  const entries = fs.readdirSync(dir, { withFileTypes: true })

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name)

    if (entry.isDirectory()) {
      loadDocsFromDir(fullPath, chunks, `${category}/${entry.name}`)
    } else if (entry.name.endsWith('.md')) {
      try {
        const content = fs.readFileSync(fullPath, 'utf8')
        const { data, content: body } = matter(content)
        const title = data.title || entry.name.replace('.md', '')

        // Split into paragraphs (chunks)
        const paragraphs = body
          .split(/\n\n+/)
          .map(p => p.trim())
          .filter(p => p.length > 30)

        for (const para of paragraphs) {
          chunks.push({
            path: entry.name,
            title,
            text: para,
            category,
            score: 0,
          })
        }
      } catch {
        // Skip unreadable files
      }
    }
  }
}

// Simple keyword-based relevance scoring
function searchChunks(chunks: DocChunk[], query: string, topK: number): DocChunk[] {
  const queryLower = query.toLowerCase()
  const queryTerms = queryLower
    .split(/\s+/)
    .filter(t => t.length > 1)

  const scored = chunks.map(chunk => {
    const textLower = chunk.text.toLowerCase()
    const titleLower = chunk.title.toLowerCase()
    let score = 0

    for (const term of queryTerms) {
      // Exact word match in text
      const textMatches = (textLower.match(new RegExp(term, 'g')) || []).length
      score += textMatches * 2

      // Title match (higher weight)
      if (titleLower.includes(term)) {
        score += 5
      }

      // Path match
      if (chunk.path.toLowerCase().includes(term)) {
        score += 3
      }
    }

    // Boost longer matches for multi-word queries
    if (queryTerms.length > 1) {
      const phrase = queryTerms.join(' ')
      if (textLower.includes(phrase)) {
        score += 10
      }
    }

    // Normalize by text length to avoid long-text bias
    const normalizedScore = score / Math.max(1, Math.log(chunk.text.length))

    return { ...chunk, score: normalizedScore }
  })

  return scored
    .filter(c => c.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, topK)
}

// Multi-Agent RAG: categorize query and route to specialist
function classifyQuery(query: string): string {
  const q = query.toLowerCase()

  if (/blockchain|chain|block|mining|pow|pouw|miner|hash|consensus|ledger/i.test(q)) {
    return 'blockchain_agent'
  }
  if (/security|crypto|quantum|dilithium|signature|key|encrypt/i.test(q)) {
    return 'security_agent'
  }
  if (/economic|money|currency|wallet|uet.?cash|issuance|inflation|trade|market/i.test(q)) {
    return 'economics_agent'
  }
  if (/governance|vote|proposal|policy|council|democracy/i.test(q)) {
    return 'governance_agent'
  }
  if (/equation|physics|equilibrium|energy|master.*eq|gamma|entropy|thermodynamic/i.test(q)) {
    return 'physics_agent'
  }
  if (/social|feed|post|comment|community|collaboration|room|project/i.test(q)) {
    return 'social_agent'
  }

  return 'general_agent'
}

// Generate a synthesized answer from search results
function synthesizeAnswer(query: string, results: DocChunk[], agent: string): string {
  if (results.length === 0) {
    return `I couldn't find relevant information about "${query}" in the UET knowledge base. Try rephrasing your question or using different keywords.`
  }

  const agentLabels: Record<string, string> = {
    blockchain_agent: '⛓️ Blockchain Specialist',
    security_agent: '🔐 Security Specialist',
    economics_agent: '💰 Economics Specialist',
    governance_agent: '🏛️ Governance Specialist',
    physics_agent: '⚛️ Physics Specialist',
    social_agent: '🌐 Social Platform Specialist',
    general_agent: '🧠 General Knowledge',
  }

  const label = agentLabels[agent] || 'General'
  const topResult = results[0]

  let answer = `**${label}** analyzed your query.\n\n`
  answer += `**Most relevant:** ${topResult.title} (${topResult.path})\n\n`
  answer += `> ${topResult.text.slice(0, 500)}${topResult.text.length > 500 ? '...' : ''}\n\n`

  if (results.length > 1) {
    answer += `**Additional references:**\n`
    for (let i = 1; i < Math.min(results.length, 4); i++) {
      answer += `- **${results[i].title}** (${results[i].path}): ${results[i].text.slice(0, 150)}...\n`
    }
  }

  return answer
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { query, top_k = 5 } = body

    if (!query || typeof query !== 'string') {
      return NextResponse.json({ error: 'Missing query' }, { status: 400 })
    }

    // 1. Classify query to route to specialist agent
    const agent = classifyQuery(query)

    // 2. Load and search docs
    const allChunks = loadAllDocs()
    const results = searchChunks(allChunks, query, top_k)

    // 3. Synthesize answer
    const answer = synthesizeAnswer(query, results, agent)

    return NextResponse.json({
      answer,
      agent,
      results: results.map(r => ({
        chunk_id: `${r.path}:${r.text.slice(0, 20)}`,
        doc_id: r.path,
        text: r.text,
        path: r.path,
        score: r.score,
        metadata: { category: r.category, title: r.title },
      })),
      query_type: agent,
      total: results.length,
    })
  } catch (error) {
    console.error('Chat API error:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}
