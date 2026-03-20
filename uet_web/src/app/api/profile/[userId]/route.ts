import { NextResponse } from 'next/server'
import { getPrisma } from '@/lib/prisma'

export async function GET(
  request: Request,
  { params }: { params: { userId: string } }
) {
  try {
    const prisma = getPrisma()

    const user = await prisma.user.findUnique({
      where: { id: params.userId },
      select: {
        id: true,
        email: true,
        name: true,
        image: true,
        reputation: true,
        createdAt: true,
        // New profile fields (will work after prisma generate)
        ...(({ displayName: true, bio: true, avatarUrl: true, institution: true, website: true }) as any),
        _count: {
          select: {
            posts: true,
            comments: true,
          },
        },
      },
    })

    if (!user) {
      return NextResponse.json({ error: 'User not found' }, { status: 404 })
    }

    // Count followers and following
    const [followersCount, followingCount] = await Promise.all([
      (prisma as any).follow.count({ where: { followingId: params.userId } }),
      (prisma as any).follow.count({ where: { followerId: params.userId } }),
    ])

    // Recent posts
    const recentPosts = await prisma.post.findMany({
      where: { authorId: params.userId },
      orderBy: { createdAt: 'desc' },
      take: 10,
      include: {
        tags: true,
        _count: { select: { comments: true } },
      },
    })

    return NextResponse.json({
      ...user,
      followersCount,
      followingCount,
      recentPosts,
    })
  } catch (error) {
    console.error('Error fetching profile:', error)
    return NextResponse.json({ error: 'Failed to fetch profile' }, { status: 500 })
  }
}
