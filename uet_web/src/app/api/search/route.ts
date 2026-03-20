import { NextResponse } from 'next/server'
import { getPrisma } from '@/lib/prisma'

export async function GET(request: Request) {
  try {
    const prisma = getPrisma()
    const { searchParams } = new URL(request.url)
    const q = searchParams.get('q')?.trim()
    const type = searchParams.get('type') || 'all' // all | posts | users
    const limit = parseInt(searchParams.get('limit') || '20')

    if (!q || q.length < 2) {
      return NextResponse.json({ posts: [], users: [] })
    }

    const results: { posts: any[]; users: any[] } = { posts: [], users: [] }

    if (type === 'all' || type === 'posts') {
      results.posts = await prisma.post.findMany({
        where: {
          OR: [
            { title: { contains: q, mode: 'insensitive' } },
            { content: { contains: q, mode: 'insensitive' } },
          ],
        },
        orderBy: { createdAt: 'desc' },
        take: limit,
        include: {
          author: {
            select: { id: true, email: true, name: true, reputation: true } as any,
          },
          tags: true,
          _count: { select: { comments: true } },
        },
      })
    }

    if (type === 'all' || type === 'users') {
      results.users = await prisma.user.findMany({
        where: {
          OR: [
            { email: { contains: q, mode: 'insensitive' } },
            { name: { contains: q, mode: 'insensitive' } },
          ] as any,
        },
        take: limit,
        select: {
          id: true,
          email: true,
          name: true,
          reputation: true,
        } as any,
      })
    }

    return NextResponse.json(results)
  } catch (error) {
    console.error('Search error:', error)
    return NextResponse.json({ error: 'Search failed' }, { status: 500 })
  }
}
