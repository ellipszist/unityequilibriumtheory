import { NextResponse } from 'next/server'
import { getPrisma } from '@/lib/prisma'

export async function GET(request: Request) {
  try {
    const prisma = getPrisma()
    const { searchParams } = new URL(request.url)
    const userId = searchParams.get('userId')
    const unreadOnly = searchParams.get('unread') === 'true'

    if (!userId) {
      return NextResponse.json({ error: 'userId is required' }, { status: 400 })
    }

    // For now, generate notifications from recent activity
    // In production, store in a dedicated Notification model
    const notifications: any[] = []

    // Recent comments on user's posts
    const recentComments = await prisma.comment.findMany({
      where: {
        post: { authorId: userId },
        authorId: { not: userId },
      },
      orderBy: { createdAt: 'desc' },
      take: 10,
      include: {
        author: { select: { id: true, email: true, name: true } as any },
        post: { select: { id: true, title: true } },
      },
    })

    for (const c of recentComments) {
      const name = (c.author as any).displayName || (c.author as any).name || (c.author as any).email?.split('@')[0]
      notifications.push({
        id: `comment-${c.id}`,
        type: 'comment',
        message: `${name} commented on "${c.post.title}"`,
        link: `/post/${c.post.id}`,
        createdAt: c.createdAt,
        read: false,
      })
    }

    // Recent followers
    const recentFollows = await (prisma as any).follow.findMany({
      where: { followingId: userId },
      orderBy: { createdAt: 'desc' },
      take: 10,
      include: {
        follower: { select: { id: true, email: true, displayName: true, avatarUrl: true } },
      },
    })

    for (const f of recentFollows) {
      const name = f.follower.displayName || f.follower.email?.split('@')[0]
      notifications.push({
        id: `follow-${f.id}`,
        type: 'follow',
        message: `${name} started following you`,
        link: `/profile/${f.follower.id}`,
        createdAt: f.createdAt,
        read: false,
      })
    }

    // Sort by date
    notifications.sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime())

    return NextResponse.json({
      notifications: notifications.slice(0, 20),
      unreadCount: notifications.length,
    })
  } catch (error) {
    console.error('Error fetching notifications:', error)
    return NextResponse.json({ error: 'Failed to fetch notifications' }, { status: 500 })
  }
}
