import { NextResponse } from 'next/server'
import { getPrisma } from '@/lib/prisma'

export async function POST(
  request: Request,
  { params }: { params: { userId: string } }
) {
  try {
    const prisma = getPrisma()
    const { followerId } = await request.json()

    if (!followerId) {
      return NextResponse.json({ error: 'followerId is required' }, { status: 400 })
    }

    if (followerId === params.userId) {
      return NextResponse.json({ error: 'Cannot follow yourself' }, { status: 400 })
    }

    const existing = await (prisma as any).follow.findUnique({
      where: {
        followerId_followingId: {
          followerId,
          followingId: params.userId,
        },
      },
    })

    if (existing) {
      return NextResponse.json({ error: 'Already following' }, { status: 409 })
    }

    await (prisma as any).follow.create({
      data: {
        followerId,
        followingId: params.userId,
      },
    })

    return NextResponse.json({ following: true })
  } catch (error) {
    console.error('Error following:', error)
    return NextResponse.json({ error: 'Failed to follow' }, { status: 500 })
  }
}

export async function DELETE(
  request: Request,
  { params }: { params: { userId: string } }
) {
  try {
    const prisma = getPrisma()
    const { searchParams } = new URL(request.url)
    const followerId = searchParams.get('followerId')

    if (!followerId) {
      return NextResponse.json({ error: 'followerId is required' }, { status: 400 })
    }

    await (prisma as any).follow.deleteMany({
      where: {
        followerId,
        followingId: params.userId,
      },
    })

    return NextResponse.json({ following: false })
  } catch (error) {
    console.error('Error unfollowing:', error)
    return NextResponse.json({ error: 'Failed to unfollow' }, { status: 500 })
  }
}
