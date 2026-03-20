import { NextResponse } from 'next/server'
import { getPrisma } from '@/lib/prisma'

export async function GET(request: Request) {
  try {
    const prisma = getPrisma()
    const { searchParams } = new URL(request.url)
    const cursor = searchParams.get('cursor')
    const limit = parseInt(searchParams.get('limit') || '20')
    const tag = searchParams.get('tag')
    const mode = searchParams.get('mode') || 'latest' // latest | trending | following
    const userId = searchParams.get('userId') // for "following" mode

    const where: any = {}

    if (tag) {
      where.tags = { some: { name: tag } }
    }

    if (mode === 'following' && userId) {
      const following = await (prisma as any).follow.findMany({
        where: { followerId: userId },
        select: { followingId: true },
      })
      where.authorId = { in: following.map((f: any) => f.followingId) }
    }

    const orderBy: any =
      mode === 'trending'
        ? [{ upvotes: 'desc' as const }, { createdAt: 'desc' as const }]
        : [{ createdAt: 'desc' as const }]

    const posts = await prisma.post.findMany({
      where,
      orderBy,
      take: limit + 1,
      ...(cursor ? { cursor: { id: cursor }, skip: 1 } : {}),
      include: {
        author: {
          select: {
            id: true,
            email: true,
            name: true,
            image: true,
            reputation: true,
          } as any,
        },
        tags: true,
        _count: {
          select: { comments: true } as any,
        },
      },
    })

    const hasMore = posts.length > limit
    const items = hasMore ? posts.slice(0, limit) : posts
    const nextCursor = hasMore ? items[items.length - 1].id : null

    return NextResponse.json({
      posts: items,
      nextCursor,
      hasMore,
    })
  } catch (error) {
    console.error('Error fetching feed:', error)
    return NextResponse.json({ error: 'Failed to fetch feed' }, { status: 500 })
  }
}
